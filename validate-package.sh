#!/bin/bash

# Test Deployment Package Script
# This script validates the deployment package before uploading to Azure

set -e

echo "🧪 Validating Azure Function Deployment Package"
echo "=============================================="
echo ""

# Check if function-app.zip exists
if [ ! -f "function-app.zip" ]; then
    echo "❌ function-app.zip not found"
    echo "Run 'make az-package' first to create the deployment package"
    exit 1
fi

echo "✅ Package found: function-app.zip"
echo ""

# Check package size
SIZE=$(du -h function-app.zip | cut -f1)
SIZE_BYTES=$(stat -f%z function-app.zip 2>/dev/null || stat -c%s function-app.zip 2>/dev/null)
echo "📦 Package size: $SIZE ($SIZE_BYTES bytes)"

# Warn if package is too large
if [ $SIZE_BYTES -gt 104857600 ]; then  # 100MB
    echo "⚠️  WARNING: Package is larger than 100MB"
    echo "Consider excluding more files or using --build-remote true"
fi

if [ $SIZE_BYTES -gt 52428800 ]; then  # 50MB
    echo "⚠️  Package is larger than 50MB - this may slow down deployment"
fi
echo ""

# List contents
echo "📋 Package contents (first 30 files):"
unzip -l function-app.zip | head -32
echo ""

# Check for required files
echo "🔍 Checking for required files..."

REQUIRED_FILES=(
    "function_app.py"
    "host.json"
    "requirements.txt"
)

for file in "${REQUIRED_FILES[@]}"; do
    if unzip -l function-app.zip | grep -q "$file"; then
        echo "✅ $file found"
    else
        echo "❌ $file missing"
        exit 1
    fi
done
echo ""

# Check for files that should NOT be included
echo "🔍 Checking for excluded files..."

EXCLUDED_PATTERNS=(
    ".git/"
    "tests/"
    "__pycache__"
    ".pytest_cache"
    "venv/"
    ".venv/"
    "terraform/"
    "helm/"
    "Dockerfile"
    ".github/"
    "requirements-dev.txt"
)

FOUND_EXCLUDED=0
for pattern in "${EXCLUDED_PATTERNS[@]}"; do
    if unzip -l function-app.zip | grep -q "$pattern"; then
        echo "⚠️  Found excluded pattern: $pattern"
        FOUND_EXCLUDED=1
    fi
done

if [ $FOUND_EXCLUDED -eq 0 ]; then
    echo "✅ No excluded files found in package"
fi
echo ""

# Summary
echo "=============================================="
echo "✅ Package validation complete!"
echo ""
echo "To deploy this package:"
echo "  make az-deploy FUNCTION_APP_NAME=<name> RESOURCE_GROUP=<group>"
echo ""
echo "Or using Azure CLI directly:"
echo "  az functionapp deployment source config-zip \\"
echo "    --resource-group <your-resource-group> \\"
echo "    --name <your-function-app> \\"
echo "    --src function-app.zip \\"
echo "    --build-remote true"
echo ""

