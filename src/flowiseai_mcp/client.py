"""FlowiseAI API Client with full endpoint coverage"""

import os
import json
import asyncio
from typing import Optional, List, Dict, Any, AsyncGenerator, Union
from urllib.parse import urlparse, urljoin
import httpx
from .models import *
import logging

logger = logging.getLogger(__name__)


class FlowiseAIClient:
    """Async client for FlowiseAI API with complete endpoint coverage"""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.base_url = self._normalize_url(base_url or os.getenv("FLOWISEAI_URL", "http://localhost:3000"))
        self.api_key = api_key or os.getenv("FLOWISEAI_API_KEY", "")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}" if self.api_key else ""
        }
        self.client = httpx.AsyncClient(timeout=60.0)
        
    def _normalize_url(self, url: str) -> str:
        """Normalize URL to handle localhost, network, and cloud deployments"""
        if not url.startswith(("http://", "https://")):
            url = f"http://{url}"
        parsed = urlparse(url)
        if not parsed.path or parsed.path == "/":
            url = urljoin(url, "/api/v1")
        elif not parsed.path.endswith("/api/v1"):
            url = urljoin(url, "api/v1")
        return url.rstrip("/")
    
    async def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an async HTTP request"""
        url = f"{self.base_url}{endpoint}"
        try:
            response = await self.client.request(method, url, headers=self.headers, **kwargs)
            response.raise_for_status()
            return response.json() if response.content else {}
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Request failed: {str(e)}")
            raise
    
    async def _stream_request(self, method: str, endpoint: str, **kwargs) -> AsyncGenerator[str, None]:
        """Make a streaming HTTP request for SSE responses"""
        url = f"{self.base_url}{endpoint}"
        headers = {**self.headers, "Accept": "text/event-stream"}
        
        async with self.client.stream(method, url, headers=headers, **kwargs) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data != "[DONE]":
                        yield data
    
    # === Assistants ===
    
    async def create_assistant(self, assistant: Assistant) -> Assistant:
        data = await self._request("POST", "/assistants", json=assistant.model_dump(exclude_none=True))
        return Assistant(**data)
    
    async def list_assistants(self) -> List[Assistant]:
        data = await self._request("GET", "/assistants")
        return [Assistant(**item) for item in data]
    
    async def get_assistant(self, assistant_id: str) -> Assistant:
        data = await self._request("GET", f"/assistants/{assistant_id}")
        return Assistant(**data)
    
    async def update_assistant(self, assistant_id: str, assistant: Assistant) -> Assistant:
        data = await self._request("PUT", f"/assistants/{assistant_id}", 
                                  json=assistant.model_dump(exclude_none=True))
        return Assistant(**data)
    
    async def delete_assistant(self, assistant_id: str) -> bool:
        await self._request("DELETE", f"/assistants/{assistant_id}")
        return True
    
    # === Chatflows ===
    
    async def list_chatflows(self) -> List[Chatflow]:
        data = await self._request("GET", "/chatflows")
        return [Chatflow(**item) for item in data]
    
    async def get_chatflow(self, chatflow_id: str) -> Chatflow:
        data = await self._request("GET", f"/chatflows/{chatflow_id}")
        return Chatflow(**data)
    
    async def get_chatflow_by_apikey(self, apikey: str) -> Chatflow:
        data = await self._request("GET", f"/chatflows/apikey/{apikey}")
        return Chatflow(**data)
    
    async def create_chatflow(self, chatflow: Chatflow) -> Chatflow:
        data = await self._request("POST", "/chatflows", json=chatflow.model_dump(exclude_none=True))
        return Chatflow(**data)
    
    async def update_chatflow(self, chatflow_id: str, chatflow: Chatflow) -> Chatflow:
        data = await self._request("PUT", f"/chatflows/{chatflow_id}", 
                                  json=chatflow.model_dump(exclude_none=True))
        return Chatflow(**data)
    
    async def delete_chatflow(self, chatflow_id: str) -> bool:
        await self._request("DELETE", f"/chatflows/{chatflow_id}")
        return True
    
    # === Prediction ===
    
    async def predict(self, chatflow_id: str, request: PredictionRequest) -> Union[PredictionResponse, AsyncGenerator[str, None]]:
        """Execute a prediction with support for streaming"""
        if request.streaming:
            return self._stream_request("POST", f"/prediction/{chatflow_id}", 
                                       json=request.model_dump(exclude_none=True))
        else:
            data = await self._request("POST", f"/prediction/{chatflow_id}", 
                                      json=request.model_dump(exclude_none=True))
            return PredictionResponse(**data)
    
    async def predict_streaming(self, chatflow_id: str, request: PredictionRequest) -> AsyncGenerator[str, None]:
        """Execute a streaming prediction"""
        request.streaming = True
        async for chunk in self._stream_request("POST", f"/prediction/{chatflow_id}", 
                                               json=request.model_dump(exclude_none=True)):
            yield chunk
    
    # === Chat Messages ===
    
    async def list_chat_messages(
        self,
        chatflow_id: str,
        chat_type: Optional[ChatType] = None,
        order: Optional[str] = "DESC",
        chat_id: Optional[str] = None,
        memory_type: Optional[MemoryType] = None,
        session_id: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        feedback: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[ChatMessage]:
        params = {
            k: v for k, v in {
                "chatType": chat_type.value if chat_type else None,
                "order": order,
                "chatId": chat_id,
                "memoryType": memory_type.value if memory_type else None,
                "sessionId": session_id,
                "startDate": start_date,
                "endDate": end_date,
                "feedback": feedback,
                "limit": limit,
                "offset": offset
            }.items() if v is not None
        }
        data = await self._request("GET", f"/chatmessages/{chatflow_id}", params=params)
        return [ChatMessage(**item) for item in data]
    
    async def delete_chat_messages(self, chatflow_id: str) -> bool:
        await self._request("DELETE", f"/chatmessages/{chatflow_id}")
        return True
    
    # === Attachments ===
    
    async def create_attachments(
        self,
        chatflow_id: str,
        chat_id: str,
        attachments: List[Dict[str, Any]],
        return_base64: bool = False
    ) -> List[Attachment]:
        data = await self._request(
            "POST",
            f"/attachments/{chatflow_id}/{chat_id}",
            json={"attachments": attachments, "returnBase64": return_base64}
        )
        return [Attachment(**item) for item in data]
    
    # === Feedback ===
    
    async def list_feedback(self, chatflow_id: str) -> List[Feedback]:
        data = await self._request("GET", f"/feedback/{chatflow_id}")
        return [Feedback(**item) for item in data]
    
    async def create_feedback(self, feedback: Feedback) -> Feedback:
        data = await self._request("POST", "/feedback", json=feedback.model_dump(exclude_none=True))
        return Feedback(**data)
    
    async def update_feedback(self, feedback_id: str, feedback: Feedback) -> Feedback:
        data = await self._request("PUT", f"/feedback/{feedback_id}", 
                                  json=feedback.model_dump(exclude_none=True))
        return Feedback(**data)
    
    # === Leads ===
    
    async def list_leads(self, chatflow_id: str) -> List[Lead]:
        data = await self._request("GET", f"/leads/{chatflow_id}")
        return [Lead(**item) for item in data]
    
    async def create_lead(self, lead: Lead) -> Lead:
        data = await self._request("POST", "/leads", json=lead.model_dump(exclude_none=True))
        return Lead(**data)
    
    # === Tools ===
    
    async def create_tool(self, tool: Tool) -> Tool:
        data = await self._request("POST", "/tools", json=tool.model_dump(exclude_none=True))
        return Tool(**data)
    
    async def list_tools(self) -> List[Tool]:
        data = await self._request("GET", "/tools")
        return [Tool(**item) for item in data]
    
    async def get_tool(self, tool_id: str) -> Tool:
        data = await self._request("GET", f"/tools/{tool_id}")
        return Tool(**data)
    
    async def update_tool(self, tool_id: str, tool: Tool) -> Tool:
        data = await self._request("PUT", f"/tools/{tool_id}", 
                                  json=tool.model_dump(exclude_none=True))
        return Tool(**data)
    
    async def delete_tool(self, tool_id: str) -> bool:
        await self._request("DELETE", f"/tools/{tool_id}")
        return True
    
    # === Variables ===
    
    async def create_variable(self, variable: Variable) -> Variable:
        data = await self._request("POST", "/variables", json=variable.model_dump(exclude_none=True))
        return Variable(**data)
    
    async def list_variables(self) -> List[Variable]:
        data = await self._request("GET", "/variables")
        return [Variable(**item) for item in data]
    
    async def update_variable(self, variable_id: str, variable: Variable) -> Variable:
        data = await self._request("PUT", f"/variables/{variable_id}", 
                                  json=variable.model_dump(exclude_none=True))
        return Variable(**data)
    
    async def delete_variable(self, variable_id: str) -> bool:
        await self._request("DELETE", f"/variables/{variable_id}")
        return True
    
    # === Document Store ===
    
    async def list_document_stores(self) -> List[DocumentStore]:
        data = await self._request("GET", "/document-store")
        return [DocumentStore(**item) for item in data]
    
    async def get_document_store(self, store_id: str) -> DocumentStore:
        data = await self._request("GET", f"/document-store/{store_id}")
        return DocumentStore(**data)
    
    async def create_document_store(self, store: DocumentStore) -> DocumentStore:
        data = await self._request("POST", "/document-store", json=store.model_dump(exclude_none=True))
        return DocumentStore(**data)
    
    async def update_document_store(self, store_id: str, store: DocumentStore) -> DocumentStore:
        data = await self._request("PUT", f"/document-store/{store_id}", 
                                  json=store.model_dump(exclude_none=True))
        return DocumentStore(**data)
    
    async def delete_document_store(self, store_id: str) -> bool:
        await self._request("DELETE", f"/document-store/{store_id}")
        return True
    
    async def upsert_document(self, store_id: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        return await self._request("POST", f"/document-store/upsert/{store_id}", json={"documents": documents})
    
    async def refresh_document_store(self, store_id: str) -> Dict[str, Any]:
        return await self._request("POST", f"/document-store/refresh/{store_id}")
    
    async def get_document_chunks(self, store_id: str, loader_id: str) -> List[DocumentChunk]:
        data = await self._request("GET", f"/document-store/{store_id}/chunks/{loader_id}")
        return [DocumentChunk(**item) for item in data]
    
    async def update_document_chunk(self, store_id: str, chunk_id: str, chunk: DocumentChunk) -> DocumentChunk:
        data = await self._request("PUT", f"/document-store/{store_id}/chunks/{chunk_id}", 
                                  json=chunk.model_dump(exclude_none=True))
        return DocumentChunk(**data)
    
    async def delete_document_chunk(self, store_id: str, chunk_id: str) -> bool:
        await self._request("DELETE", f"/document-store/{store_id}/chunks/{chunk_id}")
        return True
    
    async def delete_document_loader(self, store_id: str, loader_id: str) -> bool:
        await self._request("DELETE", f"/document-store/{store_id}/loaders/{loader_id}")
        return True
    
    # === Vector Upsert ===
    
    async def vector_upsert(self, chatflow_id: str, request: VectorUpsertRequest) -> Dict[str, Any]:
        return await self._request("POST", f"/vector/upsert/{chatflow_id}", 
                                  json=request.model_dump(exclude_none=True))
    
    # === Upsert History ===
    
    async def list_upsert_history(
        self,
        chatflow_id: str,
        order: Optional[str] = "DESC",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[UpsertHistory]:
        params = {
            k: v for k, v in {
                "order": order,
                "startDate": start_date,
                "endDate": end_date
            }.items() if v is not None
        }
        data = await self._request("GET", f"/upsert-history/{chatflow_id}", params=params)
        return [UpsertHistory(**item) for item in data]
    
    async def delete_upsert_history(self, history_id: str) -> bool:
        await self._request("PATCH", f"/upsert-history/{history_id}")
        return True
    
    # === Health Check ===
    
    async def ping(self) -> str:
        """Health check endpoint"""
        response = await self._request("GET", "/ping")
        return response.get("message", "pong")
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()