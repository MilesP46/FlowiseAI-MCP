#!/bin/bash

echo "========================================="
echo "🔍 Smithery.ai Deployment Verification"
echo "========================================="
echo ""

# Check required files
echo "📁 Required Files in Repository Root:"
echo "-------------------------------------"
for file in Dockerfile smithery.yaml README.md requirements.txt pyproject.toml; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file MISSING!"
    fi
done
echo ""

# Check git status
echo "📤 Git Push Status:"
echo "-------------------"
UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l)
if [ "$UNPUSHED" -gt 0 ]; then
    echo "⚠️  WARNING: You have $UNPUSHED unpushed commits!"
    echo ""
    echo "Unpushed commits:"
    git log origin/main..HEAD --oneline
    echo ""
    echo "Files that need to be pushed:"
    git diff --name-only origin/main..HEAD
    echo ""
    echo "🚨 ACTION REQUIRED:"
    echo "   Run: git push origin main"
    echo ""
else
    echo "✅ All commits are pushed to GitHub"
    echo ""
fi

# Show smithery.yaml content
echo "📋 smithery.yaml Configuration:"
echo "-------------------------------"
if [ -f "smithery.yaml" ]; then
    echo "Version: $(grep "^version:" smithery.yaml)"
    echo "Command: $(grep -A1 "command:" smithery.yaml | tail -1)"
    echo ""
else
    echo "❌ smithery.yaml not found!"
    echo ""
fi

# Final status
echo "========================================="
if [ "$UNPUSHED" -gt 0 ]; then
    echo "❌ NOT READY: Push your commits first!"
    echo ""
    echo "Run these commands:"
    echo "  1. git push origin main"
    echo "  2. Wait 30 seconds for GitHub to update"
    echo "  3. Try deploying on Smithery.ai again"
else
    echo "✅ READY for Smithery.ai deployment!"
    echo ""
    echo "Next steps:"
    echo "  1. Go to https://smithery.ai/"
    echo "  2. Select your repository"
    echo "  3. Configure FLOWISEAI_URL and FLOWISEAI_API_KEY"
    echo "  4. Deploy!"
fi
echo "========================================="