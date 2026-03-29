#!/usr/bin/env python3
"""Resolve environment variables into config and launch nanobot gateway."""

import json
import os
from pathlib import Path

def main():
    config_path = Path("/app/nanobot/config.json")
    resolved_path = Path("/tmp/config.resolved.json")
    workspace_path = Path("/app/nanobot/workspace")

    with open(config_path) as f:
        config = json.load(f)

    if llm_key := os.environ.get("LLM_API_KEY"):
        config["providers"]["custom"]["apiKey"] = llm_key
    if llm_base := os.environ.get("LLM_API_BASE_URL"):
        config["providers"]["custom"]["apiBase"] = llm_base
    if llm_model := os.environ.get("LLM_API_MODEL"):
        config["agents"]["defaults"]["model"] = llm_model
    if gateway_host := os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config["gateway"]["host"] = gateway_host
    if gateway_port := os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config["gateway"]["port"] = int(gateway_port)
    if lms_url := os.environ.get("NANOBOT_LMS_BACKEND_URL"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_url
    if lms_key := os.environ.get("NANOBOT_LMS_API_KEY"):
        config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_key
    
    # Observability - create if not exists
    if obs_logs_url := os.environ.get("NANOBOT_VICTORIALOGS_URL"):
        if "obs" not in config["tools"]["mcpServers"]:
            config["tools"]["mcpServers"]["obs"] = {"command": "python", "args": ["-m", "mcp_obs"], "env": {}}
        config["tools"]["mcpServers"]["obs"]["env"]["VICTORIALOGS_URL"] = obs_logs_url
    if obs_traces_url := os.environ.get("NANOBOT_VICTORIATRACES_URL"):
        if "obs" not in config["tools"]["mcpServers"]:
            config["tools"]["mcpServers"]["obs"] = {"command": "python", "args": ["-m", "mcp_obs"], "env": {}}
        config["tools"]["mcpServers"]["obs"]["env"]["VICTORIATRACES_URL"] = obs_traces_url

    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)

    nanobot_bin = "/app/nanobot/.venv/bin/nanobot"
    os.execv(nanobot_bin, [nanobot_bin, "gateway", "--config", str(resolved_path), "--workspace", str(workspace_path)])

if __name__ == "__main__":
    main()
