#!/usr/bin/env python3
"""Test script for smithery.ai connectivity check"""

import sys
import json
import asyncio
from flowiseai_mcp.server import FlowiseAIMCPServer

async def test_initialization():
    """Test if the server can initialize properly"""
    try:
        # Create server
        server = FlowiseAIMCPServer()
        
        # Send initialization response to stdout
        response = {
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "serverInfo": {
                    "name": "flowiseai-mcp",
                    "version": "1.0.0"
                }
            }
        }
        
        # Output JSON response
        print(json.dumps(response))
        return 0
        
    except Exception as e:
        error_response = {
            "jsonrpc": "2.0",
            "id": 1,
            "error": {
                "code": -32603,
                "message": str(e)
            }
        }
        print(json.dumps(error_response), file=sys.stderr)
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(test_initialization())
    sys.exit(exit_code)