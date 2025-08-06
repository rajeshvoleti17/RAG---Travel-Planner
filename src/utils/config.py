"""
Configuration utilities for Travel Planner RAG System
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the travel planner RAG system"""
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Database and Storage
    CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH", "./data/embeddings")
    DOCUMENTS_PATH = os.getenv("DOCUMENTS_PATH", "./data/documents")
    
    # Model Configuration
    DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")
    DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", "0.7"))
    
    # API Configuration
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Web Interface
    STREAMLIT_PORT = int(os.getenv("STREAMLIT_PORT", "8501"))
    
    # Vector Store Configuration
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    MAX_RESULTS = int(os.getenv("MAX_RESULTS", "5"))
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get all configuration as a dictionary"""
        return {
            "openai_api_key": cls.OPENAI_API_KEY,
            "chroma_db_path": cls.CHROMA_DB_PATH,
            "documents_path": cls.DOCUMENTS_PATH,
            "default_model": cls.DEFAULT_MODEL,
            "default_temperature": cls.DEFAULT_TEMPERATURE,
            "api_host": cls.API_HOST,
            "api_port": cls.API_PORT,
            "streamlit_port": cls.STREAMLIT_PORT,
            "embedding_model": cls.EMBEDDING_MODEL,
            "max_results": cls.MAX_RESULTS
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate the configuration"""
        errors = []
        
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is not set")
        
        if not os.path.exists(cls.DOCUMENTS_PATH):
            try:
                os.makedirs(cls.DOCUMENTS_PATH, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create documents path: {e}")
        
        if not os.path.exists(cls.CHROMA_DB_PATH):
            try:
                os.makedirs(cls.CHROMA_DB_PATH, exist_ok=True)
            except Exception as e:
                errors.append(f"Cannot create embeddings path: {e}")
        
        if errors:
            print("Configuration errors:")
            for error in errors:
                print(f"  - {error}")
            return False
        
        return True
    
    @classmethod
    def print_config(cls):
        """Print current configuration"""
        config = cls.get_config()
        print("Current Configuration:")
        for key, value in config.items():
            if key == "openai_api_key":
                # Mask API key for security
                masked_value = value[:4] + "*" * (len(value) - 8) + value[-4:] if value else "Not set"
                print(f"  {key}: {masked_value}")
            else:
                print(f"  {key}: {value}") 