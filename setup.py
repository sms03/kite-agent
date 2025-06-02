"""
Setup script for Zerodha AI Agent
Run this script to install dependencies and verify the setup
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"   Error: {e.stderr.strip()}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    
    print("✅ Python version is compatible")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        return False
    
    # Install packages
    return run_command("pip install -r requirements.txt", "Installing packages")

def verify_imports():
    """Verify that all modules can be imported"""
    print("🔍 Verifying imports...")
    
    try:
        # Test main imports
        from app.agent import ZerodhaAgent
        from app.utils import TradingUtils
        from app.config import config
        print("✅ All imports successful!")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_tests():
    """Run basic tests to ensure functionality"""
    print("🧪 Running basic tests...")
    
    try:
        # Import and test basic functionality
        from app.agent import ZerodhaAgent
        from app.utils import TradingUtils
        
        # Test utility functions
        assert TradingUtils.format_currency(1234.56) == "₹1,234.56"
        assert TradingUtils.validate_trading_symbol("INFY") == True
        
        # Test agent initialization
        agent = ZerodhaAgent()
        assert agent.agent_config['model'] == 'gemini-2.0-flash-001'
        
        print("✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def show_next_steps():
    """Show user what to do next"""
    print("\n" + "="*50)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*50)
    print("📋 Next Steps:")
    print("1. 🔑 Set up your Zerodha API credentials (when available)")
    print("2. 🚀 Run the application:")
    print("   - Interactive mode: python main.py")
    print("   - Demo mode: python demo.py")
    print("3. 📖 Check README.md for detailed usage instructions")
    print("\n💡 Note: Currently using placeholder data.")
    print("   Real trading requires Zerodha API tools integration.")
    print("="*50)

def main():
    """Main setup function"""
    print("🚀 ZERODHA AI AGENT - SETUP WIZARD")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies!")
        sys.exit(1)
    
    # Verify imports
    if not verify_imports():
        print("❌ Import verification failed!")
        sys.exit(1)
    
    # Run tests
    if not run_tests():
        print("❌ Tests failed!")
        sys.exit(1)
    
    # Show next steps
    show_next_steps()

if __name__ == "__main__":
    main()
