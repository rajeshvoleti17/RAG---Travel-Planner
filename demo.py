#!/usr/bin/env python3
"""
Demo script for Travel Planner RAG System
Showcases the main features and capabilities
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

def demo_rag_pipeline():
    """Demonstrate the RAG pipeline functionality"""
    print("🎯 RAG Pipeline Demo")
    print("=" * 40)
    
    try:
        from rag.rag_pipeline import TravelRAGPipeline
        from data.document_processor import TravelDocumentProcessor
        
        # Initialize components
        rag_pipeline = TravelRAGPipeline()
        doc_processor = TravelDocumentProcessor()
        
        # Add sample documents
        print("📚 Adding sample travel documents...")
        sample_docs = doc_processor.create_sample_travel_documents()
        result = rag_pipeline.add_travel_documents(sample_docs)
        print(f"✅ Added {result['documents_added']} documents")
        
        # Demo queries
        demo_queries = [
            "What are the best things to do in Paris?",
            "Tell me about Tokyo's food scene",
            "How can I travel on a budget?",
            "What should I know about solo travel?"
        ]
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n🔍 Query {i}: {query}")
            result = rag_pipeline.process_query(query)
            print(f"💬 Response: {result['response'][:200]}...")
        
        print("\n✅ RAG Pipeline demo completed!")
        
    except Exception as e:
        print(f"❌ RAG Pipeline demo failed: {e}")

def demo_travel_planning():
    """Demonstrate travel planning functionality"""
    print("\n🗺️ Travel Planning Demo")
    print("=" * 40)
    
    try:
        from rag.rag_pipeline import TravelRAGPipeline
        
        rag_pipeline = TravelRAGPipeline()
        
        # Demo travel plans
        demo_preferences = [
            {
                'destination': 'Paris',
                'budget': 'Mid-range',
                'duration': '5 days',
                'interests': ['Museums', 'Food', 'Culture']
            },
            {
                'destination': 'Tokyo',
                'budget': 'Luxury',
                'duration': '7 days',
                'interests': ['Food', 'Technology', 'Shopping']
            }
        ]
        
        for i, preferences in enumerate(demo_preferences, 1):
            print(f"\n📋 Travel Plan {i}:")
            print(f"Destination: {preferences['destination']}")
            print(f"Budget: {preferences['budget']}")
            print(f"Duration: {preferences['duration']}")
            print(f"Interests: {', '.join(preferences['interests'])}")
            
            result = rag_pipeline.create_travel_plan(preferences)
            print(f"📝 Plan: {result['travel_plan'][:300]}...")
        
        print("\n✅ Travel Planning demo completed!")
        
    except Exception as e:
        print(f"❌ Travel Planning demo failed: {e}")

def demo_destination_search():
    """Demonstrate destination search functionality"""
    print("\n🔍 Destination Search Demo")
    print("=" * 40)
    
    try:
        from rag.rag_pipeline import TravelRAGPipeline
        
        rag_pipeline = TravelRAGPipeline()
        
        # Demo searches
        search_terms = ["Europe", "Asia", "beach destinations"]
        
        for search_term in search_terms:
            print(f"\n🔎 Searching for: {search_term}")
            result = rag_pipeline.search_destinations(search_term)
            print(f"Found {result['count']} destinations:")
            
            for dest in result['destinations']:
                print(f"  📍 {dest.get('destination', 'Unknown')}")
        
        print("\n✅ Destination Search demo completed!")
        
    except Exception as e:
        print(f"❌ Destination Search demo failed: {e}")

def demo_api_endpoints():
    """Demonstrate API endpoint functionality"""
    print("\n🌐 API Endpoints Demo")
    print("=" * 40)
    
    print("Available API endpoints:")
    endpoints = [
        ("POST /chat", "Process travel queries"),
        ("POST /plan", "Create travel plans"),
        ("POST /destination-info", "Get destination information"),
        ("POST /search-destinations", "Search destinations"),
        ("POST /add-documents", "Add travel documents"),
        ("GET /stats", "Get system statistics")
    ]
    
    for endpoint, description in endpoints:
        print(f"  {endpoint}: {description}")
    
    print("\n✅ API Endpoints demo completed!")

def demo_web_interface():
    """Demonstrate web interface functionality"""
    print("\n💻 Web Interface Demo")
    print("=" * 40)
    
    print("Web interface features:")
    features = [
        "💬 Interactive chat interface",
        "🗺️ Travel planning form",
        "🔍 Destination search",
        "📚 Knowledge base management",
        "📊 System statistics"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\nTo start the web interface:")
    print("  python run.py --mode web")
    print("  Then open http://localhost:8501")
    
    print("\n✅ Web Interface demo completed!")

def main():
    """Run the complete demo"""
    print("✈️ Travel Planner RAG System Demo")
    print("=" * 50)
    
    demos = [
        ("RAG Pipeline", demo_rag_pipeline),
        ("Travel Planning", demo_travel_planning),
        ("Destination Search", demo_destination_search),
        ("API Endpoints", demo_api_endpoints),
        ("Web Interface", demo_web_interface)
    ]
    
    for demo_name, demo_func in demos:
        try:
            demo_func()
        except Exception as e:
            print(f"❌ {demo_name} demo failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Demo completed!")
    print("\nTo get started:")
    print("1. Run: python setup.py")
    print("2. Edit .env file with your OpenAI API key")
    print("3. Run: python run.py --mode web")
    print("4. Open http://localhost:8501 in your browser")

if __name__ == "__main__":
    main() 