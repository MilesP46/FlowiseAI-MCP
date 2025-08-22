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

# Create the MCP server and session manager globally
mcp_server_instance = FlowiseAIMCPServer()
mcp_server = mcp_server_instance.server  # Access the server attribute

# Create the session manager with our MCP server
session_manager = StreamableHTTPSessionManager(
    app=mcp_server,
    json_response=False,
    stateless=False  # Keep state between requests in a session
)


async def handle_mcp(scope, receive, send):
    """Handle MCP endpoint for Streamable HTTP protocol"""
    logger.debug(f"MCP request: {scope.get('method')} {scope.get('path')}")
    
    # Extract and apply configuration from query parameters
    # Smithery.ai passes config as base64-encoded JSON in 'config' parameter
    query_string = scope.get('query_string', b'').decode('utf-8')
    if query_string:
        from urllib.parse import parse_qs
        params = parse_qs(query_string)
        
        if 'config' in params:
            try:
                # Decode base64 and parse JSON
                config_b64 = params['config'][0]
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
    
    # Use the session manager to handle the request
    await session_manager.handle_request(scope, receive, send)


async def handle_health(request: Request):
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


# Background task to run the session manager
async def run_session_manager():
    """Run the session manager"""
    async with session_manager.run():
        # Keep running until shutdown
        await asyncio.Event().wait()


# Create Starlette app
app = Starlette(
    routes=[
        Route("/mcp", endpoint=handle_mcp, methods=["GET", "POST", "DELETE"]),
        Route("/health", endpoint=handle_health),
        Route("/", endpoint=handle_health),  # Root health check
    ],
    debug=os.getenv('DEBUG', '').lower() in ('true', '1', 'yes'),
    on_startup=[lambda: asyncio.create_task(run_session_manager())]
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