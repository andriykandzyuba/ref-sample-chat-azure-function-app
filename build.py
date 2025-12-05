#!/usr/bin/env python3
"""
Build and deployment script for Azure Function Chat API
Replaces Makefile with Python-based task runner
"""

import argparse
import os
import subprocess
import sys
import shutil
import zipfile
from pathlib import Path
from typing import List, Optional


class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(message: str):
    """Print a formatted header message"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{message}{Colors.ENDC}")
    print("=" * len(message))


def print_success(message: str):
    """Print a success message"""
    print(f"{Colors.GREEN}✅ {message}{Colors.ENDC}")


def print_error(message: str):
    """Print an error message"""
    print(f"{Colors.RED}❌ {message}{Colors.ENDC}", file=sys.stderr)


def print_warning(message: str):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠️  {message}{Colors.ENDC}")


def print_info(message: str):
    """Print an info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.ENDC}")


def run_command(cmd: List[str], cwd: Optional[str] = None, check: bool = True) -> subprocess.CompletedProcess:
    my_env = os.environ.copy()
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=check,
            text=True,
            capture_output=False,
            env=my_env,
        )
        return result
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed with exit code {e.returncode}")
        sys.exit(e.returncode)
    except FileNotFoundError as e:
        # More helpful message when an executable is not found (common for 'func', 'az', 'terraform')
        exe = cmd[0] if isinstance(cmd, (list, tuple)) and len(cmd) > 0 else str(cmd)
        print_error(f"Executable not found: {exe}")
        print_error("The command could not be started because the executable was not found on PATH.")
        print_info("Possible fixes:")
        print_info("- Ensure the required tool is installed and available on your PATH.")
        print_info("- To check if it's available, run: `where.exe func` (Windows CMD) or `Get-Command func` (PowerShell)")
        print_info("- Install Azure Functions Core Tools on Windows: `choco install azure-functions-core-tools-4` (requires Chocolatey)")
        print_info("- Or install with npm (requires Node.js): `npm i -g azure-functions-core-tools@4 --unsafe-perm true`")
        print_info("- Alternatively, run the function from VS Code with the Azure Functions extension")
        sys.exit(2)


def get_venv_python() -> str:
    """Get the path to the Python executable in the virtual environment"""
    venv_path = Path(".venv")
    if sys.platform == "win32":
        python_path = venv_path / "Scripts" / "python.exe"
    else:
        python_path = venv_path / "bin" / "python"

    if python_path.exists():
        return str(python_path)
    return sys.executable


def get_venv_pip() -> str:
    """Get the path to pip in the virtual environment"""
    venv_path = Path(".venv")
    if sys.platform == "win32":
        pip_path = venv_path / "Scripts" / "pip.exe"
    else:
        pip_path = venv_path / "bin" / "pip"

    if pip_path.exists():
        return str(pip_path)
    return "pip"


def setup():
    """Set up local development environment"""
    print_header("Setting up development environment...")

    # Create virtual environment
    print_info("Creating virtual environment...")
    run_command([sys.executable, "-m", "venv", ".venv"])

    # Upgrade pip
    print_info("Upgrading pip...")
    pip_cmd = get_venv_pip()
    run_command([pip_cmd, "install", "--upgrade", "pip"])

    # Install dependencies
    print_info("Installing dependencies...")
    run_command([pip_cmd, "install", "-r", "requirements-dev.txt"])

    print_success("Setup complete!")
    if sys.platform == "win32":
        print_info("Activate venv with: .venv\\Scripts\\activate")
    else:
        print_info("Activate venv with: source .venv/bin/activate")


def clean():
    """Clean build artifacts and cache"""
    print_header("Cleaning up...")

    patterns = [
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/.pytest_cache",
        "**/.mypy_cache",
        "**/htmlcov",
        ".coverage",
        "coverage.xml",
        "function-app.zip",
        ".python_packages"
    ]

    for pattern in patterns:
        for path in Path(".").glob(pattern):
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"Removed directory: {path}")
                else:
                    path.unlink()
                    print(f"Removed file: {path}")
            except Exception as e:
                print_warning(f"Could not remove {path}: {e}")

    print_success("Cleanup complete!")


def test():
    """Run tests"""
    print_header("Running tests...")
    python_cmd = get_venv_python()
    run_command([python_cmd, "-m", "pytest", "tests/", "-v"])
    print_success("Tests passed!")


def coverage():
    """Run tests with coverage report"""
    print_header("Running tests with coverage...")
    python_cmd = get_venv_python()
    run_command([
        python_cmd, "-m", "pytest", "tests/", "-v",
        "--cov=function_app",
        "--cov-report=html",
        "--cov-report=term"
    ])
    print_success("Coverage report generated in htmlcov/index.html")


def lint():
    """Run linting checks"""
    print_header("Running linting checks...")
    python_cmd = get_venv_python()

    # Run flake8 for critical errors
    print_info("Running flake8 (critical errors)...")
    run_command([
        python_cmd, "-m", "flake8", "function_app.py",
        "--count", "--select=E9,F63,F7,F82",
        "--show-source", "--statistics"
    ])

    # Run flake8 for all errors (non-blocking)
    print_info("Running flake8 (all checks)...")
    run_command([
        python_cmd, "-m", "flake8", "function_app.py",
        "--count", "--exit-zero",
        "--max-complexity=10",
        "--max-line-length=127",
        "--statistics"
    ], check=False)

    # Run mypy
    print_info("Running mypy...")
    run_command([
        python_cmd, "-m", "mypy", "function_app.py",
        "--ignore-missing-imports"
    ])

    print_success("Linting checks passed!")


def format_code():
    """Format code with black"""
    print_header("Formatting code...")
    python_cmd = get_venv_python()
    run_command([python_cmd, "-m", "black", "."])
    print_success("Code formatted!")


def func_start():
    """Start Azure Function locally"""
    print_header("Starting Azure Function locally...")
    run_command(["func", "start"])


def az_package():
    """Create deployment package for Azure"""
    print_header("Creating deployment package...")

    # Remove existing package
    package_path = Path("function-app.zip")
    if package_path.exists():
        package_path.unlink()
        print_info("Removed existing package")

    # Install dependencies
    print_info("Installing dependencies...")
    packages_dir = Path(".python_packages/lib/site-packages")
    packages_dir.mkdir(parents=True, exist_ok=True)

    pip_cmd = get_venv_pip()
    run_command([
        pip_cmd, "install",
        "--target", str(packages_dir),
        "-r", "requirements.txt"
    ])

    # Create zip package
    print_info("Creating zip package...")

    # Patterns to exclude
    exclude_patterns = [
        ".git",
        "tests",
        "__pycache__",
        ".pytest_cache",
        "venv",
        ".venv",
        ".vscode",
        "terraform",
        "helm",
        "Dockerfile",
        ".github",
        "requirements-dev.txt",
        ".md"
    ]

    def should_exclude(file_path: str) -> bool:
        """Check if a file should be excluded from the package"""
        path_str = file_path.replace("\\", "/")
        for pattern in exclude_patterns:
            if pattern in path_str:
                return True
        return False

    with zipfile.ZipFile("function-app.zip", "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk("."):
            # Filter out excluded directories
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d))]

            for file in files:
                file_path = os.path.join(root, file)
                if not should_exclude(file_path) and file != "function-app.zip":
                    arcname = os.path.relpath(file_path, ".")
                    zipf.write(file_path, arcname)

    # Get package size
    size_bytes = package_path.stat().st_size
    size_mb = size_bytes / (1024 * 1024)

    print_success(f"Package created: function-app.zip ({size_mb:.2f} MB)")

    if size_mb > 100:
        print_warning("Package is larger than 100MB - deployment may be slow")
    elif size_mb > 50:
        print_warning("Package is larger than 50MB - consider excluding more files")


def az_deploy(function_app_name: str, resource_group: str):
    """Deploy to Azure Functions using Azure CLI"""
    print_header("Deploying to Azure Functions...")

    # Validate parameters
    if not function_app_name or function_app_name == "your-function-app-name":
        print_error("FUNCTION_APP_NAME not set")
        print_info("Usage: python build.py az-deploy --function-app <name> --resource-group <group>")
        sys.exit(1)

    if not resource_group or resource_group == "your-resource-group":
        print_error("RESOURCE_GROUP not set")
        print_info("Usage: python build.py az-deploy --function-app <name> --resource-group <group>")
        sys.exit(1)

    # Create package first
    az_package()

    # Deploy to Azure
    print_info(f"Deploying to {function_app_name} in {resource_group}...")
    run_command([
        "az", "functionapp", "deployment", "source", "config-zip",
        "--resource-group", resource_group,
        "--name", function_app_name,
        "--src", "function-app.zip",
        "--build-remote", "true"
    ])

    print_success("Deployment complete!")


def tf_init():
    """Initialize Terraform"""
    print_header("Initializing Terraform...")
    run_command(["terraform", "init"], cwd="terraform")
    print_success("Terraform initialized!")


def tf_plan():
    """Run Terraform plan"""
    print_header("Running Terraform plan...")
    run_command(["terraform", "plan"], cwd="terraform")


def tf_apply():
    """Apply Terraform configuration"""
    print_header("Applying Terraform configuration...")
    run_command(["terraform", "apply"], cwd="terraform")
    print_success("Terraform applied!")


def run_all():
    """Run format, lint, and test"""
    print_header("Running all checks...")
    format_code()
    lint()
    test()
    print_success("All checks passed!")


def show_help():
    """Show available commands"""
    help_text = """
Available commands:

  python build.py setup          - Set up local development environment
  python build.py clean          - Clean build artifacts and cache
  python build.py test           - Run tests
  python build.py coverage       - Run tests with coverage report
  python build.py lint           - Run linting checks
  python build.py format         - Format code with black
  python build.py func-start     - Start Azure Function locally
  python build.py az-package     - Create deployment package for Azure
  python build.py az-deploy      - Deploy to Azure Functions using Azure CLI
                                   --function-app <name> --resource-group <group>
  python build.py tf-init        - Initialize Terraform
  python build.py tf-plan        - Run Terraform plan
  python build.py tf-apply       - Apply Terraform configuration
  python build.py all            - Run format, lint, and test

Examples:
  python build.py setup
  python build.py test
  python build.py az-deploy --function-app my-app --resource-group my-rg
"""
    print(help_text)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Build and deployment script for Azure Function Chat API",
        add_help=False
    )
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("--function-app", help="Azure Function App name")
    parser.add_argument("--resource-group", help="Azure Resource Group name")
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")

    args = parser.parse_args()

    if args.help or not args.command:
        show_help()
        return

    commands = {
        "setup": setup,
        "clean": clean,
        "test": test,
        "coverage": coverage,
        "lint": lint,
        "format": format_code,
        "func-start": func_start,
        "az-package": az_package,
        "tf-init": tf_init,
        "tf-plan": tf_plan,
        "tf-apply": tf_apply,
        "all": run_all,
        "help": show_help,
    }

    if args.command == "az-deploy":
        function_app = args.function_app or os.environ.get("FUNCTION_APP_NAME", "your-function-app-name")
        resource_group = args.resource_group or os.environ.get("RESOURCE_GROUP", "your-resource-group")
        az_deploy(function_app, resource_group)
    elif args.command in commands:
        commands[args.command]()
    else:
        print_error(f"Unknown command: {args.command}")
        show_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

