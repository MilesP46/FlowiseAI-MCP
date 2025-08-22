# Dockerfile for Smithery.ai deployment
FROM python:3.12-slim

WORKDIR /app

# Copy all files to the container
COPY . .

# Install the package from local directory
RUN pip install --no-cache-dir .

# Expose the HTTP port for remote deployment
EXPOSE 8000

# Default to HTTP server for smithery.ai remote deployment
# Override with flowiseai-mcp for stdio if needed
CMD ["flowiseai-mcp-http"]