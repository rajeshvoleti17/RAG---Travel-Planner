#!/usr/bin/env python3
"""
Setup script for Travel Planner RAG System
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "data/documents",
        "data/embeddings",
        "static",
        "templates"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created {directory}")

def setup_environment():
    """Setup environment file"""
    print("🔧 Setting up environment...")
    
    env_example = Path("env.example")
    env_file = Path(".env")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("✅ Created .env file from template")
            print("⚠️  Please edit .env file and add your OpenAI API key")
        else:
            print("❌ env.example not found")
            return False
    else:
        print("✅ .env file already exists")
    
    return True

def download_models():
    """Download required models"""
    print("🤖 Downloading models...")
    
    try:
        # This will download the sentence transformer model on first use
        import sentence_transformers
        model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
        print("✅ Sentence transformer model ready")
        return True
    except Exception as e:
        print(f"❌ Failed to download models: {e}")
        return False

def run_tests():
    """Run system tests"""
    print("🧪 Running tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "test_system.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Tests passed")
            return True
        else:
            print("❌ Tests failed")
            print(result.stdout)
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def main():
    """Main setup function"""
    print("✈️ Travel Planner RAG System Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Create directories
    create_directories()
    
    # Setup environment
    if not setup_environment():
        return
    
    # Download models
    if not download_models():
        return
    
    # Run tests
    if not run_tests():
        print("⚠️  Tests failed, but setup completed")
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Edit .env file and add your OpenAI API key")
    print("2. Add sample data: python run.py --mode sample-data")
    print("3. Start the web interface: python run.py --mode web")
    print("4. Or start the API server: python run.py --mode api")
    print("\nFor help, see README.md")

if __name__ == "__main__":
    main() 