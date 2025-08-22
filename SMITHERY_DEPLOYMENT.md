# FlowiseAI-MCP Smithery.ai Deployment Guide

## Status
- ✅ Docker build successful
- ✅ Server starts successfully
- ✅ Local Claude Desktop integration working
- ⚠️ Smithery.ai connectivity scan failing
- ⚠️ CLI installation needs fixing

## Installation Methods

### Method 1: Direct from GitHub (Currently Working Locally)
```json
{
  "flowiseai": {
    "command": "uvx",
    "args": ["--from", "git+https://github.com/MilesP46/FlowiseAI-MCP.git", "flowiseai-mcp"],
    "env": {
      "FLOWISEAI_URL": "http://localhost:3000",
      "FLOWISEAI_API_KEY": "your-api-key-here"
    }
  }
}
```

### Method 2: Via Smithery CLI (After Fix)
```bash
npx -y @smithery/cli install @MilesP46/flowiseai-mcp --client claude
```

## Configuration

The server requires the following environment variables:
- `FLOWISEAI_API_KEY` (required): Your FlowiseAI API key
- `FLOWISEAI_URL` (optional): FlowiseAI instance URL (defaults to http://localhost:3000)

## Known Issues

1. **Smithery.ai Scan Failure**: The deployment builds successfully but fails the connectivity scan. This might be because:
   - The server expects actual FlowiseAI credentials to initialize
   - The test configuration needs adjustment

2. **CLI Installation Error**: The smithery CLI fails with a validation error about the "remote" field. Fixed by adding `remote: false` to smithery.yaml.

## Files

- `smithery.yaml`: Smithery deployment configuration
- `Dockerfile`: Container build configuration
- `pyproject.toml`: Python package configuration
- `flowiseai_mcp/server.py`: Main server implementation

## Testing

To test the server locally:
```bash
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "2024-11-05", "clientInfo": {"name": "test", "version": "1.0.0"}, "capabilities": {}}, "id": 1}' | python3 -m flowiseai_mcp
```

Expected response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "serverInfo": {
      "name": "flowiseai-mcp",
      "version": "1.0.0"
    }
  }
}
```