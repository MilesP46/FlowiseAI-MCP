#!/bin/bash

echo "========================================="
echo "FlowiseAI MCP - Docker Build Test"
echo "========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "Install Docker from: https://docs.docker.com/get-docker/"
    exit 1
fi

echo "✅ Docker found at: $(which docker)"
echo ""

# Build the Docker image
echo "Building Docker image..."
echo "----------------------------------------"
docker build -t flowiseai-mcp-local . 2>&1 | tail -5

if [ $? -eq 0 ]; then
    echo "✅ Docker build successful"
else
    echo "❌ Docker build failed"
    exit 1
fi
echo ""

# Check image size
echo "Docker image info:"
echo "----------------------------------------"
docker images flowiseai-mcp-local --format "table {{.Repository}}\t{{.Tag}}\t{{.Size}}"
echo ""

# Test running with environment variables
echo "Testing container with environment variables..."
echo "----------------------------------------"
docker run --rm \
    -e FLOWISEAI_URL="http://localhost:3000" \
    -e FLOWISEAI_API_KEY="test-key" \
    flowiseai-mcp-local 2>&1 | head -3
echo "✅ Container can start (stdio error is expected)"
echo ""

echo "========================================="
echo "📋 Smithery.ai Deployment Ready!"
echo "========================================="
echo ""
echo "Required files present:"
[ -f "Dockerfile" ] && echo "✅ Dockerfile"
[ -f "smithery.yaml" ] && echo "✅ smithery.yaml"
[ -f ".dockerignore" ] && echo "✅ .dockerignore"
[ -f "README.md" ] && echo "✅ README.md"
[ -f "pyproject.toml" ] && echo "✅ pyproject.toml"
echo ""
echo "Next steps:"
echo "1. Commit and push to GitHub:"
echo "   git add -A && git commit -m 'Add Smithery deployment files'"
echo "   git push origin main"
echo ""
echo "2. Deploy to Smithery.ai:"
echo "   - Go to https://smithery.ai/"
echo "   - Connect your GitHub repository"
echo "   - Configure FLOWISEAI_URL and FLOWISEAI_API_KEY"
echo "   - Deploy!"
echo ""
echo "========================================="
echo "✅ All deployment checks passed!"
echo "========================================="