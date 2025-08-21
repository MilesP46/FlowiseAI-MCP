# FlowiseAI MCP Server Functionality Coverage Checklist

> Scope: **Only** endpoints and runtime features your MCP must expose to fully operate and automate Flowise (Assistants, Chatflows & Agentflow V2). No setup/env items.

- [ ] [Assistants](https://docs.flowiseai.com/api-reference/assistants) — Create (POST), Read (GET), Update (PUT), Delete (DELETE).
- [ ] [Chatflows](https://docs.flowiseai.com/api-reference/chatflows) — List (GET), Get by ID (GET), Get by API key (GET), Create (POST), Update (PUT, incl. `flowData`, `deployed`, `isPublic`), Delete (DELETE).
- [ ] [Prediction](https://docs.flowiseai.com/api-reference/prediction) — Invoke flow run (POST `/prediction/{id}`) with support for:
      `question` messages, Agentflow V2 `form` payloads, `streaming` flag, `overrideConfig` (e.g., `sessionId`, `vars`, temperature/max tokens), conversation `history`, file `uploads`, and `humanInput` for HITL resume; return handling for `text`, `json`, `chatId`, `sourceDocuments`, `usedTools`.
- [ ] [Agentflow V2 — Start Node](https://docs.flowiseai.com/using-flowise/agentflowv2#id-1.-start-node) — Accept & forward Start Node inputs (form fields), initialize flow state, memory behavior; ensure parity with Chatflow messaging path.
- [ ] [Uploads (images/audio/files)](https://docs.flowiseai.com/using-flowise/uploads) — Support `uploads` array on Prediction API (base64 or URL), and speech-to-text inputs where enabled by the flow.
- [ ] [Chat Message](https://docs.flowiseai.com/api-reference/chat-message) — List chat messages for a chatflow (GET) with filters (`chatType`, `order`, `chatId`, `memoryType`, `sessionId`, date range, feedback flags); Delete all chat messages (DELETE).
- [ ] [Attachments](https://docs.flowiseai.com/api-reference/attachments) — Create attachments array for a chatflow/chat session (POST `/attachments/{chatflowId}/{chatId}`) with optional `base64` response.
- [ ] [Feedback](https://docs.flowiseai.com/api-reference/feedback) — List feedback per chatflow (GET), Create feedback (POST), Update feedback (PUT).
- [ ] [Leads](https://docs.flowiseai.com/api-reference/leads) — List leads per chatflow (GET), Create lead (POST) with `name`, `email`, `phone`, `chatId`.
- [ ] [Tools](https://docs.flowiseai.com/api-reference/tools) — Create custom tool (POST with `schema`, `func`), List (GET), Read (GET), Update (PUT), Delete (DELETE).
- [ ] [Variables](https://docs.flowiseai.com/api-reference/variables) — Create (POST), List (GET), Update (PUT), Delete (DELETE) for runtime vars used by flows.
- [ ] [Document Store](https://docs.flowiseai.com/api-reference/document-store) — Full RAG data management:
      List stores (GET), Get store (GET), Create store (POST), Upsert document (POST `/document-store/upsert/{id}`), Refresh/reprocess all (POST `/document-store/refresh/{id}`), Get loader chunks (GET), Update chunk (PUT), Update store (PUT), Delete store (DELETE), Delete chunk (DELETE), Delete loader+chunks (DELETE), Delete vector-store data.
- [ ] [Vector Upsert](https://docs.flowiseai.com/api-reference/vector-upsert) — Upsert embeddings to vector store for a chatflow (POST `/vector/upsert/{id}`) with optional `stopNodeId` & `overrideConfig`.
- [ ] [Upsert History](https://docs.flowiseai.com/api-reference/upsert-history) — Retrieve upsert history per chatflow (GET with sort/date filters), Soft-delete records (PATCH).
- [ ] [Ping](https://docs.flowiseai.com/api-reference/ping) — Health check endpoint (GET `/ping` → `pong`) for MCP liveness probing.
- [ ] [API Reference index](https://docs.flowiseai.com/api-reference) — Ensure MCP exposes all listed public APIs consistently (routing, auth headers, error surfaces).

## Execution Semantics & Cross-Cutting Behaviors

- [ ] **Streaming Responses (SSE/Web)** — Honor `streaming` on Prediction; surface token/step streams to clients and tools where applicable.
- [ ] **Session/Memory Control** — Pass-through `sessionId` and memory selection (Agentflow/Chatflow) for thread continuity across calls.
- [ ] **Variable Injection** — Support `overrideConfig.vars` and global `Variables` store for dynamic prompt/runtime values.
- [ ] **Human-in-the-Loop** — Accept `humanInput` to resume flows from checkpoints (approve/reject/feedback) via Prediction API.
- [ ] **Uploads Pipeline** — Forward `uploads` (file/url, name, mime) to flows; ensure compatibility with enabled image/audio handling.
- [ ] **Agent-as-Tool & Multi-Agent** — Ensure flows that use agents/tools can call nested agents or Chatflow Tool nodes transparently.
- [ ] **Get-by-API-Key Routing** — Resolve chatflow via `/chatflows/apikey/{apikey}` for key-scoped predictions.
- [ ] **RAG Lifecycle** — Cover Document Store upsertion, refresh, chunk inspection/updates, and Vector Upsert orchestration end-to-end.
