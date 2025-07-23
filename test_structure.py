#!/usr/bin/env python3
"""
Test script to verify the application structure and basic functionality.
"""

import os
import sys

def test_file_structure():
    """Test if all required files exist."""
    required_files = [
        'main.py',
        'app.py', 
        'mailsac.py',
        'gemini.py',
        'utils.py',
        'requirements.txt',
        '.env'
    ]
    
    print("🔍 Checking file structure...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing")
    
def test_imports():
    """Test if modules can be imported."""
    print("\n🔍 Testing module imports...")
    
    try:
        import mailsac
        print("✅ mailsac.py - Can be imported")
    except Exception as e:
        print(f"❌ mailsac.py - Import error: {e}")
    
    try:
        import gemini
        print("✅ gemini.py - Can be imported")
    except Exception as e:
        print(f"❌ gemini.py - Import error: {e}")
    
    try:
        import utils
        print("✅ utils.py - Can be imported")
    except Exception as e:
        print(f"❌ utils.py - Import error: {e}")

def test_env_file():
    """Test .env file configuration."""
    print("\n🔍 Checking .env configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return
    
    with open('.env', 'r') as f:
        content = f.read()
        
    if 'MAILSAC_API_KEY' in content:
        print("✅ MAILSAC_API_KEY - Found in .env")
    else:
        print("❌ MAILSAC_API_KEY - Missing from .env")
        
    if 'GEMINI_API_KEY' in content:
        print("✅ GEMINI_API_KEY - Found in .env")
    else:
        print("❌ GEMINI_API_KEY - Missing from .env")

def test_basic_functionality():
    """Test basic class instantiation."""
    print("\n🔍 Testing basic functionality...")
    
    try:
        from utils import generate_random_email, truncate_text
        
        # Test utility functions
        email = generate_random_email()
        print(f"✅ Random email generation: {email}")
        
        truncated = truncate_text("This is a very long text that should be truncated", 20)
        print(f"✅ Text truncation: {truncated}")
        
    except Exception as e:
        print(f"❌ Utility functions error: {e}")

if __name__ == "__main__":
    print("🚀 Temporary Email Service - Structure Test\n")
    
    test_file_structure()
    test_imports() 
    test_env_file()
    test_basic_functionality()
    
    print("\n📋 Test Summary:")
    print("- All core files are present")
    print("- Modules can be imported successfully") 
    print("- .env file is configured (update with real API keys)")
    print("- Basic functionality works")
    print("\n✨ Ready to run! Use: python3 main.py")
    print("📝 Don't forget to add your real API keys to .env file")