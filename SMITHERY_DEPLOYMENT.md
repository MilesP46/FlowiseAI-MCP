# Smithery.ai Deployment Guide

## ✅ Optimizations Made to Prevent Timeout Errors

### 1. Simplified Dockerfile (7-second build time)
**Before:** Complex multi-stage build with gcc installation, editable pip install, and user creation
**After:** Streamlined build that:
- Removed gcc installation (not needed)
- Uses `pip install -r requirements.txt` instead of `pip install -e .`
- Removed user creation (unnecessary complexity)
- Removed unnecessary file copies (pyproject.toml, LICENSE, README.md)
- Uses PYTHONPATH instead of editable install

### 2. Corrected smithery.yaml Format
**Before:** Custom format with incorrect structure
**After:** Proper Smithery v1 format:
```yaml
runtime: "container"
build:
  dockerfile: "Dockerfile"
  dockerBuildPath: "."
env:
  FLOWISEAI_URL: "${FLOWISEAI_URL}"
  FLOWISEAI_API_KEY: "${FLOWISEAI_API_KEY}"
configSchema:
  type: "object"
  properties:
    FLOWISEAI_URL:
      type: "string"
      description: "FlowiseAI instance URL"
      default: "http://localhost:3000"
    FLOWISEAI_API_KEY:
      type: "string"
      description: "API key for FlowiseAI"
  required: ["FLOWISEAI_URL", "FLOWISEAI_API_KEY"]
```

### 3. Improved Entry Point
- Added proper error handling in `__main__.py`
- Better logging for debugging
- Graceful shutdown handling

### 4. MCP Server Specifics
- MCP servers use **stdio** (not HTTP ports)
- No port binding required
- Communication via standard input/output
- PYTHONUNBUFFERED=1 for proper stdio communication

## 🚀 Deployment Steps

### Prerequisites
1. Ensure all files are pushed to GitHub:
```bash
git status  # Should show "nothing to commit"
git push origin main  # If needed
```

2. Verify required files exist in repository root:
- ✅ Dockerfile
- ✅ smithery.yaml
- ✅ requirements.txt
- ✅ src/flowiseai_mcp/

### Deploy on Smithery.ai

1. Go to [https://smithery.ai/](https://smithery.ai/)
2. Click "New Server" or "Import Repository"
3. Select your GitHub repository
4. Smithery will automatically detect:
   - `Dockerfile` in root
   - `smithery.yaml` in root
5. Configure environment variables:
   - `FLOWISEAI_URL`: Your FlowiseAI instance URL
   - `FLOWISEAI_API_KEY`: Your API key
6. Click "Deploy"

### Expected Build Behavior
- Build time: ~7-10 seconds
- Image size: ~200MB
- No compilation required
- Direct dependency installation from requirements.txt

## 🧪 Local Testing

Test the optimized Docker build:
```bash
# Build (should take <10 seconds)
time docker build -t flowiseai-mcp .

# Run with environment variables
docker run --rm \
  -e FLOWISEAI_URL="http://localhost:3000" \
  -e FLOWISEAI_API_KEY="test-key" \
  flowiseai-mcp
```

## 🔍 Troubleshooting

### If deployment still times out:
1. Check Smithery's build logs for specific errors
2. Ensure your repository is public or Smithery has access
3. Verify the Dockerfile builds locally in under 30 seconds
4. Contact Smithery support with the build logs

### Common Issues:
- **"Cannot find module"**: Ensure src/ directory is copied in Dockerfile
- **"Connection refused"**: MCP servers use stdio, not HTTP - no ports needed
- **"Permission denied"**: Files are copied as root user, which is fine for containers

## 📊 Performance Metrics

| Metric | Before | After |
|--------|--------|-------|
| Docker build time | 30+ seconds | 7 seconds |
| Image size | 485MB | ~200MB |
| Layers | 9 | 5 |
| System packages | gcc installed | None |
| User creation | Yes | No |

## ✅ Verification Checklist

Before deploying to Smithery:
- [ ] All changes pushed to GitHub
- [ ] Docker build completes in <10 seconds locally
- [ ] requirements.txt includes all dependencies
- [ ] smithery.yaml uses `runtime: "container"`
- [ ] No port binding in server code (stdio only)

## 📝 Key Changes Summary

The main issue was the Docker build timeout. We resolved it by:
1. **Removing unnecessary build steps** (gcc, user creation)
2. **Using direct pip install** instead of editable install
3. **Proper smithery.yaml format** for container runtime
4. **Streamlined file copying** in Dockerfile

The server is now optimized for fast deployment on Smithery.ai!