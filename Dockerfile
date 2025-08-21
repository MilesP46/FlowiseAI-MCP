# Simple Dockerfile for local testing (not used by Smithery)
FROM python:3.12-slim

WORKDIR /app

# Install package directly from GitHub
RUN pip install git+https://github.com/MilesP46/FlowiseAI-MCP.git

# Run the MCP server
CMD ["flowiseai-mcp"]