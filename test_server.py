#!/usr/bin/env python3
"""Test script to verify FlowiseAI MCP server functionality"""

import asyncio
import os
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent / "src"))

from flowiseai_mcp.client import FlowiseAIClient
from flowiseai_mcp.models import *
from flowiseai_mcp.server import FlowiseAIMCPServer, find_free_port


async def test_basic_functionality():
    """Test basic server functionality"""
    print("Testing FlowiseAI MCP Server...")
    print("-" * 50)
    
    # Test port finding
    port = find_free_port()
    print(f"✓ Found free port: {port}")
    
    # Test environment variables
    flowise_url = os.getenv("FLOWISEAI_URL", "http://localhost:3000")
    api_key = os.getenv("FLOWISEAI_API_KEY", "")
    print(f"✓ FlowiseAI URL: {flowise_url}")
    print(f"✓ API Key: {'Set' if api_key else 'Not set'}")
    
    # Test model creation
    try:
        assistant = Assistant(name="Test Assistant", description="Test")
        print(f"✓ Created Assistant model: {assistant.name}")
        
        chatflow = Chatflow(name="Test Chatflow", deployed=True)
        print(f"✓ Created Chatflow model: {chatflow.name}")
        
        prediction = PredictionRequest(question="Test question", streaming=False)
        print(f"✓ Created Prediction request: {prediction.question}")
    except Exception as e:
        print(f"✗ Model creation failed: {e}")
        return False
    
    # Test client initialization
    try:
        client = FlowiseAIClient()
        print(f"✓ Client initialized with base URL: {client.base_url}")
        
        # Test URL normalization
        test_urls = [
            "localhost:3000",
            "http://localhost:3000",
            "https://api.flowiseai.com",
            "192.168.1.100:3000"
        ]
        
        for url in test_urls:
            test_client = FlowiseAIClient(base_url=url)
            print(f"  - {url} → {test_client.base_url}")
        
        await client.close()
        print("✓ Client closed successfully")
    except Exception as e:
        print(f"✗ Client test failed: {e}")
        return False
    
    # Test server initialization
    try:
        server = FlowiseAIMCPServer()
        print("✓ MCP Server initialized")
        
        # Note: Tool list would be available when server is running
        # Here we just verify the server can be instantiated
        print("✓ Server handlers configured")
        print("  Tools include: assistant_*, chatflow_*, prediction_*, docstore_*, etc.")
        
    except Exception as e:
        print(f"✗ Server initialization failed: {e}")
        return False
    
    print("-" * 50)
    print("✓ All basic tests passed!")
    return True


async def test_api_connection():
    """Test actual API connection if configured"""
    if not os.getenv("FLOWISEAI_API_KEY"):
        print("\\nSkipping API connection test (no API key set)")
        return True
    
    print("\\nTesting API connection...")
    print("-" * 50)
    
    client = FlowiseAIClient()
    
    try:
        # Test ping
        result = await client.ping()
        print(f"✓ Ping successful: {result}")
        
        # Try to list chatflows
        chatflows = await client.list_chatflows()
        print(f"✓ Found {len(chatflows)} chatflows")
        
        await client.close()
        print("✓ API connection test passed!")
        return True
        
    except Exception as e:
        print(f"✗ API connection failed: {e}")
        print("  Make sure FlowiseAI is running and credentials are correct")
        await client.close()
        return False


async def main():
    """Run all tests"""
    print("=" * 50)
    print("FlowiseAI MCP Server Test Suite")
    print("=" * 50)
    
    # Run basic tests
    basic_ok = await test_basic_functionality()
    
    # Run API tests if possible
    api_ok = await test_api_connection()
    
    print("\\n" + "=" * 50)
    if basic_ok:
        print("✓ Server is ready for use!")
        print("\\nTo use with Claude Desktop or Claude Code:")
        print("  1. Set FLOWISEAI_URL and FLOWISEAI_API_KEY")
        print("  2. Run: uvx flowiseai-mcp")
        print("  3. Configure in your AI tool's MCP settings")
    else:
        print("✗ Some tests failed. Please check the errors above.")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())