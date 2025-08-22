"""FlowiseAI MCP Server - Complete implementation with all tools and resources"""

import os
import sys
import json
import asyncio
import socket
from typing import Optional, List, Dict, Any, Union
from contextlib import closing
import logging
from dotenv import load_dotenv

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool as MCPTool, TextContent, ImageContent, EmbeddedResource,
    BlobResourceContents, TextResourceContents, ServerCapabilities
)

from .client import FlowiseAIClient
from .models import *
from .models import Tool as FlowiseTool

# Load environment variables
load_dotenv()

# Configure logging to stderr with ERROR level only to avoid interfering with MCP protocol
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# Enable debug logging if DEBUG env var is set
if os.getenv('DEBUG', '').lower() in ('true', '1', 'yes'):
    logger.setLevel(logging.DEBUG)


def find_free_port() -> int:
    """Find a free port dynamically"""
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class FlowiseAIMCPServer:
    """MCP Server for FlowiseAI with complete API coverage"""
    
    def __init__(self):
        self.server = Server("flowiseai-mcp")
        self.client: Optional[FlowiseAIClient] = None
        self.initialization_options = InitializationOptions(
            server_name="flowiseai-mcp",
            server_version="1.0.0",
            capabilities=ServerCapabilities()
        )
        self.setup_handlers()
        
    def setup_handlers(self):
        """Setup all MCP handlers"""
        
        # === Assistants Tools ===
        
        @self.server.list_tools()
        async def list_tools() -> List[MCPTool]:
            return [
                # Assistant tools
                MCPTool(
                    name="assistant_create",
                    description="Create a new assistant",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "model": {"type": "string"},
                            "prompt": {"type": "string"},
                            "temperature": {"type": "number"},
                            "max_tokens": {"type": "integer"},
                            "tools": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["name"]
                    }
                ),
                MCPTool(
                    name="assistant_list",
                    description="List all assistants",
                    inputSchema={"type": "object", "properties": {}}
                ),
                MCPTool(
                    name="assistant_get",
                    description="Get an assistant by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"]
                    }
                ),
                MCPTool(
                    name="assistant_update",
                    description="Update an assistant",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "model": {"type": "string"},
                            "prompt": {"type": "string"},
                            "temperature": {"type": "number"},
                            "max_tokens": {"type": "integer"}
                        },
                        "required": ["id"]
                    }
                ),
                MCPTool(
                    name="assistant_delete",
                    description="Delete an assistant",
                    inputSchema={
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"]
                    }
                ),
                
                # Chatflow tools
                MCPTool(
                    name="chatflow_create",
                    description="Create a new chatflow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "flowData": {"type": "object"},
                            "deployed": {"type": "boolean"},
                            "isPublic": {"type": "boolean"},
                            "category": {"type": "string"}
                        },
                        "required": ["name"]
                    }
                ),
                MCPTool(
                    name="chatflow_list",
                    description="List all chatflows",
                    inputSchema={"type": "object", "properties": {}}
                ),
                MCPTool(
                    name="chatflow_get",
                    description="Get a chatflow by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"]
                    }
                ),
                MCPTool(
                    name="chatflow_get_by_apikey",
                    description="Get a chatflow by API key",
                    inputSchema={
                        "type": "object",
                        "properties": {"apikey": {"type": "string"}},
                        "required": ["apikey"]
                    }
                ),
                MCPTool(
                    name="chatflow_update",
                    description="Update a chatflow including flowData, deployed status, and isPublic",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "flowData": {"type": "object"},
                            "deployed": {"type": "boolean"},
                            "isPublic": {"type": "boolean"}
                        },
                        "required": ["id"]
                    }
                ),
                MCPTool(
                    name="chatflow_delete",
                    description="Delete a chatflow",
                    inputSchema={
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"]
                    }
                ),
                
                # Prediction tools
                MCPTool(
                    name="prediction_run",
                    description="Run a prediction on a chatflow with support for question, form (AgentFlow V2), streaming, overrideConfig, history, uploads, and humanInput",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "chatflow_id": {"type": "string"},
                            "question": {"type": "string"},
                            "form": {"type": "object", "description": "AgentFlow V2 form inputs"},
                            "streaming": {"type": "boolean"},
                            "overrideConfig": {
                                "type": "object",
                                "properties": {
                                    "sessionId": {"type": "string"},
                                    "vars": {"type": "object"},
                                    "temperature": {"type": "number"},
                                    "maxTokens": {"type": "integer"}
                                }
                            },
                            "history": {"type": "array", "items": {"type": "object"}},
                            "uploads": {"type": "array", "items": {"type": "object"}},
                            "humanInput": {"type": "string", "description": "Human-in-the-loop input"},
                            "chatId": {"type": "string"}
                        },
                        "required": ["chatflow_id"]
                    }
                ),
                MCPTool(
                    name="prediction_stream",
                    description="Run a streaming prediction on a chatflow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "chatflow_id": {"type": "string"},
                            "question": {"type": "string"},
                            "form": {"type": "object"},
                            "overrideConfig": {"type": "object"},
                            "history": {"type": "array"},
                            "uploads": {"type": "array"},
                            "sessionId": {"type": "string"}
                        },
                        "required": ["chatflow_id"]
                    }
                ),
                
                # Chat Message tools
                MCPTool(
                    name="chatmessage_list",
                    description="List chat messages for a chatflow with filters",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "chatflow_id": {"type": "string"},
                            "chatType": {"type": "string", "enum": ["INTERNAL", "EXTERNAL"]},
                            "order": {"type": "string", "enum": ["ASC", "DESC"]},
                            "chatId": {"type": "string"},
                            "memoryType": {"type": "string"},
                            "sessionId": {"type": "string"},
                            "startDate": {"type": "string"},
                            "endDate": {"type": "string"},
                            "feedback": {"type": "boolean"},
                            "limit": {"type": "integer"},
                            "offset": {"type": "integer"}
                        },
                        "required": ["chatflow_id"]
                    }
                ),
                MCPTool(
                    name="chatmessage_delete_all",
                    description="Delete all chat messages for a chatflow",
                    inputSchema={
                        "type": "object",
                        "properties": {"chatflow_id": {"type": "string"}},
                        "required": ["chatflow_id"]
                    }
                ),
                
                # Attachment tools
                MCPTool(
                    name="attachment_create",
                    description="Create attachments for a chatflow/chat session",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "chatflow_id": {"type": "string"},
                            "chat_id": {"type": "string"},
                            "attachments": {"type": "array"},
                            "return_base64": {"type": "boolean"}
                        },
                        "required": ["chatflow_id", "chat_id", "attachments"]
                    }
                ),
                
                # Feedback tools
                MCPTool(
                    name="feedback_list",
                    description="List feedback for a chatflow",
                    inputSchema={
                        "type": "object",
                        "properties": {"chatflow_id": {"type": "string"}},
                        "required": ["chatflow_id"]
                    }
                ),
                MCPTool(
                    name="feedback_create",
                    description="Create feedback",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "chatflowid": {"type": "string"},
                            "chatId": {"type": "string"},
                            "messageId": {"type": "string"},
                            "rating": {"type": "integer", "minimum": 1, "maximum": 5},
                            "content": {"type": "string"}
                        },
                        "required": ["chatflowid", "chatId"]
                    }
                ),
                MCPTool(
                    name="feedback_update",
                    description="Update feedback",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "rating": {"type": "integer"},
                            "content": {"type": "string"}
                        },
                        "required": ["id"]
                    }
                ),
                
                # Lead tools
                MCPTool(
                    name="lead_list",
                    description="List leads for a chatflow",
                    inputSchema={
                        "type": "object",
                        "properties": {"chatflow_id": {"type": "string"}},
                        "required": ["chatflow_id"]
                    }
                ),
                MCPTool(
                    name="lead_create",
                    description="Create a lead",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "chatflowid": {"type": "string"},
                            "chatId": {"type": "string"},
                            "name": {"type": "string"},
                            "email": {"type": "string"},
                            "phone": {"type": "string"}
                        },
                        "required": ["chatflowid", "chatId"]
                    }
                ),
                
                # Custom Tool tools
                MCPTool(
                    name="tool_create",
                    description="Create a custom tool with schema and function",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "schema": {"type": "object"},
                            "func": {"type": "string"}
                        },
                        "required": ["name"]
                    }
                ),
                MCPTool(
                    name="tool_list",
                    description="List all custom tools",
                    inputSchema={"type": "object", "properties": {}}
                ),
                MCPTool(
                    name="tool_get",
                    description="Get a custom tool by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"]
                    }
                ),
                MCPTool(
                    name="tool_update",
                    description="Update a custom tool",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "schema": {"type": "object"},
                            "func": {"type": "string"}
                        },
                        "required": ["id"]
                    }
                ),
                MCPTool(
                    name="tool_delete",
                    description="Delete a custom tool",
                    inputSchema={
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"]
                    }
                ),
                
                # Variable tools
                MCPTool(
                    name="variable_create",
                    description="Create a runtime variable",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "value": {},
                            "type": {"type": "string"}
                        },
                        "required": ["name", "value"]
                    }
                ),
                MCPTool(
                    name="variable_list",
                    description="List all variables",
                    inputSchema={"type": "object", "properties": {}}
                ),
                MCPTool(
                    name="variable_update",
                    description="Update a variable",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "value": {},
                            "type": {"type": "string"}
                        },
                        "required": ["id"]
                    }
                ),
                MCPTool(
                    name="variable_delete",
                    description="Delete a variable",
                    inputSchema={
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"]
                    }
                ),
                
                # Document Store tools
                MCPTool(
                    name="docstore_list",
                    description="List all document stores",
                    inputSchema={"type": "object", "properties": {}}
                ),
                MCPTool(
                    name="docstore_get",
                    description="Get a document store by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"]
                    }
                ),
                MCPTool(
                    name="docstore_create",
                    description="Create a new document store",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "loaders": {"type": "array"},
                            "vectorStoreConfig": {"type": "object"},
                            "embeddingConfig": {"type": "object"},
                            "recordManagerConfig": {"type": "object"}
                        },
                        "required": ["name"]
                    }
                ),
                MCPTool(
                    name="docstore_upsert",
                    description="Upsert documents to a document store",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "store_id": {"type": "string"},
                            "documents": {"type": "array"}
                        },
                        "required": ["store_id", "documents"]
                    }
                ),
                MCPTool(
                    name="docstore_refresh",
                    description="Refresh/reprocess all documents in a store",
                    inputSchema={
                        "type": "object",
                        "properties": {"store_id": {"type": "string"}},
                        "required": ["store_id"]
                    }
                ),
                MCPTool(
                    name="docstore_get_chunks",
                    description="Get loader chunks from a document store",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "store_id": {"type": "string"},
                            "loader_id": {"type": "string"}
                        },
                        "required": ["store_id", "loader_id"]
                    }
                ),
                MCPTool(
                    name="docstore_update_chunk",
                    description="Update a document chunk",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "store_id": {"type": "string"},
                            "chunk_id": {"type": "string"},
                            "pageContent": {"type": "string"},
                            "metadata": {"type": "object"}
                        },
                        "required": ["store_id", "chunk_id"]
                    }
                ),
                MCPTool(
                    name="docstore_update",
                    description="Update a document store",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "description": {"type": "string"}
                        },
                        "required": ["id"]
                    }
                ),
                MCPTool(
                    name="docstore_delete",
                    description="Delete a document store",
                    inputSchema={
                        "type": "object",
                        "properties": {"id": {"type": "string"}},
                        "required": ["id"]
                    }
                ),
                MCPTool(
                    name="docstore_delete_chunk",
                    description="Delete a document chunk",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "store_id": {"type": "string"},
                            "chunk_id": {"type": "string"}
                        },
                        "required": ["store_id", "chunk_id"]
                    }
                ),
                MCPTool(
                    name="docstore_delete_loader",
                    description="Delete a loader and all its chunks",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "store_id": {"type": "string"},
                            "loader_id": {"type": "string"}
                        },
                        "required": ["store_id", "loader_id"]
                    }
                ),
                
                # Vector tools
                MCPTool(
                    name="vector_upsert",
                    description="Upsert embeddings to vector store for a chatflow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "chatflow_id": {"type": "string"},
                            "documents": {"type": "array"},
                            "texts": {"type": "array"},
                            "embeddings": {"type": "array"},
                            "metadata": {"type": "array"},
                            "stopNodeId": {"type": "string"},
                            "overrideConfig": {"type": "object"}
                        },
                        "required": ["chatflow_id"]
                    }
                ),
                
                # Upsert History tools
                MCPTool(
                    name="upsert_history_list",
                    description="Retrieve upsert history for a chatflow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "chatflow_id": {"type": "string"},
                            "order": {"type": "string", "enum": ["ASC", "DESC"]},
                            "startDate": {"type": "string"},
                            "endDate": {"type": "string"}
                        },
                        "required": ["chatflow_id"]
                    }
                ),
                MCPTool(
                    name="upsert_history_delete",
                    description="Soft-delete upsert history records",
                    inputSchema={
                        "type": "object",
                        "properties": {"history_id": {"type": "string"}},
                        "required": ["history_id"]
                    }
                ),
                
                # Health check
                MCPTool(
                    name="ping",
                    description="Health check endpoint",
                    inputSchema={"type": "object", "properties": {}}
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[Union[TextContent, ImageContent]]:
            """Execute tool calls"""
            
            # Handle ping without client for test mode
            if name == "ping":
                # Check if we're in test mode (no API key)
                if not os.getenv("FLOWISEAI_API_KEY") or os.getenv("FLOWISEAI_API_KEY") == "test-key":
                    return [TextContent(type="text", text="pong (test mode)")]
                
                # Otherwise try real ping
                if not self.client:
                    self.client = FlowiseAIClient()
                try:
                    result = await self.client.ping()
                    return [TextContent(type="text", text=result)]
                except:
                    return [TextContent(type="text", text="pong (offline)")]
            
            # For all other tools, create client if needed
            if not self.client:
                # Check if we're in test mode
                if not os.getenv("FLOWISEAI_API_KEY") or os.getenv("FLOWISEAI_API_KEY") == "test-key":
                    return [TextContent(type="text", text=f"Tool '{name}' unavailable in test mode. Please configure FLOWISEAI_API_KEY.")]
                self.client = FlowiseAIClient()
            
            try:
                # Assistant operations
                if name == "assistant_create":
                    assistant = Assistant(**arguments)
                    result = await self.client.create_assistant(assistant)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "assistant_list":
                    results = await self.client.list_assistants()
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                elif name == "assistant_get":
                    result = await self.client.get_assistant(arguments["id"])
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "assistant_update":
                    assistant_id = arguments.pop("id")
                    assistant = Assistant(**arguments)
                    result = await self.client.update_assistant(assistant_id, assistant)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "assistant_delete":
                    await self.client.delete_assistant(arguments["id"])
                    return [TextContent(type="text", text="Assistant deleted successfully")]
                
                # Chatflow operations
                elif name == "chatflow_create":
                    chatflow = Chatflow(**arguments)
                    result = await self.client.create_chatflow(chatflow)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "chatflow_list":
                    results = await self.client.list_chatflows()
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                elif name == "chatflow_get":
                    result = await self.client.get_chatflow(arguments["id"])
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "chatflow_get_by_apikey":
                    result = await self.client.get_chatflow_by_apikey(arguments["apikey"])
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "chatflow_update":
                    chatflow_id = arguments.pop("id")
                    chatflow = Chatflow(**arguments)
                    result = await self.client.update_chatflow(chatflow_id, chatflow)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "chatflow_delete":
                    await self.client.delete_chatflow(arguments["id"])
                    return [TextContent(type="text", text="Chatflow deleted successfully")]
                
                # Prediction operations
                elif name == "prediction_run":
                    chatflow_id = arguments.pop("chatflow_id")
                    request = PredictionRequest(**arguments)
                    
                    if request.streaming:
                        chunks = []
                        async for chunk in await self.client.predict(chatflow_id, request):
                            chunks.append(chunk)
                        return [TextContent(type="text", text="\\n".join(chunks))]
                    else:
                        result = await self.client.predict(chatflow_id, request)
                        return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "prediction_stream":
                    chatflow_id = arguments.pop("chatflow_id")
                    request = PredictionRequest(**arguments)
                    chunks = []
                    async for chunk in self.client.predict_streaming(chatflow_id, request):
                        chunks.append(chunk)
                    return [TextContent(type="text", text="\\n".join(chunks))]
                
                # Chat Message operations
                elif name == "chatmessage_list":
                    chatflow_id = arguments.pop("chatflow_id")
                    chat_type = ChatType(arguments.pop("chatType")) if "chatType" in arguments else None
                    memory_type = MemoryType(arguments.pop("memoryType")) if "memoryType" in arguments else None
                    
                    results = await self.client.list_chat_messages(
                        chatflow_id,
                        chat_type=chat_type,
                        memory_type=memory_type,
                        **arguments
                    )
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                elif name == "chatmessage_delete_all":
                    await self.client.delete_chat_messages(arguments["chatflow_id"])
                    return [TextContent(type="text", text="All chat messages deleted successfully")]
                
                # Attachment operations
                elif name == "attachment_create":
                    results = await self.client.create_attachments(
                        arguments["chatflow_id"],
                        arguments["chat_id"],
                        arguments["attachments"],
                        arguments.get("return_base64", False)
                    )
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                # Feedback operations
                elif name == "feedback_list":
                    results = await self.client.list_feedback(arguments["chatflow_id"])
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                elif name == "feedback_create":
                    feedback = Feedback(**arguments)
                    result = await self.client.create_feedback(feedback)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "feedback_update":
                    feedback_id = arguments.pop("id")
                    feedback = Feedback(**arguments)
                    result = await self.client.update_feedback(feedback_id, feedback)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                # Lead operations
                elif name == "lead_list":
                    results = await self.client.list_leads(arguments["chatflow_id"])
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                elif name == "lead_create":
                    lead = Lead(**arguments)
                    result = await self.client.create_lead(lead)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                # Custom Tool operations
                elif name == "tool_create":
                    tool = FlowiseTool(**arguments)
                    result = await self.client.create_tool(tool)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "tool_list":
                    results = await self.client.list_tools()
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                elif name == "tool_get":
                    result = await self.client.get_tool(arguments["id"])
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "tool_update":
                    tool_id = arguments.pop("id")
                    tool = FlowiseTool(**arguments)
                    result = await self.client.update_tool(tool_id, tool)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "tool_delete":
                    await self.client.delete_tool(arguments["id"])
                    return [TextContent(type="text", text="Tool deleted successfully")]
                
                # Variable operations
                elif name == "variable_create":
                    variable = Variable(**arguments)
                    result = await self.client.create_variable(variable)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "variable_list":
                    results = await self.client.list_variables()
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                elif name == "variable_update":
                    variable_id = arguments.pop("id")
                    variable = Variable(**arguments)
                    result = await self.client.update_variable(variable_id, variable)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "variable_delete":
                    await self.client.delete_variable(arguments["id"])
                    return [TextContent(type="text", text="Variable deleted successfully")]
                
                # Document Store operations
                elif name == "docstore_list":
                    results = await self.client.list_document_stores()
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                elif name == "docstore_get":
                    result = await self.client.get_document_store(arguments["id"])
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "docstore_create":
                    store = DocumentStore(**arguments)
                    result = await self.client.create_document_store(store)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "docstore_upsert":
                    result = await self.client.upsert_document(arguments["store_id"], arguments["documents"])
                    return [TextContent(type="text", text=json.dumps(result, default=str))]
                
                elif name == "docstore_refresh":
                    result = await self.client.refresh_document_store(arguments["store_id"])
                    return [TextContent(type="text", text=json.dumps(result, default=str))]
                
                elif name == "docstore_get_chunks":
                    results = await self.client.get_document_chunks(arguments["store_id"], arguments["loader_id"])
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                elif name == "docstore_update_chunk":
                    store_id = arguments.pop("store_id")
                    chunk_id = arguments.pop("chunk_id")
                    chunk = DocumentChunk(**arguments)
                    result = await self.client.update_document_chunk(store_id, chunk_id, chunk)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "docstore_update":
                    store_id = arguments.pop("id")
                    store = DocumentStore(**arguments)
                    result = await self.client.update_document_store(store_id, store)
                    return [TextContent(type="text", text=json.dumps(result.model_dump(), default=str))]
                
                elif name == "docstore_delete":
                    await self.client.delete_document_store(arguments["id"])
                    return [TextContent(type="text", text="Document store deleted successfully")]
                
                elif name == "docstore_delete_chunk":
                    await self.client.delete_document_chunk(arguments["store_id"], arguments["chunk_id"])
                    return [TextContent(type="text", text="Document chunk deleted successfully")]
                
                elif name == "docstore_delete_loader":
                    await self.client.delete_document_loader(arguments["store_id"], arguments["loader_id"])
                    return [TextContent(type="text", text="Document loader and chunks deleted successfully")]
                
                # Vector operations
                elif name == "vector_upsert":
                    chatflow_id = arguments.pop("chatflow_id")
                    request = VectorUpsertRequest(**arguments)
                    result = await self.client.vector_upsert(chatflow_id, request)
                    return [TextContent(type="text", text=json.dumps(result, default=str))]
                
                # Upsert History operations
                elif name == "upsert_history_list":
                    chatflow_id = arguments.pop("chatflow_id")
                    results = await self.client.list_upsert_history(chatflow_id, **arguments)
                    return [TextContent(type="text", text=json.dumps([r.model_dump() for r in results], default=str))]
                
                elif name == "upsert_history_delete":
                    await self.client.delete_upsert_history(arguments["history_id"])
                    return [TextContent(type="text", text="Upsert history deleted successfully")]
                
                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]
                    
            except Exception as e:
                logger.error(f"Tool execution error: {str(e)}")
                return [TextContent(type="text", text=f"Error: {str(e)}")]
        
        # Resources for configuration and status
        @self.server.list_resources()
        async def list_resources() -> List[str]:
            return [
                "config://server",
                "status://connection",
                "status://health"
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            if uri == "config://server":
                config = {
                    "base_url": os.getenv("FLOWISEAI_URL", "http://localhost:3000"),
                    "api_key": "***" if os.getenv("FLOWISEAI_API_KEY") else "Not set",
                    "test_mode": not os.getenv("FLOWISEAI_API_KEY") or os.getenv("FLOWISEAI_API_KEY") == "test-key"
                }
                return json.dumps(config, indent=2)
            
            elif uri == "status://connection":
                # Check if we're in test mode
                if not os.getenv("FLOWISEAI_API_KEY") or os.getenv("FLOWISEAI_API_KEY") == "test-key":
                    return json.dumps({"status": "test_mode", "message": "Running in test mode without FlowiseAI connection"})
                
                if not self.client:
                    self.client = FlowiseAIClient()
                try:
                    result = await self.client.ping()
                    return json.dumps({"status": "connected", "message": result})
                except:
                    return json.dumps({"status": "disconnected", "message": "Unable to connect to FlowiseAI"})
            
            elif uri == "status://health":
                return json.dumps({
                    "server": "running",
                    "version": "1.0.0",
                    "capabilities": [
                        "assistants", "chatflows", "predictions", "streaming",
                        "agentflow_v2", "document_store", "vector_operations",
                        "uploads", "hitl", "session_management"
                    ],
                    "test_mode": not os.getenv("FLOWISEAI_API_KEY") or os.getenv("FLOWISEAI_API_KEY") == "test-key"
                })
            
            return ""
    
    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(read_stream, write_stream, self.initialization_options)
    
    async def cleanup(self):
        """Cleanup resources"""
        if self.client:
            await self.client.close()


def main():
    """Main entry point"""
    server = None
    try:
        # Check required environment variables (only log warnings in debug mode)
        if not os.getenv("FLOWISEAI_URL") and logger.level <= logging.WARNING:
            logger.warning("FLOWISEAI_URL not set, using default: http://localhost:3000")
        
        if not os.getenv("FLOWISEAI_API_KEY") and logger.level <= logging.WARNING:
            logger.warning("FLOWISEAI_API_KEY not set, authentication may fail")
        
        # Create and run server
        server = FlowiseAIMCPServer()
        asyncio.run(server.run())
        
    except KeyboardInterrupt:
        if logger.level <= logging.INFO:
            logger.info("Server stopped by user")
    except Exception as e:
        import traceback
        logger.error(f"Server error: {str(e)}")
        if logger.level <= logging.DEBUG:
            logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)
    finally:
        if server:
            asyncio.run(server.cleanup())


if __name__ == "__main__":
    main()