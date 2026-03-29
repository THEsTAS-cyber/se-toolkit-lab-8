# Simplified Dockerfile for nanobot
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app/nanobot

# Copy config and code
COPY config.json pyproject.toml entrypoint.py ./
COPY workspace/ ./workspace/

# Create virtual environment and install base nanobot
RUN uv venv && \
    uv pip install "nanobot-ai @ https://github.com/HKUDS/nanobot/archive/e7d371ec1e6531b28898ec2c869ef338e8dd46ec.zip"

# Copy MCP packages from workspace context
COPY --from=workspace /mcp/mcp-lms /tmp/mcp-lms
COPY --from=workspace /mcp/mcp-obs /tmp/mcp-obs
COPY --from=workspace /nanobot-websocket-channel/nanobot-channel-protocol /tmp/nanobot-channel-protocol
COPY --from=workspace /nanobot-websocket-channel/mcp-webchat /tmp/mcp-webchat
COPY --from=workspace /nanobot-websocket-channel/nanobot-webchat /tmp/nanobot-webchat

# Remove workspace sources from pyproject.toml files to allow installation
RUN sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/mcp-lms/pyproject.toml 2>/dev/null || true && \
    sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/mcp-obs/pyproject.toml 2>/dev/null || true && \
    sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/nanobot-channel-protocol/pyproject.toml 2>/dev/null || true && \
    sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/mcp-webchat/pyproject.toml 2>/dev/null || true && \
    sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/nanobot-webchat/pyproject.toml 2>/dev/null || true

# Install MCP packages in dependency order
RUN uv pip install -e /tmp/nanobot-channel-protocol && \
    uv pip install -e /tmp/mcp-lms && \
    uv pip install -e /tmp/mcp-obs && \
    uv pip install -e /tmp/mcp-webchat && \
    uv pip install -e /tmp/nanobot-webchat

CMD ["python", "/app/nanobot/entrypoint.py"]
