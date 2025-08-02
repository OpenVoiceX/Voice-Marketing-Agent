"""
Setup script to ensure the testing environment is ready.
Run this before running tests for the first time.
"""
import os
import sys
import subprocess

def install_test_dependencies():
    """Install test dependencies."""
    print("📦 Installing test dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"], check=True)
        print("✅ Test dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install test dependencies")
        return False
    return True

def create_test_directories():
    """Create necessary test directories."""
    print("📁 Creating test directories...")
    directories = [
        "tests",
        "tests/test_models",
        "tests/test_services", 
        "tests/test_api",
        "tests/test_agents",
        "tests/utils"
    ]
    
    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        # Create __init__.py files for proper Python packages
        init_file = os.path.join(dir_path, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, "w") as f:
                f.write("# Test package\n")
    
    print("✅ Test directories created!")

def check_environment():
    """Check if the environment is ready for testing."""
    print("🔍 Checking environment...")
    
    # Check if we're in the backend directory
    if not os.path.exists("src"):
        print("❌ Please run this script from the backend directory")
        return False
    
    # Check if main application files exist
    required_files = [
        "src/main.py",
        "src/core/database.py",
        "src/models/agent.py"
    ]
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"❌ Required file missing: {file_path}")
            return False
    
    print("✅ Environment looks good!")
    return True

def main():
    """Main setup function."""
    print("🧪 Setting up Voice Marketing Agents Test Environment")
    print("=" * 50)
    
    if not check_environment():
        sys.exit(1)
    
    create_test_directories()
    
    if not install_test_dependencies():
        sys.exit(1)
    
    print("\n🎉 Test environment setup complete!")
    print("\nNext steps:")
    print("1. Run tests: pytest")
    print("2. Run with coverage: pytest --cov=src")
    print("3. Use Makefile commands: make test, make test-coverage")

if __name__ == "__main__":
    main()