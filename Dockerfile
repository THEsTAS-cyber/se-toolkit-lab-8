# Stage 1: Build
FROM ghcr.io/astral-sh/uv:python3.14-bookworm AS builder

WORKDIR /app/nanobot

# Copy from nanobot context
COPY --chown=app:app workspace/ ./workspace/
COPY --chown=app:app pyproject.toml entrypoint.py ./

# Generate lock file inside container
RUN uv lock

# Install base nanobot
RUN uv sync --frozen --no-dev

# Install MCP packages - copy them first, then install
COPY --from=workspace --chown=app:app /mcp/mcp-lms /tmp/mcp-lms
COPY --from=workspace --chown=app:app /nanobot-websocket-channel/nanobot-webchat /tmp/nanobot-webchat
COPY --from=workspace --chown=app:app /nanobot-websocket-channel/mcp-webchat /tmp/mcp-webchat

RUN uv add mcp-lms --editable /tmp/mcp-lms
RUN uv add nanobot-webchat --editable /tmp/nanobot-webchat
RUN uv add mcp-webchat --editable /tmp/mcp-webchat

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
