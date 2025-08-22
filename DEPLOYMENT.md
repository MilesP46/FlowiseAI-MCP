# Deployment Guide

This MCP server supports two deployment modes to accommodate different use cases:

## Local Deployment (stdio transport)

**Command:** `flowiseai-mcp`  
**Transport:** stdio  
**Use Case:** Local installation with Claude Desktop via uvx  

The stdio transport is ideal for local usage where the MCP client (Claude Desktop) spawns the server as a subprocess. This provides:
- Direct process communication
- Lower latency
- Simple configuration
- No network exposure

Install locally with:
```bash
uvx --from git+https://github.com/MilesP46/FlowiseAI-MCP.git flowiseai-mcp
```

## Remote Deployment (Streamable HTTP transport)

**Configuration:** `smithery.yaml`  
**Transport:** Streamable HTTP  
**Use Case:** Smithery.ai hosted deployment  

The Streamable HTTP transport enables remote deployment on platforms like Smithery.ai, providing:
- Network accessibility  
- Multiple concurrent clients
- Health check endpoints
- Scalable deployment
- MCP protocol over HTTP

### HTTP Endpoints

When running in HTTP mode (`flowiseai-mcp-http`):
- `/health` - Health check endpoint
- `/mcp` - MCP endpoint for Streamable HTTP protocol
- `/` - Root health check

### Environment Variables

Both modes support:
- `FLOWISEAI_API_KEY` - Your FlowiseAI API key (required)
- `FLOWISEAI_URL` - FlowiseAI instance URL (default: http://localhost:3000)

HTTP mode additional variables:
- `PORT` - HTTP server port (default: 8000)
- `HOST` - HTTP server host (default: 0.0.0.0)
- `DEBUG` - Enable debug logging (set to 'true', '1', or 'yes')

## Docker Deployment

The included Dockerfile supports both modes:
- Default: `flowiseai-mcp-http` for remote deployment
- Override with `flowiseai-mcp` for stdio if needed

```bash
# Build the Docker image
docker build -t flowiseai-mcp .

# Run with HTTP transport (for Smithery.ai)
docker run -p 8000:8000 -e FLOWISEAI_API_KEY=your-key flowiseai-mcp

# Run with stdio transport (for local testing)
docker run -i -e FLOWISEAI_API_KEY=your-key flowiseai-mcp flowiseai-mcp
```

## Test Mode

The server includes a test mode that activates when:
- `FLOWISEAI_API_KEY` is not set, or
- `FLOWISEAI_API_KEY` is set to "test-key"

In test mode:
- The `ping` tool returns "pong (test mode)" without requiring a FlowiseAI connection
- Other tools return a helpful message about test mode
- This allows deployment platforms to validate the server without a live FlowiseAI instance