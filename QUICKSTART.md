# FlowiseAI MCP Server - Quick Start Guide

## 🚀 Fastest Way to Get Started

### 1. Install uvx
```bash
pip install uvx
```

### 2. Run from This Directory
```bash
# Set your FlowiseAI credentials
export FLOWISEAI_URL="http://localhost:3000"
export FLOWISEAI_API_KEY="your-api-key"

# Run the MCP server
uvx --from . flowiseai-mcp
```

### 3. Configure Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "flowiseai": {
      "command": "uvx",
      "args": ["--from", "/absolute/path/to/FlowiseAI-MCP", "flowiseai-mcp"],
      "env": {
        "FLOWISEAI_URL": "http://localhost:3000",
        "FLOWISEAI_API_KEY": "your-api-key"
      }
    }
  }
}
```

### 4. Restart Claude Desktop

The FlowiseAI tools will appear in the tools panel (🔧 icon).

## 📋 Test Your Setup

```bash
# Run the test script
./test_uvx_local.sh

# Or test manually
uvx --from . flowiseai-mcp
```

## 🎯 Using the Tools in Claude

Once configured, you can use commands like:
- "List all my chatflows"
- "Create a new assistant"
- "Run a prediction on chatflow XYZ"
- "Upload documents to the RAG store"
- "Get feedback from users"

## 🔧 Troubleshooting

If tools don't appear:
1. Check FlowiseAI is running: `curl http://localhost:3000/api/v1/ping`
2. Verify API key is correct
3. Restart Claude Desktop completely
4. Check logs in Claude's developer console

## 📚 Full Documentation

See [README.md](README.md) for complete documentation and all configuration options.