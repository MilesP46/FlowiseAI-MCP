"""HTTP server wrapper for MCP using Streamable HTTP transport"""

import os
import sys
import json
import logging
import base64
import asyncio
from typing import Optional
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.requests import Request
import uvicorn
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager

# Import the main server
from .server import FlowiseAIMCPServer

# Configure logging to stderr
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# Enable debug logging if DEBUG env var is set
if os.getenv('DEBUG', '').lower() in ('true', '1', 'yes'):
    logger.setLevel(logging.DEBUG)


class MCPApp:
    """MCP Application with Streamable HTTP transport"""
    
    def __init__(self):
        # Create the MCP server instance
        self.mcp_server_instance = FlowiseAIMCPServer()
        self.mcp_server = self.mcp_server_instance.server
        
        # Create the session manager
        self.session_manager = StreamableHTTPSessionManager(
            app=self.mcp_server,
            json_response=False,
            stateless=False
        )
        
        # Track if session manager is running
        self.manager_task = None
    
    async def startup(self):
        """Start the session manager"""
        async def run_manager():
            async with self.session_manager.run():
                await asyncio.Event().wait()
        
        self.manager_task = asyncio.create_task(run_manager())
        logger.info("Session manager started")
    
    async def shutdown(self):
        """Shutdown the session manager"""
        if self.manager_task:
            self.manager_task.cancel()
            try:
                await self.manager_task
            except asyncio.CancelledError:
                pass
        logger.info("Session manager stopped")
    
    async def handle_mcp(self, request: Request):
        """Handle MCP requests"""
        # Extract configuration from query parameters if provided
        if request.url.query:
            params = dict(request.query_params)
            if 'config' in params:
                try:
                    # Decode base64 and parse JSON
                    config_b64 = params['config']
                    config_json = base64.b64decode(config_b64).decode('utf-8')
                    config = json.loads(config_json)
                    logger.debug(f"Applying config: {config}")
                    
                    # Set environment variables from config
                    if 'flowiseaiApiKey' in config:
                        os.environ['FLOWISEAI_API_KEY'] = config['flowiseaiApiKey']
                    if 'flowiseaiUrl' in config:
                        os.environ['FLOWISEAI_URL'] = config['flowiseaiUrl']
                except Exception as e:
                    logger.error(f"Failed to decode config: {e}")
        
        # Get the raw ASGI scope, receive, send
        scope = request.scope
        receive = request.receive
        
        # We need to handle the response properly
        # The session manager will send the response directly
        response_started = False
        
        async def send(message):
            nonlocal response_started
            if message['type'] == 'http.response.start':
                response_started = True
            await request._send(message)
        
        # Handle the request with the session manager
        await self.session_manager.handle_request(scope, receive, send)
        
        # Return empty response as the actual response was sent via send()
        from starlette.responses import Response
        return Response(content=b'', media_type='application/octet-stream')
    
    async def handle_health(self, request: Request):
        """Health check endpoint"""
        return JSONResponse({
            "status": "healthy",
            "service": "flowiseai-mcp",
            "transport": "streamable-http",
            "test_mode": not os.getenv("FLOWISEAI_API_KEY") or os.getenv("FLOWISEAI_API_KEY") == "test-key",
            "endpoints": {
                "mcp": "/mcp",
                "health": "/health"
            }
        })


# Create the MCP app instance
mcp_app = MCPApp()

# Create Starlette app
app = Starlette(
    routes=[
        Route("/mcp", endpoint=mcp_app.handle_mcp, methods=["GET", "POST", "DELETE"]),
        Route("/health", endpoint=mcp_app.handle_health),
        Route("/", endpoint=mcp_app.handle_health),  # Root health check
    ],
    debug=os.getenv('DEBUG', '').lower() in ('true', '1', 'yes'),
    on_startup=[mcp_app.startup],
    on_shutdown=[mcp_app.shutdown]
)


def main():
    """Main entry point for HTTP server"""
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting FlowiseAI MCP HTTP Server")
    logger.info(f"Listening on {host}:{port}")
    logger.info(f"MCP endpoint: http://{host}:{port}/mcp")
    logger.info(f"Health check: http://{host}:{port}/health")
    
    if not os.getenv("FLOWISEAI_API_KEY") or os.getenv("FLOWISEAI_API_KEY") == "test-key":
        logger.info("Running in TEST MODE - ping will work without FlowiseAI connection")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="error" if not os.getenv('DEBUG') else "debug"
    )


if __name__ == "__main__":
    main()