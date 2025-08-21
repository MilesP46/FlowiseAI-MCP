"""Data models for FlowiseAI MCP Server"""

from typing import Optional, List, Dict, Any, Union
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class ChatType(str, Enum):
    INTERNAL = "INTERNAL"
    EXTERNAL = "EXTERNAL"


class MemoryType(str, Enum):
    WINDOW_BUFFER = "windowBufferMemory"
    CONVERSATION_SUMMARY = "conversationSummaryMemory"
    BUFFER = "bufferMemory"


class Assistant(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    model: Optional[str] = None
    prompt: Optional[str] = None
    temperature: Optional[float] = Field(default=0.7, ge=0, le=1)
    max_tokens: Optional[int] = None
    tools: Optional[List[str]] = None
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None


class Chatflow(BaseModel):
    id: Optional[str] = None
    name: str
    flowData: Optional[Dict[str, Any]] = None
    deployed: Optional[bool] = True
    isPublic: Optional[bool] = False
    apikeyid: Optional[str] = None
    category: Optional[str] = None
    speechToText: Optional[Dict[str, Any]] = None
    chatbotConfig: Optional[Dict[str, Any]] = None
    createdDate: Optional[datetime] = None
    updatedDate: Optional[datetime] = None


class PredictionRequest(BaseModel):
    question: Optional[str] = None
    overrideConfig: Optional[Dict[str, Any]] = None
    history: Optional[List[Dict[str, str]]] = None
    uploads: Optional[List[Dict[str, Any]]] = None
    streaming: Optional[bool] = False
    form: Optional[Dict[str, Any]] = None  # For AgentFlow V2
    humanInput: Optional[str] = None  # For HITL
    sessionId: Optional[str] = None
    chatId: Optional[str] = None


class PredictionResponse(BaseModel):
    text: Optional[str] = None
    json_response: Optional[Dict[str, Any]] = Field(None, alias="json")
    chatId: Optional[str] = None
    sessionId: Optional[str] = None
    sourceDocuments: Optional[List[Dict[str, Any]]] = None
    usedTools: Optional[List[Dict[str, Any]]] = None
    question: Optional[str] = None
    chatMessageId: Optional[str] = None


class ChatMessage(BaseModel):
    id: Optional[str] = None
    role: str
    content: str
    chatflowid: str
    chatType: Optional[ChatType] = ChatType.INTERNAL
    chatId: Optional[str] = None
    memoryType: Optional[MemoryType] = None
    sessionId: Optional[str] = None
    createdDate: Optional[datetime] = None
    sourceDocuments: Optional[List[Dict[str, Any]]] = None
    usedTools: Optional[List[Dict[str, Any]]] = None
    fileAnnotations: Optional[List[Dict[str, Any]]] = None
    feedback: Optional[Dict[str, Any]] = None


class Attachment(BaseModel):
    id: Optional[str] = None
    chatflowId: str
    chatId: str
    fileName: str
    fileBase64: Optional[str] = None
    fileUrl: Optional[str] = None
    mimeType: Optional[str] = None
    createdDate: Optional[datetime] = None


class Feedback(BaseModel):
    id: Optional[str] = None
    chatflowid: str
    chatId: str
    messageId: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    content: Optional[str] = None
    createdDate: Optional[datetime] = None


class Lead(BaseModel):
    id: Optional[str] = None
    chatflowid: str
    chatId: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    createdDate: Optional[datetime] = None


class Tool(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    tool_schema: Optional[Dict[str, Any]] = Field(None, alias="schema")
    func: Optional[str] = None
    iconSrc: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedDate: Optional[datetime] = None


class Variable(BaseModel):
    id: Optional[str] = None
    name: str
    value: Any
    type: Optional[str] = Field(default="string")
    createdDate: Optional[datetime] = None
    updatedDate: Optional[datetime] = None


class DocumentStore(BaseModel):
    id: Optional[str] = None
    name: str
    description: Optional[str] = None
    loaders: Optional[List[Dict[str, Any]]] = None
    whereUsed: Optional[List[str]] = None
    vectorStoreConfig: Optional[Dict[str, Any]] = None
    embeddingConfig: Optional[Dict[str, Any]] = None
    recordManagerConfig: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedDate: Optional[datetime] = None


class DocumentLoader(BaseModel):
    id: Optional[str] = None
    loaderId: str
    storeId: str
    loaderName: str
    loaderConfig: Optional[Dict[str, Any]] = None
    splitterConfig: Optional[Dict[str, Any]] = None
    totalChunks: Optional[int] = None
    totalChars: Optional[int] = None
    status: Optional[str] = None
    createdDate: Optional[datetime] = None
    updatedDate: Optional[datetime] = None


class DocumentChunk(BaseModel):
    id: Optional[str] = None
    docId: str
    storeId: str
    loaderId: str
    chunkNo: Optional[int] = None
    pageContent: str
    metadata: Optional[Dict[str, Any]] = None


class VectorUpsertRequest(BaseModel):
    documents: Optional[List[Dict[str, Any]]] = None
    texts: Optional[List[str]] = None
    embeddings: Optional[List[List[float]]] = None
    metadata: Optional[List[Dict[str, Any]]] = None
    stopNodeId: Optional[str] = None
    overrideConfig: Optional[Dict[str, Any]] = None


class UpsertHistory(BaseModel):
    id: Optional[str] = None
    chatflowid: str
    result: Optional[Dict[str, Any]] = None
    flowData: Optional[str] = None
    date: Optional[datetime] = None