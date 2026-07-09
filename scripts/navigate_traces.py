#!/usr/bin/env python3
"""Navigate agent traces from logs/agent_traces.jsonl.

Model-traffic traces (type=generation) are the spans of interest.
Agent-level spans (type=agent) and raw observability spans are filtered out.

Usage:
  navigate_traces.py --count / -c
  navigate_traces.py --trace N / -t N  [--verbose / -v]
  navigate_traces.py --follow / -f     [--verbose / -v]
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from textwrap import indent

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover
    yaml = None

# ── ANSI colours ─────────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"

# message roles
C_USER      = "\033[36m"   # cyan
C_ASSISTANT = "\033[32m"   # green
C_THINKING  = "\033[35m"   # magenta
C_TOOL_CALL = "\033[33m"   # yellow
C_TOOL_RESP = "\033[34m"   # blue
C_HEADER    = "\033[1;37m" # bold white
C_META      = "\033[90m"   # dark grey
C_INSTR     = "\033[96m"   # bright cyan
C_TOOLDEF   = "\033[93m"   # bright yellow


def color(c: str, text: str) -> str:
    return f"{c}{text}{RESET}"


# ── File loading ──────────────────────────────────────────────────────────────

TRACES_PATH = Path(__file__).resolve().parents[1] / "logs" / "agent_traces.jsonl"


def load_spans(file_path: Path | None = None) -> list[dict]:
    path = file_path or TRACES_PATH
    if not path.exists():
        sys.exit(f"Traces file not found: {path}")
    spans = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                spans.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return spans


def model_traffic(spans: list[dict]) -> list[dict]:
    """Return only generation-type spans that have actual input/output."""
    return [
        s for s in spans
        if s.get("span_data", {}).get("type") == "generation"
        and (s["span_data"].get("input") or s["span_data"].get("output"))
    ]


# ── Rendering helpers ─────────────────────────────────────────────────────────

TRUNCATE_AT = 300


if yaml is not None:
    class _PrettyYAMLDumper(yaml.SafeDumper):
        pass


    def _str_presenter(dumper, data):
        if "\n" in data:
            return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
        return dumper.represent_scalar("tag:yaml.org,2002:str", data)


    _PrettyYAMLDumper.add_representer(str, _str_presenter)


def _try_parse_entire_json(text: str):
    stripped = text.strip()
    if not stripped or stripped[0] not in "[{":
        return None
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return None


def _to_pretty_yaml(data: dict | list) -> str:
    if yaml is None:
        return json.dumps(data, indent=2, ensure_ascii=False)
    dumped = yaml.dump(
        data,
        Dumper=_PrettyYAMLDumper,
        sort_keys=False,
        allow_unicode=True,
        default_flow_style=False,
        width=10_000,
    )
    return dumped.rstrip()


def _render_structured_if_json(text: str) -> str:
    structured = _try_parse_entire_json(text)
    if structured is None:
        return text
    return _to_pretty_yaml(structured)


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + color(DIM, f"… [{len(text) - limit} chars omitted]")


def fmt_args(arguments: dict | str) -> str:
    """Render tool arguments as named-arg call."""
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except Exception:
            return repr(arguments)
    if not isinstance(arguments, dict):
        return repr(arguments)
    parts = ", ".join(f"{k}={json.dumps(v)}" for k, v in arguments.items())
    return f"({parts})"


def fmt_tool_call(part: dict) -> str:
    name = part.get("name", "?")
    args = part.get("arguments", {})
    builtin = part.get("builtin")
    tag = f"[builtin]" if builtin else ""
    return color(C_TOOL_CALL, f"⚙ tool_call{tag}: {name}{fmt_args(args)}")


def fmt_tool_response(part: dict, full_responses: bool) -> str:
    name = part.get("name", "?")
    result = part.get("result", "")

    structured = None
    if isinstance(result, (dict, list)):
        structured = result
    elif isinstance(result, str):
        structured = _try_parse_entire_json(result)

    if structured is not None:
        result = _to_pretty_yaml(structured)
    else:
        result = str(result)

    if not full_responses:
        result = truncate(result, TRUNCATE_AT)
    return color(C_TOOL_RESP, f"↩ tool_response: {name}\n{result}")


def fmt_instruction_part(part: dict) -> str:
    content = part.get("content", "")
    dynamic = part.get("dynamic", False)
    tag = " (dynamic)" if dynamic else ""
    return color(C_INSTR, f"[instruction{tag}]\n{content}")


def fmt_tool_def(tool: dict) -> str:
    """Render a function tool definition in YAML-ish style."""
    name = tool.get("name", "?")
    desc = tool.get("description", "")
    schema = tool.get("parameters_json_schema", {})
    props = schema.get("properties", {})
    lines = [color(C_TOOLDEF, f"  - {name}:")]
    if desc:
        lines.append(f"      description: {desc}")
    if props:
        lines.append("      parameters:")
        for pname, pdef in props.items():
            ptype = pdef.get("type", "any")
            pdesc = pdef.get("description", "")
            lines.append(f"        {pname} ({ptype}): {pdesc}")
    return "\n".join(lines)


def fmt_builtin_tool(tool: dict) -> str:
    kind = tool.get("kind", "?")
    rest = {k: v for k, v in tool.items() if k != "kind" and v is not None and v is not False}
    lines = [color(C_TOOLDEF, f"  - {kind}: (builtin)")]
    for k, v in rest.items():
        lines.append(f"      {k}: {v}")
    return "\n".join(lines)


# ── Diff helpers ──────────────────────────────────────────────────────────────

def _message_key(msg: dict) -> list[str]:
    """Return a stable list of canonical strings, one per part, for comparison."""
    keys: list[str] = []
    for part in msg.get("parts") or []:
        ptype = part.get("type", "?")
        if ptype in ("text", "thinking"):
            keys.append(f"{ptype}:{part.get('content', '')}")
        elif ptype == "tool_call":
            name = part.get("name", "?")
            args = json.dumps(part.get("arguments", {}), sort_keys=True)
            keys.append(f"tool_call:{name}:{args}")
        elif ptype == "tool_call_response":
            name = part.get("name", "?")
            result = part.get("result", "")
            if isinstance(result, (dict, list)):
                result = json.dumps(result, sort_keys=True)
            keys.append(f"tool_call_response:{name}:{result}")
        else:
            keys.append(f"{ptype}:{json.dumps(part, sort_keys=True)}")
    return keys


def new_messages_only(new_trace: dict, old_trace: dict) -> list[dict]:
    """Return messages present in *new_trace* but not in *old_trace*."""
    old_keys = set()
    for msg in (old_trace.get("span_data", {}).get("input") or []) + (old_trace.get("span_data", {}).get("output") or []):
        old_keys.add("\n".join(_message_key(msg)))

    added: list[dict] = []
    for msg in (new_trace.get("span_data", {}).get("input") or []) + (new_trace.get("span_data", {}).get("output") or []):
        if "\n".join(_message_key(msg)) not in old_keys:
            added.append(msg)
    return added


# ── Main trace renderer ───────────────────────────────────────────────────────

def render_messages(messages: list[dict], full_responses: bool) -> None:
    """Render a flat list of message dicts with role-based colours."""
    for msg in messages:
        role = msg.get("role", "?")
        parts = msg.get("parts") or []

        for part in parts:
            ptype = part.get("type", "?")

            if ptype == "text":
                content = _render_structured_if_json(part.get("content", ""))
                if role == "user":
                    print(color(C_USER, f"\n[user]\n{content}"))
                else:
                    print(color(C_ASSISTANT, f"\n[assistant]\n{content}"))

            elif ptype == "thinking":
                content = part.get("content", "")
                print(color(C_THINKING, f"\n[thinking]\n{content}"))

            elif ptype == "tool_call":
                print(f"\n{fmt_tool_call(part)}")

            elif ptype == "tool_call_response":
                print(f"\n{fmt_tool_response(part, full_responses)}")

            else:
                print(color(C_META, f"\n  [{ptype}] {str(part)[:200]}"))


def render_trace(span: dict, *, show_instructions: bool, show_tools: bool,
                 full_responses: bool, show_header: bool = True) -> None:
    sd = span["span_data"]
    mc = sd.get("model_config") or {}

    # ── header ──
    if show_header:
        model = sd.get("model") or "unknown model"
        usage = sd.get("usage") or {}
        in_tok = usage.get("input_tokens", "?")
        out_tok = usage.get("output_tokens", "?")
        started = span.get("started_at", "")
        ended = span.get("ended_at", "")
        print(color(C_HEADER, f"\n{'─'*70}"))
        print(color(C_HEADER, f"  model: {model}"))
        print(color(C_META,   f"  tokens: {in_tok} in / {out_tok} out   {started} → {ended}"))
        print(color(C_HEADER, f"{'─'*70}"))

    # ── instructions ──
    if show_instructions:
        instr_parts = mc.get("instruction_parts") or []
        if instr_parts:
            print(color(C_INSTR, "\n[INSTRUCTIONS]"))
            for part in instr_parts:
                if isinstance(part, dict):
                    print(fmt_instruction_part(part))
                else:
                    print(indent(str(part), "    "))

    # ── tool definitions ──
    if show_tools:
        fn_tools = mc.get("function_tools") or []
        bt_tools = mc.get("builtin_tools") or []
        if fn_tools or bt_tools:
            print(color(C_TOOLDEF, "\n[TOOL DEFINITIONS]"))
            for t in fn_tools:
                print(fmt_tool_def(t))
            for t in bt_tools:
                print(fmt_builtin_tool(t))

    # ── messages ──
    print()
    all_messages = list(sd.get("input") or []) + list(sd.get("output") or [])
    render_messages(all_messages, full_responses)
    print()


# ── Follow mode ───────────────────────────────────────────────────────────────

POLL_INTERVAL = 1.0  # seconds


def _file_size(path: Path) -> int:
    try:
        return path.stat().st_size
    except FileNotFoundError:
        return 0


def follow_traces(traces_file: Path, verbose: bool) -> None:
    # Load current state
    all_spans = load_spans(traces_file)
    traces = model_traffic(all_spans)

    if not traces:
        print("No traces yet. Waiting for new traces…")
    else:
        last = traces[-1]
        print(color(C_META, f"Showing last trace (#{len(traces)})…"))
        render_trace(last, show_instructions=verbose, show_tools=verbose,
                     full_responses=verbose)
        print(color(C_META, f"Watching {traces_file} for new traces… (Ctrl-C to stop)"))

    prev_size = _file_size(traces_file)
    prev_traces = traces

    try:
        while True:
            time.sleep(POLL_INTERVAL)
            current_size = _file_size(traces_file)

            if current_size <= prev_size:
                continue

            # Read only new bytes from the file
            with open(traces_file, encoding="utf-8") as f:
                f.seek(prev_size)
                new_bytes = f.read(current_size - prev_size)

            prev_size = current_size

            # Parse any new spans
            new_spans: list[dict] = []
            for line in new_bytes.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    new_spans.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

            new_traces = model_traffic(new_spans)
            if not new_traces:
                continue

            for trace in new_traces:
                trace_idx = len(prev_traces) + 1
                print(color(C_META, f"\n--- new trace #{trace_idx} ---"))

                if prev_traces:
                    added = new_messages_only(trace, prev_traces[-1])
                    if added:
                        render_messages(added, full_responses=verbose)
                    else:
                        print(color(C_META, "  (no new messages detected in this trace)"))

                print()  # trailing blank line for readability
                prev_traces.append(trace)

    except KeyboardInterrupt:
        print()


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Navigate agent traces from logs/agent_traces.jsonl"
    )
    parser.add_argument("-c", "--count", action="store_true",
                        help="Print the number of model-traffic traces")
    parser.add_argument("-t", "--trace", type=int, metavar="N",
                        help="Print trace N (1-indexed)")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show instructions, tool definitions, and untruncated tool responses")
    parser.add_argument("-f", "--follow", action="store_true",
                        help="Print the last trace and follow, printing new messages as they arrive")
    args = parser.parse_args()

    if args.follow and args.trace is not None:
        sys.exit("--follow (-f) and --trace (-t) are mutually exclusive.")

    spans = load_spans()
    traces = model_traffic(spans)

    if args.count:
        print(f"{len(traces)} model-traffic trace(s) in {TRACES_PATH}")

    if args.follow:
        follow_traces(TRACES_PATH, verbose=args.verbose)
        return

    # Determine which trace to show: explicit -t, or default to last.
    if args.trace is not None:
        n = args.trace
    elif not args.count:
        n = len(traces)
    else:
        n = None  # -c only

    if n is not None:
        if len(traces) == 0:
            sys.exit("No traces found.")
        if n < 1 or n > len(traces):
            sys.exit(f"Trace {n} out of range (1–{len(traces)})")
        render_trace(
            traces[n - 1],
            show_instructions=args.verbose,
            show_tools=args.verbose,
            full_responses=args.verbose,
        )


if __name__ == "__main__":
    main()
