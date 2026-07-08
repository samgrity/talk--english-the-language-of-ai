#!/usr/bin/env python3
"""Navigate agent traces from logs/agent_traces.jsonl.

Model-traffic traces (type=generation) are the spans of interest.
Agent-level spans (type=agent) and raw observability spans are filtered out.

Usage:
  navigate_traces.py --count / -c
  navigate_traces.py --trace N / -t N  [--full / -f]
"""

import argparse
import json
import sys
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


def load_spans() -> list[dict]:
    if not TRACES_PATH.exists():
        sys.exit(f"Traces file not found: {TRACES_PATH}")
    spans = []
    with open(TRACES_PATH, encoding="utf-8") as f:
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


# ── Main trace renderer ───────────────────────────────────────────────────────

def render_trace(span: dict, *, show_instructions: bool, show_tools: bool,
                 full_responses: bool) -> None:
    sd = span["span_data"]
    mc = sd.get("model_config") or {}

    # ── header ──
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

    for msg in all_messages:
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
    parser.add_argument("-f", "--full", action="store_true",
                        help="Show instructions, tool definitions, and untruncated tool responses")
    args = parser.parse_args()

    spans = load_spans()
    traces = model_traffic(spans)

    if args.count:
        print(f"{len(traces)} model-traffic trace(s) in {TRACES_PATH}")

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
            show_instructions=args.full,
            show_tools=args.full,
            full_responses=args.full,
        )


if __name__ == "__main__":
    main()
