#!/usr/bin/env python3
"""
Setup script for AI-powered DOCX to JSON Converter
"""

import os
import sys

def setup_environment():
    """Setup environment for the application"""
    print("🤖 AI-POWERED DOCX TO JSON CONVERTER SETUP")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    
    print(f"✅ Python version: {sys.version}")
    
    # Check if OpenAI API key is set
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OpenAI API key found in environment")
    else:
        print("⚠️  OpenAI API key not found in environment")
        print("\nTo use AI features, you need to set your OpenAI API key:")
        print("1. Get your API key from: https://platform.openai.com/api-keys")
        print("2. Set environment variable:")
        print("   Windows: set OPENAI_API_KEY=your-key-here")
        print("   Linux/Mac: export OPENAI_API_KEY=your-key-here")
        print("3. Or edit config.py file")
        
        choice = input("\nDo you want to set the API key now? (y/N): ")
        if choice.lower().startswith('y'):
            new_key = input("Enter your OpenAI API key: ").strip()
            if new_key:
                # Update config.py
                try:
                    with open('config.py', 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Replace the empty key with the new one
                    content = content.replace(
                        "OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')",
                        f"OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '{new_key}')"
                    )
                    
                    with open('config.py', 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print("✅ API key saved to config.py")
                except Exception as e:
                    print(f"❌ Error saving API key: {e}")
    
    # Check required packages
    print("\n📦 Checking required packages...")
    required_packages = [
        'flask', 'flask_cors', 'docx', 'openai', 
        'PyPDF2', 'openpyxl', 'pandas', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            if package == 'docx':
                __import__('docx')
            elif package == 'flask_cors':
                __import__('flask_cors')
            else:
                __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start the server: python app_ai.py")
    print("2. Test with: python test_ai.py")
    print("3. Access API at: http://localhost:5000")
    
    return True

def create_sample_files():
    """Create sample files for testing"""
    print("\n📄 Creating sample files...")
    
    # Sample DOCX content
    sample_docx_content = """
Câu 1: Python là gì?
A. Một ngôn ngữ lập trình
B. Một loài rắn
C. Một hệ điều hành
D. Một trình duyệt web

Câu 2: Flask là gì?
A. Một framework web Python
B. Một cơ sở dữ liệu
C. Một ngôn ngữ lập trình
D. Một IDE
"""
    
    print("Sample files would be created here (requires python-docx)")
    print("You can create your own test files or use existing documents.")

def main():
    """Main setup function"""
    if setup_environment():
        create_sample = input("\nCreate sample test files? (y/N): ")
        if create_sample.lower().startswith('y'):
            create_sample_files()
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()
