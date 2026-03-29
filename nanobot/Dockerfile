FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app/nanobot
COPY config.json pyproject.toml entrypoint.py ./
COPY workspace/ ./workspace/

RUN uv venv

COPY --from=workspace /mcp/mcp-lms /tmp/mcp-lms
COPY --from=workspace /mcp/mcp-obs /tmp/mcp-obs
COPY --from=workspace /nanobot-websocket-channel/nanobot-channel-protocol /tmp/nanobot-channel-protocol
COPY --from=workspace /nanobot-websocket-channel/mcp-webchat /tmp/mcp-webchat
COPY --from=workspace /nanobot-websocket-channel/nanobot-webchat /tmp/nanobot-webchat

# Remove workspace sources from all MCP packages
RUN sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/mcp-lms/pyproject.toml && \
    sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/mcp-obs/pyproject.toml && \
    sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/nanobot-channel-protocol/pyproject.toml && \
    sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/mcp-webchat/pyproject.toml && \
    sed -i '/\[tool.uv.sources\]/,/^\[/d' /tmp/nanobot-webchat/pyproject.toml

# Install in dependency order
RUN uv pip install -e /tmp/nanobot-channel-protocol && \
    uv pip install -e /tmp/mcp-lms && \
    uv pip install -e /tmp/mcp-obs && \
    uv pip install -e /tmp/mcp-webchat && \
    uv pip install -e /tmp/nanobot-webchat

RUN uv pip install mcp httpx "nanobot-ai @ https://github.com/HKUDS/nanobot/archive/e7d371ec1e6531b28898ec2c869ef338e8dd46ec.zip"

CMD ["python", "/app/nanobot/entrypoint.py"]
