"""Agent observability – logfire tracing to a local JSONL file.

Call ``configure_agent_logging()`` once at process startup (after env vars are
loaded) to start capturing every pydantic-ai span to ``logs/agent_traces.jsonl``
in the repo root.

Each line in the file is a JSON object. LLM spans are written in an
OpenAI-style envelope (type "agent" or "generation"); all other spans are
written as raw attribute dicts.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import logfire
from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter, SpanExportResult

_REPO_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_TRACE_PATH = _REPO_ROOT / "logs" / "agent_traces.jsonl"


class FileSpanExporter(SpanExporter):
    """Appends spans to a newline-delimited JSON file."""

    def __init__(self, path: Path = _DEFAULT_TRACE_PATH) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _maybe_json(value):
        if isinstance(value, str):
            value = value.strip()
            if value and value[0] in ("{", "["):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
        return value

    @staticmethod
    def _to_iso_utc(nanoseconds: int) -> str:
        return datetime.fromtimestamp(nanoseconds / 1_000_000_000, tz=timezone.utc).isoformat()

    @staticmethod
    def _is_llm_span(attributes: dict) -> bool:
        return any(key.startswith("gen_ai.") for key in attributes)

    def _export_llm_span(self, span, attributes: dict) -> dict:
        usage = {}
        if attributes.get("gen_ai.usage.input_tokens") is not None:
            usage["input_tokens"] = attributes["gen_ai.usage.input_tokens"]
        if attributes.get("gen_ai.usage.output_tokens") is not None:
            usage["output_tokens"] = attributes["gen_ai.usage.output_tokens"]
        if attributes.get("gen_ai.usage.details.reasoning_tokens") is not None:
            usage["reasoning_tokens"] = attributes["gen_ai.usage.details.reasoning_tokens"]

        parent_context = getattr(span, "parent", None)
        parent_id = f"span_{format(parent_context.span_id, '016x')}" if parent_context else None

        operation = attributes.get("gen_ai.operation.name")
        if operation == "invoke_agent":
            span_data = {
                "type": "agent",
                "name": attributes.get("gen_ai.agent.name") or span.name,
                "handoffs": None,
                "tools": None,
                "output_type": None,
            }
        else:
            span_data = {
                "type": "generation",
                "input": self._maybe_json(attributes.get("gen_ai.input.messages")),
                "output": self._maybe_json(attributes.get("gen_ai.output.messages")),
                "model": attributes.get("gen_ai.response.model") or attributes.get("gen_ai.request.model"),
                "model_config": self._maybe_json(attributes.get("model_request_parameters")),
                "usage": usage or None,
            }

        return {
            "object": "trace.span",
            "id": f"span_{format(span.context.span_id, '016x')}",
            "trace_id": f"trace_{format(span.context.trace_id, '032x')}",
            "parent_id": parent_id,
            "started_at": self._to_iso_utc(span.start_time),
            "ended_at": self._to_iso_utc(span.end_time),
            "span_data": span_data,
            "error": None,
        }

    def export(self, spans) -> SpanExportResult:
        records = []
        for span in spans:
            attributes = dict(span.attributes or {})
            if self._is_llm_span(attributes):
                records.append(self._export_llm_span(span, attributes))
            else:
                records.append({
                    "name": span.name,
                    "trace_id": format(span.context.trace_id, "032x"),
                    "span_id": format(span.context.span_id, "016x"),
                    "attributes": attributes,
                    "start_time": span.start_time,
                    "end_time": span.end_time,
                })
        with open(self.path, "a", encoding="utf-8") as f:
            for record in records:
                f.write(json.dumps(record, default=str))
                f.write("\n")
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        pass


def configure_agent_logging(trace_path: Path = _DEFAULT_TRACE_PATH) -> None:
    """Configure logfire to trace pydantic-ai spans to *trace_path*.

    Safe to call multiple times – logfire ignores repeated configure() calls.
    """
    logfire.configure(
        send_to_logfire="if-token-present",
        additional_span_processors=[
            BatchSpanProcessor(FileSpanExporter(trace_path))
        ]
    )
    logfire.instrument_pydantic_ai()
