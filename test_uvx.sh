#!/bin/bash

# Test script to verify the MCP server works with uvx (as it would on smithery.ai)

echo "Testing FlowiseAI-MCP with uvx..."
echo "================================="
echo ""

# Set test environment variables
export FLOWISEAI_URL="http://localhost:3000"
export FLOWISEAI_API_KEY="test-key"

# Test 1: Check if the server starts without output interference
echo "Test 1: Checking server initialization..."
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "0.1.0", "clientInfo": {"name": "test", "version": "1.0.0"}}, "id": 1}' | \
    uvx --from . flowiseai-mcp 2>/dev/null | head -1 | python3 -m json.tool > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Server initialization successful (valid JSON response)"
else
    echo "✗ Server initialization failed (invalid or no JSON response)"
    echo "  Debug: Running with error output..."
    echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "0.1.0", "clientInfo": {"name": "test", "version": "1.0.0"}}, "id": 1}' | \
        uvx --from . flowiseai-mcp 2>&1 | head -5
fi

echo ""

# Test 2: Check with DEBUG mode
echo "Test 2: Testing with DEBUG mode enabled..."
export DEBUG=true
echo '{"jsonrpc": "2.0", "method": "initialize", "params": {"protocolVersion": "0.1.0", "clientInfo": {"name": "test", "version": "1.0.0"}}, "id": 1}' | \
    timeout 2 uvx --from . flowiseai-mcp 2>/tmp/debug.log | head -1 | python3 -m json.tool > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✓ Server works with DEBUG mode"
    echo "  Debug logs captured to stderr (not interfering with stdout)"
else
    echo "✗ DEBUG mode may be interfering with MCP protocol"
fi

echo ""
echo "Test complete!"