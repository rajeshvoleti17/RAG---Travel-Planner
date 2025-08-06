#!/usr/bin/env python3
"""
Main script to run the Travel Planner RAG System
"""

import os
import sys
import argparse
import subprocess
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from utils.config import Config

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import fastapi
        import uvicorn
        import chromadb
        import sentence_transformers
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup the environment and add sample data"""
    print("🔧 Setting up environment...")
    
    # Create necessary directories
    os.makedirs("./data/documents", exist_ok=True)
    os.makedirs("./data/embeddings", exist_ok=True)
    
    # Validate configuration
    if not Config.validate_config():
        print("❌ Configuration validation failed")
        return False
    
    print("✅ Environment setup complete")
    return True

def run_api_server():
    """Run the FastAPI server"""
    print("🚀 Starting API server...")
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app", 
            "--host", Config.API_HOST, 
            "--port", str(Config.API_PORT),
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 API server stopped")

def run_web_interface():
    """Run the Streamlit web interface"""
    print("🌐 Starting web interface...")
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/web/app.py",
            "--server.port", str(Config.STREAMLIT_PORT)
        ])
    except KeyboardInterrupt:
        print("\n🛑 Web interface stopped")

def add_sample_data():
    """Add sample travel documents to the system"""
    print("📚 Adding sample travel documents...")
    
    # Import here to avoid circular imports
    from rag.rag_pipeline import TravelRAGPipeline
    from data.document_processor import TravelDocumentProcessor
    
    try:
        # Initialize components
        rag_pipeline = TravelRAGPipeline()
        doc_processor = TravelDocumentProcessor()
        
        # Create sample documents
        sample_docs = doc_processor.create_sample_travel_documents()
        
        # Add to knowledge base
        result = rag_pipeline.add_travel_documents(sample_docs)
        
        if result.get('status') == 'success':
            print(f"✅ Added {result['documents_added']} sample documents")
        else:
            print(f"❌ Failed to add sample documents: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Travel Planner RAG System")
    parser.add_argument(
        "--mode", 
        choices=["api", "web", "setup", "sample-data"], 
        default="web",
        help="Run mode: api (FastAPI server), web (Streamlit interface), setup (environment setup), sample-data (add sample documents)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        help="Port for the server (overrides config)"
    )
    
    args = parser.parse_args()
    
    print("✈️ Travel Planner RAG System")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Setup environment
    if not setup_environment():
        return
    
    # Print configuration
    Config.print_config()
    print()
    
    # Run based on mode
    if args.mode == "api":
        run_api_server()
    elif args.mode == "web":
        run_web_interface()
    elif args.mode == "setup":
        print("✅ Setup complete")
    elif args.mode == "sample-data":
        add_sample_data()
    else:
        print("❌ Invalid mode specified")

if __name__ == "__main__":
    main() 