"""MCP server exposing VictoriaLogs and VictoriaTraces tools."""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel


class LogsSearchArgs(BaseModel):
    query: str = ""
    time_range: str = "1h"
    limit: int = 50


class LogsErrorCountArgs(BaseModel):
    time_range: str = "1h"
    group_by: str = "service.name"


class TracesListArgs(BaseModel):
    service: str = ""
    limit: int = 20


class TracesGetArgs(BaseModel):
    trace_id: str


class ToolSpec(BaseModel):
    name: str
    description: str
    model: type[BaseModel]

    def as_tool(self) -> Tool:
        schema = self.model.model_json_schema()
        return Tool(
            name=self.name,
            description=self.description,
            inputSchema=schema,
        )


TOOL_SPECS = [
    ToolSpec(
        name="logs_search",
        description="Search logs in VictoriaLogs using LogsQL. "
        "Args: query (LogsQL query string), time_range (e.g. '1h', '10m'), limit (max entries).",
        model=LogsSearchArgs,
    ),
    ToolSpec(
        name="logs_error_count",
        description="Count errors per service over a time window. "
        "Args: time_range (e.g. '1h', '10m'), group_by (field to group by).",
        model=LogsErrorCountArgs,
    ),
    ToolSpec(
        name="traces_list",
        description="List recent traces for a service from VictoriaTraces. "
        "Args: service (service name), limit (max traces).",
        model=TracesListArgs,
    ),
    ToolSpec(
        name="traces_get",
        description="Fetch a specific trace by ID from VictoriaTraces. "
        "Args: trace_id (the trace ID to fetch).",
        model=TracesGetArgs,
    ),
]

TOOLS_BY_NAME = {spec.name: spec for spec in TOOL_SPECS}


class ObsSettings(BaseModel):
    victorialogs_url: str
    victoriatraces_url: str


def resolve_settings() -> ObsSettings:
    return ObsSettings(
        victorialogs_url=os.environ.get(
            "VICTORIALOGS_URL", "http://victorialogs:9428"
        ),
        victoriatraces_url=os.environ.get(
            "VICTORIATRACES_URL", "http://victoriatraces:10428"
        ),
    )


async def logs_search(client: httpx.AsyncClient, settings: ObsSettings, args: LogsSearchArgs) -> str:
    """Search logs in VictoriaLogs."""
    logsql_query = f"_time:{args.time_range}"
    if args.query:
        logsql_query = f"{logsql_query} {args.query}"

    response = await client.get(
        f"{settings.victorialogs_url}/select/logsql/query",
        params={"query": logsql_query, "limit": args.limit},
        timeout=30.0,
    )
    response.raise_for_status()

    content = response.text
    try:
        data = json.loads(content)
        return json.dumps(data, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        return content


async def logs_error_count(
    client: httpx.AsyncClient, settings: ObsSettings, args: LogsErrorCountArgs
) -> str:
    """Count errors per service over a time window."""
    logsql_query = f"_time:{args.time_range} severity:ERROR"

    response = await client.get(
        f"{settings.victorialogs_url}/select/logsql/query",
        params={"query": logsql_query, "limit": 1000},
        timeout=30.0,
    )
    response.raise_for_status()

    content = response.text
    try:
        logs = json.loads(content)
    except json.JSONDecodeError:
        return json.dumps({"error": "Failed to parse logs response"})

    error_counts: dict[str, int] = {}

    if isinstance(logs, list):
        for entry in logs:
            if isinstance(entry, dict):
                field_value = entry.get(args.group_by, "unknown")
                if isinstance(field_value, dict):
                    field_value = field_value.get("value", "unknown")
                error_counts[str(field_value)] = error_counts.get(str(field_value), 0) + 1
    elif isinstance(logs, dict):
        hits = logs.get("hits", [])
        for entry in hits:
            if isinstance(entry, dict):
                fields = entry.get("fields", {})
                field_value = fields.get(args.group_by, "unknown")
                error_counts[str(field_value)] = error_counts.get(str(field_value), 0) + 1

    return json.dumps(
        {"time_range": args.time_range, "error_counts": error_counts},
        ensure_ascii=False,
        indent=2,
    )


async def traces_list(
    client: httpx.AsyncClient, settings: ObsSettings, args: TracesListArgs
) -> str:
    """List recent traces for a service."""
    endpoint = f"{settings.victoriatraces_url}/select/jaeger/api/traces"
    params = {"limit": args.limit}
    if args.service:
        params["service"] = args.service

    response = await client.get(endpoint, params=params, timeout=30.0)
    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):
        traces_data = data.get("data", [])
    elif isinstance(data, list):
        traces_data = data
    else:
        traces_data = []

    result = []
    for trace in traces_data[: args.limit]:
        trace_info = {
            "trace_id": trace.get("traceID", "unknown"),
            "spans": len(trace.get("spans", [])),
            "start_time": trace.get("startTime", 0),
            "duration": trace.get("duration", 0),
        }
        services = set()
        for span in trace.get("spans", []):
            process_id = span.get("processID", "")
            process = trace.get("processes", {}).get(process_id, {})
            if process.get("serviceName"):
                services.add(process["serviceName"])
        trace_info["services"] = list(services)
        result.append(trace_info)

    return json.dumps({"traces": result}, ensure_ascii=False, indent=2)


async def traces_get(
    client: httpx.AsyncClient, settings: ObsSettings, args: TracesGetArgs
) -> str:
    """Fetch a specific trace by ID."""
    endpoint = f"{settings.victoriatraces_url}/select/jaeger/api/traces/{args.trace_id}"

    response = await client.get(endpoint, timeout=30.0)
    response.raise_for_status()

    data = response.json()

    if isinstance(data, dict):
        trace_data = data.get("data", [])
    elif isinstance(data, list):
        trace_data = data
    else:
        trace_data = []

    result = []
    for trace in trace_data if isinstance(trace_data, list) else [trace_data]:
        summary = {
            "trace_id": trace.get("traceID", "unknown"),
            "total_spans": len(trace.get("spans", [])),
            "duration_ms": trace.get("duration", 0) / 1000,
            "start_time": trace.get("startTime", 0),
            "spans_summary": [],
        }

        for span in trace.get("spans", [])[:20]:
            span_info = {
                "span_id": span.get("spanID", "unknown"),
                "operation": span.get("operationName", "unknown"),
                "duration_ms": span.get("duration", 0) / 1000,
                "tags_count": len(span.get("tags", [])),
            }
            for tag in span.get("tags", []):
                if tag.get("key") == "error" and tag.get("value"):
                    span_info["error"] = str(tag.get("value"))
            summary["spans_summary"].append(span_info)

        result.append(summary)

    return json.dumps({"trace": result}, ensure_ascii=False, indent=2)


def _text(data: str) -> list[TextContent]:
    return [TextContent(type="text", text=data)]


def create_server(settings: ObsSettings) -> Server:
    server = Server("mcp-obs")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [spec.as_tool() for spec in TOOL_SPECS]

    @server.call_tool()
    async def call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[TextContent]:
        spec = TOOLS_BY_NAME.get(name)
        if spec is None:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]

        async with httpx.AsyncClient() as http_client:
            try:
                args = spec.model.model_validate(arguments or {})
                if name == "logs_search":
                    result = await logs_search(http_client, settings, args)
                elif name == "logs_error_count":
                    result = await logs_error_count(http_client, settings, args)
                elif name == "traces_list":
                    result = await traces_list(http_client, settings, args)
                elif name == "traces_get":
                    result = await traces_get(http_client, settings, args)
                else:
                    result = json.dumps({"error": f"Unknown tool: {name}"})
                return _text(result)
            except Exception as exc:
                return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    _ = list_tools, call_tool
    return server


async def main() -> None:
    settings = resolve_settings()
    server = create_server(settings)
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
