# Azure Function Chat API

> **Complete Documentation** - All-in-one guide for deployment, development, and operations

A production-ready Azure Function App providing a REST API Chat endpoint with complete CI/CD pipeline and Infrastructure as Code (Terraform). Deployed exclusively using Azure CLI for simplicity and efficiency.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#️-architecture)
- [Quick Start](#-quick-start)
- [Build Script (build.py)](#-build-script-buildpy)
- [Deployment](#-deployment)
- [Azure CLI Deployment](#-azure-cli-deployment-details)
- [Infrastructure (Terraform)](#️-infrastructure-terraform)
- [Configuration & Secrets](#-configuration--secrets)
- [Testing](#-testing)
- [Monitoring](#-monitoring)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [Migration Notes](#-migration-notes)

---

## ✨ Features

- **Azure Functions REST API** - Chat endpoint with request logging
- **Health Check Endpoint** - For monitoring and load balancers
- **Comprehensive Testing** - Unit tests with pytest and coverage reports
- **CI/CD Pipeline** - GitHub Actions workflow with automated testing and deployment
- **Infrastructure as Code** - Terraform for Azure resource provisioning
- **Azure CLI Deployment** - Direct zip deployment to Azure Functions
- **Cross-Platform Build Tool** - Python-based build.py script (replaces Makefile)
- **Secrets Management** - Azure Key Vault integration
- **Monitoring** - Application Insights integration
- **No Docker Required** - Simplified deployment without containers

---

## 🏗️ Architecture

### Components

1. **Azure Function App** - Serverless Python 3.11 application
2. **Azure Storage Account** - Required for Azure Functions runtime
3. **App Service Plan** - Hosting plan for the Function App
4. **Application Insights** - Monitoring and logging
5. **Azure Key Vault** - Secrets and certificate management

### Deployment Flow

```
Git Push → GitHub Actions → Tests → Terraform (Infrastructure)
                              ↓
                         Build Package → Azure CLI → Azure Functions
                              ↓
                         Smoke Tests
```

### API Endpoints

#### POST /api/chat
Chat endpoint that accepts JSON payloads and logs requests.

**Request:**
```json
{
  "message": "Hello, Azure!",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "status": "success",
  "user_id": "user123",
  "message_received": "Hello, Azure!",
  "response": "Echo: Hello, Azure!",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### GET /api/health
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Azure CLI** - [Install Guide](https://docs.microsoft.com/cli/azure/install-azure-cli)
- **Azure Functions Core Tools** - [Install Guide](https://docs.microsoft.com/azure/azure-functions/functions-run-local)
- **Git** - [Download](https://git-scm.com/downloads)
- **Terraform 1.0+** (optional) - [Download](https://www.terraform.io/downloads)

### 5-Minute Setup

```bash
# 1. Clone the repository
git clone <repository-url>
cd azure-function-chat-api

# 2. Setup environment (creates venv and installs dependencies)
python build.py setup

# 3. Activate virtual environment
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 4. Start function locally
python build.py func-start
```

# Test the API

```bash
# Health check
curl http://localhost:7071/api/health

# Chat API (examples for different shells)

# 1) Bash / macOS / Linux (recommended)
curl -X POST 'http://localhost:7071/api/chat' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Hello","user_id":"test"}'

# 2) PowerShell (recommended on Windows)
Invoke-RestMethod -Method Post -Uri 'http://localhost:7071/api/chat' \
  -ContentType 'application/json' \
  -Body '{"message":"Hello","user_id":"test"}'

# 3) Windows CMD (use double quotes and escape inner quotes)
curl -X POST "http://localhost:7071/api/chat" -H "Content-Type: application/json" \
  -d "{\"message\":\"Hello\",\"user_id\":\"test\"}"
```

---

## 🛠️ Build Script (build.py)

**Cross-platform Python build tool** that replaces Makefile. Works on Windows, macOS, and Linux.

### Features

- ✅ **Cross-platform** - No need for make, WSL, or Cygwin
- ✅ **Colored output** - Green ✅, Red ❌, Yellow ⚠️ indicators
- ✅ **Smart packaging** - Automatic exclusion of dev files
- ✅ **Environment variables** - Supports FUNCTION_APP_NAME and RESOURCE_GROUP
- ✅ **Error handling** - Clear error messages with suggestions

### Available Commands

```bash
# View all commands
python build.py help

# Development
python build.py setup          # Setup environment
python build.py clean          # Clean artifacts
python build.py test           # Run tests
python build.py coverage       # Test with coverage
python build.py lint           # Run linting
python build.py format         # Format code
python build.py all            # Run all checks
python build.py func-start     # Start locally

# Deployment
python build.py az-package     # Create deployment package
python build.py az-deploy      # Deploy to Azure
  --function-app <name> 
  --resource-group <group>

# Infrastructure
python build.py tf-init        # Initialize Terraform
python build.py tf-plan        # Plan infrastructure
python build.py tf-apply       # Apply infrastructure
```

### Usage Examples

**Local Development:**
```bash
# Format and check code
python build.py format
python build.py lint
python build.py test

# Or run all at once
python build.py all
```

**Deployment:**
```bash
# Using command line arguments
python build.py az-deploy \
  --function-app func-chatapi-prod \
  --resource-group rg-chatapi-prod

# Using environment variables
export FUNCTION_APP_NAME=func-chatapi-prod
export RESOURCE_GROUP=rg-chatapi-prod
python build.py az-deploy
```

---

## 📦 Deployment

### Method 1: GitHub Actions (Automatic CI/CD)

**Recommended for production deployments**

1. **Configure GitHub Secrets** (see [Configuration & Secrets](#-configuration--secrets))
2. **Push to main branch:**
   ```bash
   git push origin main
   ```

The workflow automatically:
- ✅ Runs linting and tests
- ✅ Provisions/updates infrastructure via Terraform
- ✅ Creates deployment package
- ✅ Deploys to Azure Functions
- ✅ Runs smoke tests

### Method 2: Local Deployment with build.py

**Recommended for development/testing**

```bash
python build.py az-deploy \
  --function-app your-function-app \
  --resource-group your-resource-group
```

### Method 3: Manual Azure CLI

```bash
# 1. Create package
pip install --target ./.python_packages/lib/site-packages -r requirements.txt
zip -r function-app.zip . \
  -x "*.git*" "*tests*" "*__pycache__*" "*.pytest_cache*" \
  "*venv*" "*.vscode*" "*terraform*" "*helm*" \
  "*.github*" "*requirements-dev.txt" "*.md"

# 2. Deploy to Azure
az functionapp deployment source config-zip \
  --resource-group your-resource-group \
  --name your-function-app \
  --src function-app.zip \
  --build-remote true

# 3. Configure settings (optional)
az functionapp config appsettings set \
  --resource-group your-resource-group \
  --name your-function-app \
  --settings \
    FUNCTIONS_WORKER_RUNTIME=python \
    PYTHON_VERSION=3.11 \
    ENVIRONMENT=production
```

---

## 🔧 Azure CLI Deployment Details

### Package Creation

The deployment package includes:
- ✅ `function_app.py` - Main application code
- ✅ `host.json` - Function host configuration
- ✅ `requirements.txt` - Python dependencies
- ✅ `.python_packages/` - Installed dependencies

The deployment package excludes:
- ❌ Tests and test configurations
- ❌ Development dependencies
- ❌ Documentation files (*.md)
- ❌ Git history
- ❌ Virtual environments
- ❌ Terraform/Helm configurations

### Remote Build

Using `--build-remote true` means:
1. Azure extracts the zip package
2. Installs Python dependencies on Azure infrastructure
3. Builds native extensions for target environment
4. Optimizes deployment for production

**Benefits:**
- Smaller upload size
- Correct binary compatibility
- Faster parallel builds on Azure

### Package Validation

```bash
# Create and validate package
python build.py az-package
./validate-package.sh
```

The validation script checks:
- Package size (warns if > 50MB or > 100MB)
- Required files present
- No excluded files included

---

## 🏗️ Infrastructure (Terraform)

### Quick Setup

```bash
# Initialize Terraform
python build.py tf-init

# Or manually
cd terraform
terraform init
```

### Configure Variables

Copy and customize the example file:
```bash
cp terraform/terraform.tfvars.example terraform/terraform.tfvars
# Edit terraform.tfvars with your values
```

### Deploy Infrastructure

```bash
# Using build.py
python build.py tf-plan   # Preview changes
python build.py tf-apply  # Apply changes

# Or manually
cd terraform
terraform plan
terraform apply
```

### Infrastructure Components

Terraform creates:
- ✅ Resource Group
- ✅ Storage Account
- ✅ App Service Plan (Linux)
- ✅ Function App with managed identity
- ✅ Application Insights
- ✅ Key Vault with access policies

**Removed components** (no longer used):
- ❌ Azure Container Registry
- ❌ Azure Kubernetes Service (AKS)

### Required Terraform Variables

```hcl
resource_group_name         = "rg-chatapi-prod"
location                    = "eastus"
storage_account_name        = "stchatapiprod"       # Must be globally unique
app_service_plan_name       = "asp-chatapi-prod"
function_app_name           = "func-chatapi-prod"   # Must be globally unique
application_insights_name   = "appi-chatapi-prod"
key_vault_name             = "kv-chatapi-prod"      # Must be globally unique
environment                = "production"
```

---

## 🔐 Configuration & Secrets

### Required GitHub Secrets

#### Azure Authentication
- `AZURE_CREDENTIALS` - Service principal JSON:
  ```json
  {
    "clientId": "<client-id>",
    "clientSecret": "<client-secret>",
    "subscriptionId": "<subscription-id>",
    "tenantId": "<tenant-id>"
  }
  ```

#### Terraform
- `ARM_CLIENT_ID` - Azure client ID
- `ARM_CLIENT_SECRET` - Azure client secret
- `ARM_SUBSCRIPTION_ID` - Azure subscription ID
- `ARM_TENANT_ID` - Azure tenant ID

#### Terraform Backend
- `TF_BACKEND_RESOURCE_GROUP` - Backend resource group
- `TF_BACKEND_STORAGE_ACCOUNT` - Backend storage account
- `TF_BACKEND_CONTAINER` - Backend container name
- `TF_BACKEND_KEY` - State file key

#### Optional
- `AZURE_FUNCTION_KEY` - For smoke tests

### Required GitHub Variables

- `AZURE_FUNCTIONAPP_NAME` - Function App name
- `AZURE_RESOURCE_GROUP` - Resource group name
- `STORAGE_ACCOUNT_NAME` - Storage account name
- `APP_SERVICE_PLAN_NAME` - App Service Plan name
- `APPLICATION_INSIGHTS_NAME` - Application Insights name
- `KEY_VAULT_NAME` - Key Vault name

### Setup Guide

**1. Create Azure Service Principal:**
```bash
az ad sp create-for-rbac --name "github-actions-chatapi" --role contributor \
  --scopes /subscriptions/{subscription-id} \
  --sdk-auth
```

**2. Get Function App Key:**
```bash
az functionapp keys list \
  --name <your-function-app> \
  --resource-group <your-resource-group>
```

**3. Configure in GitHub:**
- Go to repository Settings → Secrets and variables → Actions
- Add secrets and variables listed above

---

## 🧪 Testing

### Running Tests

```bash
# Using build.py (recommended)
python build.py test           # Run all tests
python build.py coverage       # With coverage report
python build.py lint           # Run linting checks
python build.py format         # Format code
python build.py all            # Run all checks

# Using pytest directly
pytest
pytest --cov=function_app --cov-report=html
pytest tests/test_chat_api.py -v
```

### Test Structure

```
tests/
├── __init__.py
├── conftest.py           # Pytest fixtures
└── test_chat_api.py      # API tests
```

### Writing Tests

Follow AAA pattern (Arrange, Act, Assert):

```python
def test_chat_api_with_valid_message():
    """Test chat API with a valid message"""
    # Arrange
    req = func.HttpRequest(
        method='POST',
        url='/api/chat',
        body=json.dumps({'message': 'Hello'}).encode('utf-8')
    )
    
    # Act
    response = chat_api(req)
    
    # Assert
    assert response.status_code == 200
```

### CI/CD Testing

GitHub Actions automatically runs:
1. Flake8 linting (critical errors)
2. Mypy type checking
3. Pytest unit tests with coverage
4. Smoke tests after deployment

---

## 📊 Monitoring

### Application Insights

All logs automatically sent to Application Insights.

**View in Azure Portal:**
1. Navigate to Application Insights resource
2. Go to "Logs" or "Live Metrics"
3. Query logs using KQL

**Example KQL Query:**
```kql
traces
| where message contains "chat"
| order by timestamp desc
| take 100
```

### Azure CLI Monitoring

```bash
# View live logs
az functionapp log tail \
  --name <function-app-name> \
  --resource-group <resource-group>

# List app settings
az functionapp config appsettings list \
  --name <function-app-name> \
  --resource-group <resource-group>

# Restart function
az functionapp restart \
  --name <function-app-name> \
  --resource-group <resource-group>
```

### Health Checks

```bash
# Check health endpoint
curl https://<function-app-name>.azurewebsites.net/api/health

# Expected response
{"status":"healthy","timestamp":"2024-01-01T12:00:00Z"}
```

---

## 📁 Project Structure

```
azure-function-chat-api/
├── .github/
│   └── workflows/
│       └── deploy.yml              # CI/CD workflow
├── terraform/
│   ├── main.tf                     # Infrastructure
│   ├── variables.tf                # Variables
│   ├── outputs.tf                  # Outputs
│   └── terraform.tfvars.example    # Example config
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest config
│   └── test_chat_api.py            # Tests
├── .gitignore
├── README.md                       # This file
├── build.py                        # Build script ⭐
├── function_app.py                 # Main application
├── host.json                       # Function config
├── local.settings.json             # Local settings
├── pytest.ini                      # Pytest config
├── requirements-dev.txt            # Dev dependencies
├── requirements.txt                # Production deps
├── setup.sh                        # Environment setup
└── validate-package.sh             # Package validator
```

### Key Files

- **build.py** - Cross-platform build and deployment script
- **function_app.py** - Main Azure Function application
- **host.json** - Azure Functions host configuration
- **requirements.txt** - Production Python dependencies
- **terraform/** - Infrastructure as Code

---

## 🤝 Contributing

### Quick Guide

1. **Fork the repository**
2. **Create feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make changes and test:**
   ```bash
   python build.py format
   python build.py lint
   python build.py test
   ```
4. **Commit with conventional commits:**
   ```bash
   git commit -m "feat: add amazing feature"
   ```
5. **Push and create PR:**
   ```bash
   git push origin feature/amazing-feature
   ```

### Commit Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code formatting
- `refactor:` Code refactoring
- `test:` Adding/updating tests
- `chore:` Maintenance tasks

### Code Standards

- Follow PEP 8 style guide
- Use Black for formatting (88 char line length)
- Add type hints where appropriate
- Write docstrings for functions
- Maintain or improve test coverage

### Pull Request Checklist

- [ ] Code follows project style
- [ ] Tests added for new functionality
- [ ] All tests pass locally
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] No merge conflicts

---

## 🆘 Troubleshooting

### Common Issues

#### Function App not responding

**Check logs:**
```bash
az functionapp log tail --name <app> --resource-group <rg>
```

**Verify configuration:**
```bash
az functionapp config appsettings list --name <app> --resource-group <rg>
```

**Restart function:**
```bash
az functionapp restart --name <app> --resource-group <rg>
```

#### Deployment fails

**Check authentication:**
```bash
az login
az account show
```

**Verify function app exists:**
```bash
az functionapp show --name <app> --resource-group <rg>
```

**Check package size:**
```bash
ls -lh function-app.zip
# Should be < 100MB, ideally < 50MB
```

#### Package too large

**Use remote build (automatic in build.py):**
```bash
az functionapp deployment source config-zip \
  --resource-group <rg> \
  --name <app> \
  --src function-app.zip \
  --build-remote true  # ← This is important
```

**Check package contents:**
```bash
unzip -l function-app.zip | less
```

#### Terraform errors

**Resource name conflicts:**
- Storage accounts, Key Vaults, and Function Apps must be globally unique
- Try adding random suffix or use different naming

**State locking:**
```bash
# If state is locked
terraform force-unlock <lock-id>
```

**Reset state:**
```bash
# CAREFUL: This removes state
rm -rf .terraform terraform.tfstate*
terraform init
```

#### Build.py errors

**Virtual environment issues:**
```bash
# Recreate venv
rm -rf .venv
python build.py setup
```

**Missing dependencies:**
```bash
pip install -r requirements-dev.txt
```

**Permission denied (Unix/macOS):**
```bash
chmod +x build.py
./build.py help
```

### Getting Help

1. Check Application Insights logs
2. Review Azure Monitor metrics
3. Check this README troubleshooting section
4. Create GitHub issue with:
   - Error message
   - Steps to reproduce
   - Environment details
   - Relevant logs

---

## 📝 Migration Notes

### From Docker/Kubernetes to Azure CLI

This project was migrated from Docker/Kubernetes deployment to Azure CLI deployment for simplicity and cost reduction.

#### What Changed

**Removed:**
- ❌ Makefile (replaced by build.py)
- ❌ Dockerfile
- ❌ .dockerignore
- ❌ Azure Container Registry (ACR)
- ❌ Azure Kubernetes Service (AKS)
- ❌ Helm charts (still in repo but not used)

**Added:**
- ✅ build.py - Cross-platform build script
- ✅ Azure CLI zip deployment
- ✅ Direct Azure Functions deployment
- ✅ Simplified documentation

#### Benefits

- 💰 **Lower costs** - No ACR or AKS charges
- 🚀 **Faster deployment** - No Docker build/push
- 🎯 **Simpler architecture** - Single deployment path
- 🌍 **Better cross-platform** - build.py works on Windows
- 📦 **Smaller packages** - Remote build on Azure

#### Command Migration

| Old (Makefile) | New (build.py) |
|----------------|----------------|
| `make setup` | `python build.py setup` |
| `make test` | `python build.py test` |
| `make az-deploy ...` | `python build.py az-deploy --function-app ... --resource-group ...` |

### From Makefile to build.py

**Why the change?**
- Cross-platform compatibility (Windows without WSL)
- Better error handling and messages
- Colored output for better UX
- No external dependencies (just Python)

**Migration is seamless:**
- All commands have equivalent names
- Same functionality, better UX
- Can keep both during transition

---

## 📚 Additional Resources

### Documentation Files (Historical)

These files contain additional details but are summarized in this README:
- `BUILD_SCRIPT.md` - Detailed build.py documentation
- `AZURE_CLI_DEPLOYMENT.md` - Extended Azure CLI guide
- `DEPLOYMENT_CHANGES.md` - Migration history
- `CLEANUP_SUMMARY.md` - Cleanup details
- `MAKEFILE_TO_BUILDPY.md` - Migration guide
- `PROJECT_STRUCTURE.md` - Detailed structure
- `SECRETS_SETUP.md` - Extended secrets guide
- `QUICKSTART.md` - Quick start guide

### External Links

- [Azure Functions Python Guide](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [Azure CLI Reference](https://docs.microsoft.com/cli/azure/)
- [Terraform Azure Provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Python Packaging Guide](https://packaging.python.org/)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🎉 Quick Reference Card

### Essential Commands

```bash
# Setup
python build.py setup

# Development
python build.py all                    # Run all checks
python build.py func-start             # Start locally

# Deployment
python build.py az-deploy \
  --function-app <name> \
  --resource-group <group>

# Infrastructure
python build.py tf-apply               # Deploy infrastructure

# Testing
python build.py test                   # Run tests
python build.py coverage               # With coverage

# Utilities
python build.py help                   # Show all commands
python build.py clean                  # Clean artifacts
```

### Useful Azure CLI Commands

```bash
# Logs
az functionapp log tail --name <app> --resource-group <rg>

# Deploy
az functionapp deployment source config-zip \
  --resource-group <rg> --name <app> \
  --src function-app.zip --build-remote true

# Settings
az functionapp config appsettings set \
  --resource-group <rg> --name <app> \
  --settings KEY=VALUE

# Status
az functionapp show --name <app> --resource-group <rg>
```

---

**Made with ❤️ for Azure Functions**

*Last Updated: December 3, 2025*

