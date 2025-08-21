# Minimal Dockerfile for Smithery MCP server
FROM python:3.12-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code with correct structure
COPY src/flowiseai_mcp ./flowiseai_mcp

# MCP servers communicate via stdio
ENV PYTHONUNBUFFERED=1

# Run the MCP server
CMD ["python", "-m", "flowiseai_mcp.server"]