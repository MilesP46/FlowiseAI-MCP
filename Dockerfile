# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only requirements first for better caching
COPY requirements.txt ./

# Install dependencies directly from requirements.txt (faster)
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Set Python path
ENV PYTHONPATH=/app

# MCP servers need unbuffered output for stdio
ENV PYTHONUNBUFFERED=1

# Run the MCP server
CMD ["python", "-m", "flowiseai_mcp.server"]