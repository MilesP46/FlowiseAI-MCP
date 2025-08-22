# FlowiseAI-MCP Claude Desktop Fix

## Problem Identified
The FlowiseAI-MCP server was logging to stdout, which interferes with the MCP protocol communication that also uses stdout. This causes the server to fail when Claude Desktop tries to initialize it.

## Fixed Files
1. `flowiseai_mcp/server.py` - Redirected logging to stderr
2. `flowiseai_mcp/__main__.py` - Redirected logging to stderr

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

### Option 2: Push Fixed Code to Your Fork
1. Commit the changes:
```bash
git add flowiseai_mcp/__main__.py flowiseai_mcp/server.py
git commit -m "Fix: Redirect logging to stderr to prevent MCP protocol interference"
```

2. Push to your fork:
```bash
git push origin main
```

3. Keep your existing uvx configuration in Claude Desktop

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
The logging configuration was changed from:
```python
logging.basicConfig(level=logging.INFO)
```

To:
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
```

This ensures all log output goes to stderr, leaving stdout clean for MCP protocol communication.