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

uvx is a tool for running Python packages in isolated environments. Install it first:

```bash
# Install uvx if you haven't already
pip install uvx
# or
pipx install uvx
```

#### Run from GitHub (Easiest)
```bash
# Run directly from GitHub repository
uvx --from git+https://github.com/MilesP46/FlowiseAI-MCP.git flowiseai-mcp
```

#### Run from Local Directory
```bash
# Clone the repository
git clone https://github.com/MilesP46/FlowiseAI-MCP.git
cd FlowiseAI-MCP

# Run with uvx from local directory
uvx --from . flowiseai-mcp
```

#### Test Local Installation
```bash
# Verify uvx can build and run the package
./test_uvx_local.sh
```

### Using Python Module Directly

```bash
# Clone the repository
git clone https://github.com/MilesP46/FlowiseAI-MCP.git
cd FlowiseAI-MCP

# Run as Python module
PYTHONPATH=src python3 -m flowiseai_mcp
```

### Development Installation

```bash
# Clone the repository
git clone https://github.com/MilesP46/FlowiseAI-MCP.git
cd FlowiseAI-MCP

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e .

# Run the server
flowiseai-mcp
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

### Running Locally vs Remote

The MCP server can connect to FlowiseAI instances running in different locations:

#### Local FlowiseAI Instance
```bash
# For local development (default)
export FLOWISEAI_URL="http://localhost:3000"
export FLOWISEAI_API_KEY="your-local-api-key"
```

#### Network FlowiseAI Instance
```bash
# For network/LAN instances
export FLOWISEAI_URL="http://192.168.1.100:3000"
export FLOWISEAI_API_KEY="your-network-api-key"
```

#### Cloud FlowiseAI Instance
```bash
# For cloud-hosted instances
export FLOWISEAI_URL="https://your-flowise.example.com"
export FLOWISEAI_API_KEY="your-cloud-api-key"
```

### Claude Desktop

Configuration varies based on how you're running the MCP server:

#### Option 1: Using uvx from Local Directory
For local development and testing:
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "flowiseai": {
      "command": "uvx",
      "args": ["--from", "/path/to/FlowiseAI-MCP", "flowiseai-mcp"],
      "env": {
        "FLOWISEAI_URL": "http://localhost:3000",
        "FLOWISEAI_API_KEY": "your-api-key"
      }
    }
  }
}
```

#### Option 2: Using uvx from GitHub (Recommended for Production)
For stable usage without local files:

```json
{
  "mcpServers": {
    "flowiseai": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/MilesP46/FlowiseAI-MCP.git", "flowiseai-mcp"],
      "env": {
        "FLOWISEAI_URL": "http://localhost:3000",
        "FLOWISEAI_API_KEY": "your-api-key"
      }
    }
  }
}
```

#### Option 3: Running Python Module Directly
For development without uvx:

```json
{
  "mcpServers": {
    "flowiseai": {
      "command": "python",
      "args": ["-m", "flowiseai_mcp.server"],
      "cwd": "/path/to/FlowiseAI-MCP",
      "env": {
        "PYTHONPATH": "/path/to/FlowiseAI-MCP/src",
        "FLOWISEAI_URL": "http://localhost:3000",
        "FLOWISEAI_API_KEY": "your-api-key"
      }
    }
  }
}
```

#### Option 4: Using Virtual Environment
For isolated Python environment:

```json
{
  "mcpServers": {
    "flowiseai": {
      "command": "/path/to/venv/bin/python",
      "args": ["-m", "flowiseai_mcp.server"],
      "cwd": "/path/to/FlowiseAI-MCP",
      "env": {
        "FLOWISEAI_URL": "http://localhost:3000",
        "FLOWISEAI_API_KEY": "your-api-key"
      }
    }
  }
}
```

After updating configuration:
1. Save the file
2. Restart Claude Desktop completely
3. Look for "flowiseai" in the tools panel (🔧 icon)
4. Test with the `ping` tool to verify connection

### Claude Code CLI

#### Option 1: Global Installation
Install globally and configure:

```bash
# Install Claude Code CLI
npm install -g @anthropic/claude-code

# Install MCP server globally
uvx --from git+https://github.com/MilesP46/FlowiseAI-MCP.git flowiseai-mcp
```

Create `.claude/mcp_servers.json` in your project:
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

#### Option 2: Local Development
For testing local changes:

```json
{
  "flowiseai": {
    "command": "python3",
    "args": ["-m", "flowiseai_mcp.server"],
    "cwd": "/absolute/path/to/FlowiseAI-MCP",
    "env": {
      "PYTHONPATH": "/absolute/path/to/FlowiseAI-MCP/src",
      "FLOWISEAI_URL": "http://localhost:3000",
      "FLOWISEAI_API_KEY": "your-api-key"
    }
  }
}
```

#### Option 3: Using .env File
Create `.env` in your project root:
```env
FLOWISEAI_URL=http://localhost:3000
FLOWISEAI_API_KEY=your-api-key
```

Then in `.claude/mcp_servers.json`:
```json
{
  "flowiseai": {
    "command": "uvx",
    "args": ["flowiseai-mcp"]
  }
}
```

Run Claude Code:
```bash
# From your project directory
claude-code
```

### Troubleshooting

#### Verify Installation
```bash
# Test the server directly
python -m flowiseai_mcp.server

# Or with uvx
uvx flowiseai-mcp
```

#### Check Connection
1. Ensure FlowiseAI is running and accessible
2. Verify the URL format (http/https, port number)
3. Test API key validity
4. Check firewall/network settings for remote instances

#### Common Issues

**"Server not found"**: 
- Ensure the command path is correct
- Check Python/uvx is in PATH
- Verify the cwd directory exists

**"Connection refused"**:
- Check FlowiseAI is running
- Verify URL and port are correct
- Check firewall settings

**"Authentication failed"**:
- Verify API key is correct
- Check API key permissions in FlowiseAI

**"Tools not appearing"**:
- Restart Claude Desktop/CLI completely
- Check configuration file syntax
- Look for errors in Claude's developer console

### Smithery.ai Deployment

This MCP server is fully configured for deployment to [Smithery.ai](https://smithery.ai/) with Docker:

#### Prerequisites
The repository includes all required files:
- ✅ `Dockerfile` - Multi-stage Python build
- ✅ `smithery.yaml` - Smithery configuration
- ✅ `.dockerignore` - Optimized build context

#### Deployment Steps

1. **Fork or Push this repository** to your GitHub account

2. **Go to [Smithery.ai](https://smithery.ai/)** and sign in

3. **Create New Server**:
   - Click "New Server"
   - Select your repository
   - Smithery will automatically detect the configuration files

4. **Configure Environment Variables**:
   - `FLOWISEAI_URL`: Your FlowiseAI instance URL
   - `FLOWISEAI_API_KEY`: Your API key

5. **Deploy**:
   - Click "Deploy"
   - Smithery will build the Docker image and start your server

6. **Connect to your AI tools**:
   - Use the provided MCP connection details
   - Add to Claude Desktop, Claude CLI, or other MCP-compatible tools

#### Testing Before Deployment

```bash
# Test Docker build locally
./test_docker_build.sh

# Or manually:
docker build -t flowiseai-mcp .
docker run --rm -e FLOWISEAI_URL=http://localhost:3000 -e FLOWISEAI_API_KEY=test flowiseai-mcp
```

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