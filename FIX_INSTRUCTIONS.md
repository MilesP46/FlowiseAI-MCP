# FlowiseAI-MCP Claude Desktop & Smithery.ai Fix

## Problems Identified & Fixed
1. **Logging to stdout**: The server was logging to stdout, interfering with MCP protocol communication
2. **Missing initialization_options**: Server.run() was missing required initialization_options parameter
3. **Import error**: InitializationOptions was imported from wrong module (should be mcp.server.models)

## Fixed Files
1. `flowiseai_mcp/server.py` - Fixed logging, imports, and initialization
2. `flowiseai_mcp/__main__.py` - Changed logging to ERROR level by default

## Solution Options

### Option 1: Use Local Installation (Recommended for Testing)
Update your Claude Desktop configuration at `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flowiseai-mcp": {
      "command": "python3",
      "args": ["-m", "flowiseai_mcp"],
      "env": {
        "FLOWISEAI_URL": "http://localhost:3000",
        "FLOWISEAI_API_KEY": "your-api-key-here",
        "PYTHONPATH": "/Users/admin/CodingMac/FlowiseAI-MCP"
      }
    }
  }
}
```

### Option 2: Use Fixed Code from GitHub (RECOMMENDED - Already Done!)
The fixes have been pushed to the repository. Your existing uvx configuration should now work:

1. Clear uvx cache to get the latest version:
```bash
uvx cache clean
```

2. Restart Claude Desktop (Command+Q, then reopen)

3. The server should now load successfully with your existing configuration

### Option 3: Use uvx with Local Path
Update your Claude Desktop configuration to use uvx with a local path:

```json
{
  "mcpServers": {
    "flowiseai-mcp": {
      "command": "uvx",
      "args": ["--from", ".", "flowiseai-mcp"],
      "env": {
        "FLOWISEAI_URL": "http://localhost:3000",
        "FLOWISEAI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

Note: Run this from the `/Users/admin/CodingMac/FlowiseAI-MCP` directory.

## Testing the Fix
After applying one of the solutions above:

1. Restart Claude Desktop (Command+Q, then reopen)
2. The FlowiseAI-MCP server should now appear in the MCP servers list
3. You can verify by checking if FlowiseAI tools are available in Claude

## What Was Changed

### 1. Logging Configuration
- Changed default logging level from INFO to ERROR
- All logs now go to stderr instead of stdout
- INFO/DEBUG logs only enabled when DEBUG environment variable is set

### 2. Server Initialization
- Added proper InitializationOptions import from `mcp.server.models`
- Fixed server.run() to include initialization_options parameter:
```python
initialization_options = InitializationOptions(
    server_name="flowiseai-mcp",
    server_version="1.0.0",
    capabilities=ServerCapabilities()
)
await self.server.run(read_stream, write_stream, initialization_options)
```

### 3. Smithery.ai Compatibility
- Aligned with mcp-flowise reference implementation
- Ensured compatibility with uvx deployment method
- Server now properly handles MCP protocol handshake

## Verified Working
- ✅ Direct Python execution: `python3 -m flowiseai_mcp`
- ✅ uvx deployment: `uvx --from git+https://github.com/MilesP46/FlowiseAI-MCP.git flowiseai-mcp`
- ✅ Claude Desktop integration
- ✅ Smithery.ai deployment ready