# Use Python 3.12 slim image for smaller size
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy project files first (for better caching)
COPY pyproject.toml ./
COPY README.md ./
COPY LICENSE ./

# Copy source code
COPY src/ ./src/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Create non-root user for security
RUN useradd -m -u 1000 mcp && \
    chown -R mcp:mcp /app

# Switch to non-root user
USER mcp

# Set environment variables (can be overridden)
ENV PYTHONUNBUFFERED=1
ENV FLOWISEAI_URL=http://localhost:3000
ENV FLOWISEAI_API_KEY=""

# Entry point for MCP server
ENTRYPOINT ["python", "-m", "flowiseai_mcp.server"]