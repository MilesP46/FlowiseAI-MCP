# FlowiseAI MCP Server - Tools Reference

## Complete Tool Listing (46 Tools)

### Assistant Management (5 tools)
| Tool | Description |
|------|-------------|
| `assistant_create` | Create a new assistant |
| `assistant_list` | List all assistants |
| `assistant_get` | Get an assistant by ID |
| `assistant_update` | Update an assistant |
| `assistant_delete` | Delete an assistant |

### Chatflow Management (6 tools)
| Tool | Description |
|------|-------------|
| `chatflow_create` | Create a new chatflow |
| `chatflow_list` | List all chatflows |
| `chatflow_get` | Get a chatflow by ID |
| `chatflow_get_by_apikey` | Get a chatflow by API key |
| `chatflow_update` | Update a chatflow including flowData, deployed status, and isPublic |
| `chatflow_delete` | Delete a chatflow |

### Predictions & Inference (2 tools)
| Tool | Description |
|------|-------------|
| `prediction_run` | Run a prediction on a chatflow with support for question, form (AgentFlow V2), streaming, overrideConfig, history, uploads, and humanInput |
| `prediction_stream` | Run a streaming prediction on a chatflow |

### Chat Message Management (2 tools)
| Tool | Description |
|------|-------------|
| `chatmessage_list` | List chat messages for a chatflow with filters |
| `chatmessage_delete_all` | Delete all chat messages for a chatflow |

### Attachments (1 tool)
| Tool | Description |
|------|-------------|
| `attachment_create` | Create attachments for a chatflow/chat session |

### Feedback Management (3 tools)
| Tool | Description |
|------|-------------|
| `feedback_list` | List feedback for a chatflow |
| `feedback_create` | Create feedback |
| `feedback_update` | Update feedback |

### Lead Management (2 tools)
| Tool | Description |
|------|-------------|
| `lead_list` | List leads for a chatflow |
| `lead_create` | Create a lead |

### Custom Tool Management (5 tools)
| Tool | Description |
|------|-------------|
| `tool_create` | Create a custom tool with schema and function |
| `tool_list` | List all custom tools |
| `tool_get` | Get a custom tool by ID |
| `tool_update` | Update a custom tool |
| `tool_delete` | Delete a custom tool |

### Variable Management (4 tools)
| Tool | Description |
|------|-------------|
| `variable_create` | Create a runtime variable |
| `variable_list` | List all variables |
| `variable_update` | Update a variable |
| `variable_delete` | Delete a variable |

### Document Store Operations (11 tools)
| Tool | Description |
|------|-------------|
| `docstore_list` | List all document stores |
| `docstore_get` | Get a document store by ID |
| `docstore_create` | Create a new document store |
| `docstore_upsert` | Upsert documents to a document store |
| `docstore_refresh` | Refresh/reprocess all documents in a store |
| `docstore_get_chunks` | Get loader chunks from a document store |
| `docstore_update_chunk` | Update a document chunk |
| `docstore_update` | Update a document store |
| `docstore_delete` | Delete a document store |
| `docstore_delete_chunk` | Delete a document chunk |
| `docstore_delete_loader` | Delete a loader and all its chunks |

### Vector Operations (1 tool)
| Tool | Description |
|------|-------------|
| `vector_upsert` | Upsert embeddings to vector store for a chatflow |

### Upsert History (2 tools)
| Tool | Description |
|------|-------------|
| `upsert_history_list` | Retrieve upsert history for a chatflow |
| `upsert_history_delete` | Soft-delete upsert history records |

### System & Health (1 tool)
| Tool | Description |
|------|-------------|
| `ping` | Health check endpoint |

## Resources (3 Resources)

| Resource | Description |
|----------|-------------|
| `config://server` | Server configuration including base URL and API key status |
| `status://connection` | Current connection status to FlowiseAI |
| `status://health` | Server health and capabilities information |

## Key Features

### Advanced Capabilities
- **Streaming Support**: Real-time prediction streaming
- **AgentFlow V2**: Full support for form-based inputs
- **Human-in-the-Loop**: Support for human intervention in workflows
- **Session Management**: Maintain conversation context across interactions
- **File Uploads**: Handle attachments and document uploads
- **Vector Operations**: RAG and semantic search capabilities
- **Override Configurations**: Dynamic runtime configuration

### Input Types Supported
- Text questions
- Form data (AgentFlow V2)
- File uploads
- Chat history
- Session IDs
- Override configurations
- Human input for HITL workflows

### Use Cases
1. **Chatbot Development**: Create and manage conversational AI
2. **Document Q&A**: Build RAG systems with document stores
3. **Workflow Automation**: Design complex AI workflows
4. **Feedback Collection**: Gather and analyze user feedback
5. **Lead Generation**: Capture and manage leads
6. **Custom Tool Creation**: Extend functionality with custom tools
7. **Variable Management**: Dynamic runtime configuration

## Quick Start Examples

### Initialize Connection
```python
# Python example
from mcp import Client
client = Client("flowiseai-client", "1.0.0")
# ... connect to server
```

### List Available Chatflows
```python
chatflows = await client.call_tool("chatflow_list", {})
```

### Run a Simple Prediction
```python
result = await client.call_tool("prediction_run", {
    "chatflow_id": "your-chatflow-id",
    "question": "What can you help me with?"
})
```

### Create a Document Store
```python
docstore = await client.call_tool("docstore_create", {
    "name": "Company Knowledge Base",
    "description": "Internal documentation",
    "loaders": [...],
    "vectorStoreConfig": {...}
})
```

### Stream a Prediction
```python
async for chunk in client.call_tool("prediction_stream", {
    "chatflow_id": "your-chatflow-id",
    "question": "Tell me a story",
    "streaming": True
}):
    print(chunk, end="")