#!/bin/bash

# Azure Function Chat API - Setup Script
# This script sets up the local development environment

set -e

echo "🚀 Azure Function Chat API Setup"
echo "================================="
echo ""

# Check Python version
echo "📌 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Python $PYTHON_VERSION found"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate || . .venv/Scripts/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
python -m pip install --upgrade pip
echo "✅ pip upgraded"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements-dev.txt
echo "✅ Dependencies installed"
echo ""

# Check Azure CLI
echo "📌 Checking Azure CLI..."
if command -v az &> /dev/null; then
    echo "✅ Azure CLI found"
else
    echo "⚠️  Azure CLI not found. Install from: https://docs.microsoft.com/cli/azure/install-azure-cli"
fi
echo ""

# Check Azure Functions Core Tools
echo "📌 Checking Azure Functions Core Tools..."
if command -v func &> /dev/null; then
    echo "✅ Azure Functions Core Tools found"
else
    echo "⚠️  Azure Functions Core Tools not found. Install from: https://docs.microsoft.com/azure/azure-functions/functions-run-local"
fi
echo ""

# Check Terraform
echo "📌 Checking Terraform..."
if command -v terraform &> /dev/null; then
    echo "✅ Terraform found"
else
    echo "⚠️  Terraform not found (optional). Install from: https://www.terraform.io/downloads"
fi
echo ""

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v
echo "✅ All tests passed"
echo ""

echo "============================================"
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment: source .venv/bin/activate"
echo "2. Start function locally: func start"
echo "3. Configure Azure credentials for deployment"
echo "4. Review README.md for deployment instructions"
echo ""
echo "Happy coding! 🎉"
