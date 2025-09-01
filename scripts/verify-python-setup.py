#!/usr/bin/env python3
"""
Verification script to check Python interpreter and package setup.
Run this script to verify that your Python environment is properly configured.
"""

import sys
import subprocess
import os

def check_python_interpreter():
    """Check which Python interpreter is being used."""
    print("🐍 Python Interpreter Check")
    print(f"Executable: {sys.executable}")
    print(f"Version: {sys.version}")
    print(f"Python Path: {sys.path[0]}")
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in a virtual environment")
    else:
        print("⚠️  Not running in a virtual environment")

def check_fastapi_installation():
    """Check if FastAPI is properly installed."""
    print("\n🚀 FastAPI Installation Check")
    try:
        import fastapi
        print(f"✅ FastAPI version: {fastapi.__version__}")
        return True
    except ImportError as e:
        print(f"❌ FastAPI not found: {e}")
        return False

def check_other_packages():
    """Check other important packages."""
    print("\n📦 Package Installation Check")
    packages = [
        'uvicorn', 'sqlalchemy', 'langchain', 'google.generativeai',
        'pydantic', 'python-dotenv'
    ]
    
    for package in packages:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"✅ {package}: {version}")
        except ImportError:
            print(f"❌ {package}: not found")

def check_python_path():
    """Check Python path for proper module resolution."""
    print("\n🔍 Python Path Check")
    ai_service_src = os.path.join(os.getcwd(), 'services', 'ai-service', 'src')
    if ai_service_src in sys.path:
        print(f"✅ AI service src in Python path: {ai_service_src}")
    else:
        print(f"⚠️  AI service src not in Python path: {ai_service_src}")

def main():
    print("🔧 WarrantyWallet Python Environment Verification")
    print("=" * 50)
    
    check_python_interpreter()
    fastapi_ok = check_fastapi_installation()
    check_other_packages()
    check_python_path()
    
    print("\n" + "=" * 50)
    if fastapi_ok:
        print("✅ Setup looks good! You should be able to import FastAPI without issues.")
    else:
        print("❌ FastAPI is not properly installed. Please check your virtual environment.")
        print("💡 Try running: cd services/ai-service && venv\\Scripts\\activate && pip install -r requirements.txt")

if __name__ == "__main__":
    main()
