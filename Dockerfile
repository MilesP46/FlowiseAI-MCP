# Minimal Dockerfile for Smithery.ai deployment
FROM python:3.12-slim

WORKDIR /app

# Copy all files to the container
COPY . .

# Install the package from local directory
RUN pip install --no-cache-dir .

# The MCP server will be started via smithery.yaml's startCommand
# This CMD is just a placeholder that Smithery will override
CMD ["flowiseai-mcp"]