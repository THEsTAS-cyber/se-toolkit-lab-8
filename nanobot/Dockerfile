В Task 2 нужно:

Создать Docker-образ nanobot (вместо запуска через uv run)
Добавить WebSocket канал для веб-клиента
Запустить Flutter веб-клиент для чата
План для Part A:

Сначала завершите Task 1 — оформите REPORT.md с ответами из Part A, B, C.

Затем для Task 2 создайте файлы:

1. nanobot/entrypoint.py — скрипт, который читает config.json, подставляет env vars и запускает nanobot gateway:

#!/usr/bin/env python3
"""Resolve environment variables into config and launch nanobot gateway."""

import json
import os
import sys
from pathlib import Path

def main():
    config_path = Path("/app/nanobot/config.json")
    resolved_path = Path("/app/nanobot/config.resolved.json")
    workspace_path = Path("/app/nanobot/workspace")
    
    # Load config
    with open(config_path) as f:
        config = json.load(f)
    
    # Override from env vars
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
    
    # Write resolved config
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)
    
    # Launch nanobot gateway
    os.execvp("nanobot", [
        "nanobot", "gateway",
        "--config", str(resolved_path),
        "--workspace", str(workspace_path)
    ])

if __name__ == "__main__":
    main()
2. nanobot/Dockerfile — multi-stage build:

# Stage 1: Build
FROM ghcr.io/astral-sh/uv:python3.14-bookworm AS builder

WORKDIR /app

# Copy workspace first (changes often)
COPY --chown=app:app workspace/ ./workspace/

# Copy project files
COPY --chown=app:app pyproject.toml uv.lock ./
COPY --chown=app:app entrypoint.py ./nanobot/

# Install dependencies
RUN uv sync --frozen --no-dev

# Stage 2: Runtime
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ARG APP_UID=1000
ARG APP_GID=1000

RUN groupadd --gid $APP_GID app && \
    useradd --uid $APP_UID --gid $APP_GID --shell /bin/bash --create-home app

WORKDIR /app

# Copy from builder
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/workspace /app/nanobot/workspace
COPY --from=builder --chown=app:app /app/entrypoint.py /app/nanobot/entrypoint.py
COPY --from=builder --chown=app:app /app/pyproject.toml /app/nanobot/
COPY --from=builder --chown=app:app /app/uv.lock /app/nanobot/

ENV PATH="/app/.venv/bin:$PATH"

USER app

CMD ["python", "/app/nanobot/entrypoint.py"]
