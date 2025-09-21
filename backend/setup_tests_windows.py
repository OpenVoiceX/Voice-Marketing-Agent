"""
Windows-specific setup script for the testing environment.
"""
import os
import sys
import subprocess

def install_dependencies():
    """Install test dependencies."""
    print("📦 Installing test dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "pytest>=8.0.0",
            "pytest-asyncio>=0.24.0", 
            "pytest-mock>=3.14.0",
            "httpx>=0.28.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "isort>=5.13.0",
            "flake8>=6.0.0"
        ], check=True)
        print("✅ Dependencies installed!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def create_test_structure():
    """Create the test directory structure."""
    print("📁 Creating test structure...")
    
    directories = [
        "tests",
        "tests/test_models", 
        "tests/test_api",
        "tests/test_services",
        "test_audio"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        init_file = os.path.join(directory, "__init__.py")
        if not os.path.exists(init_file) and directory.startswith("tests"):
            with open(init_file, "w") as f:
                f.write("# Test package\n")
    
    print("✅ Test structure created!")

def main():
    """Main setup function."""
    print("🧪 Setting up Voice Marketing Agents Testing for Windows")
    print("=" * 55)
    
    if not os.path.exists("src"):
        print("❌ Please run this from the backend directory")
        return 1
    
    create_test_structure()
    
    if not install_dependencies():
        print("⚠️  Install dependencies manually with:")
        print("pip install pytest pytest-asyncio pytest-mock httpx pytest-cov")
        return 1
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Run tests: python run_tests_simple.py")
    print("2. Or use pytest directly: pytest -v")
    print("3. Run specific tests: pytest tests/test_basic.py -v")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())