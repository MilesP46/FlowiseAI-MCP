# FlowiseAI MCP Server

A comprehensive Model Context Protocol (MCP) server for FlowiseAI that provides complete API coverage for automating and managing FlowiseAI chatflows, assistants, and AgentFlow V2.

## Features

### Complete FlowiseAI API Coverage

- **Assistants** - Full CRUD operations for AI assistants
- **Chatflows** - Create, manage, and deploy chatflows with public/private settings
- **Predictions** - Execute flows with streaming, forms (AgentFlow V2), and human-in-the-loop support
- **Document Store** - Complete RAG lifecycle management with vector operations
- **Chat Management** - Messages, attachments, feedback, and leads
- **Custom Tools** - Create and manage custom tools with schemas
- **Variables** - Runtime variable management for dynamic flows
- **Session Control** - Full session and memory management
- **File Uploads** - Support for images, audio, and documents

### Advanced Capabilities

- ✅ **Streaming Predictions** - Real-time SSE/WebSocket responses
- ✅ **AgentFlow V2** - Full form input support with Start Node integration
- ✅ **Human-in-the-Loop** - Resume flows with human approval/feedback
- ✅ **Multi-Agent Support** - Nested agents and Chatflow Tool nodes
- ✅ **RAG Operations** - Document store, vector upsert, chunk management
- ✅ **Dynamic Configuration** - Override configs, variables, temperature, max tokens
- ✅ **Upload Pipeline** - Base64 and URL uploads for multimedia content
- ✅ **Session Continuity** - Thread management across multiple calls

## Installation

### Using uvx (Recommended)

```bash
# Install directly from GitHub
uvx --from git+https://github.com/MilesP46/FlowiseAI-MCP.git flowiseai-mcp

# Or install from PyPI (when published)
uvx flowiseai-mcp
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/MilesP46/FlowiseAI-MCP.git
cd FlowiseAI-MCP

# Install with pip
pip install -e .
```

## Configuration

The server requires only two environment variables:

```bash
# FlowiseAI instance URL (supports localhost, network, or cloud)
export FLOWISEAI_URL="http://localhost:3000"  # Default
# or
export FLOWISEAI_URL="https://your-flowise-instance.com"

# API Key for authentication
export FLOWISEAI_API_KEY="your-api-key-here"
```

You can also create a `.env` file in your working directory:

```env
FLOWISEAI_URL=https://your-flowise-instance.com
FLOWISEAI_API_KEY=your-api-key-here
```

The server automatically handles:
- URL normalization (localhost, network, cloud deployments)
- Dynamic port assignment
- API versioning

## Usage

### Claude Desktop

1. Update your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "flowiseai": {
      "command": "uvx",
      "args": ["flowiseai-mcp"],
      "env": {
        "FLOWISEAI_URL": "http://localhost:3000",
        "FLOWISEAI_API_KEY": "your-api-key"
      }
    }
  }
}
```

2. Restart Claude Desktop
3. The FlowiseAI tools will appear in the tools panel

### Claude Code CLI

1. Install Claude Code CLI:
```bash
npm install -g @anthropic/claude-code
```

2. Configure MCP servers in your project:

Create `.claude/mcp_servers.json`:
```json
{
  "flowiseai": {
    "command": "uvx",
    "args": ["flowiseai-mcp"],
    "env": {
      "FLOWISEAI_URL": "http://localhost:3000",
      "FLOWISEAI_API_KEY": "your-api-key"
    }
  }
}
```

3. Run Claude Code:
```bash
claude-code
```

### Smithery.ai Deployment

This MCP server is ready for deployment to [Smithery.ai](https://smithery.ai/):

1. Fork this repository to your GitHub account

2. Go to [Smithery.ai](https://smithery.ai/) and sign in

3. Click "New Server" and select your forked repository

4. Configure the server:
   - Name: `FlowiseAI MCP`
   - Command: `uvx flowiseai-mcp`
   - Environment Variables:
     - `FLOWISEAI_URL`: Your FlowiseAI instance URL
     - `FLOWISEAI_API_KEY`: Your API key

5. Deploy the server

6. Use the provided connection details in your AI tools

## Available Tools

### Assistant Management
- `assistant_create` - Create new assistant
- `assistant_list` - List all assistants
- `assistant_get` - Get assistant by ID
- `assistant_update` - Update assistant
- `assistant_delete` - Delete assistant

### Chatflow Operations
- `chatflow_create` - Create new chatflow
- `chatflow_list` - List all chatflows
- `chatflow_get` - Get chatflow by ID
- `chatflow_get_by_apikey` - Get chatflow by API key
- `chatflow_update` - Update chatflow (flowData, deployed, isPublic)
- `chatflow_delete` - Delete chatflow

### Predictions & Execution
- `prediction_run` - Execute prediction with full options
- `prediction_stream` - Execute streaming prediction

### Chat Management
- `chatmessage_list` - List messages with filters
- `chatmessage_delete_all` - Delete all messages
- `attachment_create` - Create attachments
- `feedback_create/list/update` - Manage feedback
- `lead_create/list` - Manage leads

### Custom Tools & Variables
- `tool_create/list/get/update/delete` - Manage custom tools
- `variable_create/list/update/delete` - Manage runtime variables

### Document Store & RAG
- `docstore_create/list/get/update/delete` - Manage document stores
- `docstore_upsert` - Upsert documents
- `docstore_refresh` - Refresh store
- `docstore_get_chunks` - Get document chunks
- `docstore_update_chunk` - Update chunk
- `docstore_delete_chunk` - Delete chunk
- `docstore_delete_loader` - Delete loader and chunks
- `vector_upsert` - Upsert to vector store

### History & Health
- `upsert_history_list` - List upsert history
- `upsert_history_delete` - Delete history records
- `ping` - Health check

## Example Usage

### Create and Run a Chatflow

```python
# Create a new chatflow
chatflow = await call_tool("chatflow_create", {
    "name": "Customer Support Bot",
    "flowData": {...},  # Your flow configuration
    "deployed": True,
    "isPublic": False
})

# Run a prediction
response = await call_tool("prediction_run", {
    "chatflow_id": chatflow["id"],
    "question": "How can I help you today?",
    "streaming": True,
    "overrideConfig": {
        "sessionId": "user-123",
        "temperature": 0.7
    }
})
```

### AgentFlow V2 with Forms

```python
# Execute AgentFlow V2 with form inputs
response = await call_tool("prediction_run", {
    "chatflow_id": "agentflow-id",
    "form": {
        "customerName": "John Doe",
        "orderNumber": "12345",
        "issueType": "shipping"
    },
    "sessionId": "session-456"
})
```

### Document Store Operations

```python
# Create document store
store = await call_tool("docstore_create", {
    "name": "Knowledge Base",
    "description": "Company documentation"
})

# Upsert documents
await call_tool("docstore_upsert", {
    "store_id": store["id"],
    "documents": [
        {"content": "...", "metadata": {...}}
    ]
})

# Refresh store
await call_tool("docstore_refresh", {
    "store_id": store["id"]
})
```

### Human-in-the-Loop

```python
# Resume flow with human input
response = await call_tool("prediction_run", {
    "chatflow_id": "flow-id",
    "humanInput": "approved",
    "chatId": "existing-chat-id"
})
```

## Development

### Local Development

```bash
# Clone the repository
git clone https://github.com/MilesP46/FlowiseAI-MCP.git
cd FlowiseAI-MCP

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black src/
ruff check src/
```

### Testing

```bash
# Run the server locally
python -m flowiseai_mcp.server

# Test with MCP client
mcp-client test localhost:PORT
```

## Architecture

The server follows a modular architecture:

```
src/flowiseai_mcp/
├── __init__.py          # Package initialization
├── server.py            # MCP server implementation
├── client.py            # FlowiseAI API client
└── models.py            # Pydantic data models
```

- **Server Layer**: Handles MCP protocol and tool definitions
- **Client Layer**: Manages FlowiseAI API interactions
- **Model Layer**: Provides data validation and serialization

## Error Handling

The server implements comprehensive error handling:

- Connection errors are logged and returned as tool errors
- Invalid inputs are validated using Pydantic models
- API errors are caught and returned with descriptive messages
- Streaming errors are handled gracefully

## Security

- API keys are never logged or exposed
- All connections use HTTPS when available
- Input validation prevents injection attacks
- Follows FlowiseAI security best practices

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

- GitHub Issues: [https://github.com/MilesP46/FlowiseAI-MCP/issues](https://github.com/MilesP46/FlowiseAI-MCP/issues)
- FlowiseAI Documentation: [https://docs.flowiseai.com/](https://docs.flowiseai.com/)
- MCP Documentation: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)

## Acknowledgments

- FlowiseAI team for the excellent platform
- Anthropic for the MCP specification
- Community contributors