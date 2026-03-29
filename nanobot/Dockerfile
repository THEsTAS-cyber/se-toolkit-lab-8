# Stage 1: Build
FROM ghcr.io/astral-sh/uv:python3.14-bookworm AS builder

WORKDIR /app/nanobot
COPY --chown=app:app config.json pyproject.toml entrypoint.py ./
COPY --chown=app:app workspace/ ./workspace/
# Copy from nanobot context
COPY --chown=app:app workspace/ ./workspace/
COPY --chown=app:app pyproject.toml entrypoint.py ./

# Generate lock and install base nanobot
RUN uv lock
RUN uv sync --frozen --no-dev

# Copy MCP packages from workspace context
COPY --from=workspace --chown=app:app /mcp/mcp-lms /tmp/mcp-lms
COPY --from=workspace --chown=app:app /mcp/mcp-obs /tmp/mcp-obs
COPY --from=workspace --chown=app:app /nanobot-websocket-channel/nanobot-webchat /tmp/nanobot-webchat
COPY --from=workspace --chown=app:app /nanobot-websocket-channel/mcp-webchat /tmp/mcp-webchat
COPY --from=workspace --chown=app:app /nanobot-websocket-channel/nanobot-channel-protocol /tmp/nanobot-channel-protocol

# Install build dependencies
RUN uv pip install --python /app/nanobot/.venv/bin/python setuptools wheel

# Remove workspace sources from pyproject.toml files
RUN sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/mcp-lms/pyproject.toml 2>/dev/null || true
RUN sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/mcp-obs/pyproject.toml 2>/dev/null || true
RUN sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/nanobot-channel-protocol/pyproject.toml 2>/dev/null || true
RUN sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/nanobot-webchat/pyproject.toml 2>/dev/null || true
RUN sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/mcp-webchat/pyproject.toml 2>/dev/null || true

# Install MCP packages in dependency order
RUN uv pip install --python /app/nanobot/.venv/bin/python -e /tmp/nanobot-channel-protocol
RUN uv pip install --python /app/nanobot/.venv/bin/python -e /tmp/mcp-lms
RUN uv pip install --python /app/nanobot/.venv/bin/python -e /tmp/mcp-obs
RUN uv pip install --python /app/nanobot/.venv/bin/python -e /tmp/mcp-webchat
RUN uv pip install --python /app/nanobot/.venv/bin/python -e /tmp/nanobot-webchat

# Stage 2: Runtime
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

ARG APP_UID=1000
ARG APP_GID=1000

RUN groupadd --gid $APP_GID app && \
    useradd --uid $APP_UID --gid $APP_GID --shell /bin/bash --create-home app

WORKDIR /app/nanobot

# Copy from builder
COPY --from=builder --chown=app:app /app/nanobot/.venv /app/nanobot/.venv
COPY --from=builder --chown=app:app /app/nanobot/workspace /app/nanobot/workspace
COPY --from=builder --chown=app:app /app/nanobot/entrypoint.py /app/nanobot/entrypoint.py
COPY --from=builder --chown=app:app /app/nanobot/pyproject.toml /app/nanobot/pyproject.toml

ENV PATH="/app/nanobot/.venv/bin:$PATH"

USER app

CMD ["python", "/app/nanobot/entrypoint.py"]
