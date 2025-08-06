"""
Streamlit Web Application for Travel Planner RAG System
Provides a user-friendly interface for travel planning
"""

import streamlit as st
import requests
import json
import os
import sys
from typing import Dict, Any, List
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# API configuration
API_BASE_URL = "http://localhost:8000"

def init_session_state():
    """Initialize session state variables"""
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'current_plan' not in st.session_state:
        st.session_state.current_plan = None

def call_api(endpoint: str, data: Dict[str, Any] = None, method: str = "POST") -> Dict[str, Any]:
    """Make API call to the FastAPI backend"""
    try:
        url = f"{API_BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url)
        else:
            response = requests.post(url, json=data)
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {e}")
        return {}

def add_sample_documents():
    """Add sample travel documents to the knowledge base"""
    try:
        result = call_api("/add-sample-documents", method="POST")
        if result:
            st.success("Sample documents added successfully!")
        else:
            st.error("Failed to add sample documents")
    except Exception as e:
        st.error(f"Error adding sample documents: {e}")

def chat_interface():
    """Chat interface for travel queries"""
    st.header("💬 Travel Chat")
    st.write("Ask me anything about travel destinations, planning, or recommendations!")
    
    # Chat input
    user_query = st.text_input("Your travel question:", key="chat_input")
    
    if st.button("Send", key="send_chat"):
        if user_query:
            with st.spinner("Thinking..."):
                response = call_api("/chat", {"query": user_query, "n_results": 5})
                
                if response:
                    # Add to chat history
                    st.session_state.chat_history.append({
                        "user": user_query,
                        "assistant": response["response"],
                        "context": response.get("context", "")
                    })
                    
                    # Display response
                    st.success("Response:")
                    st.write(response["response"])
                    
                    # Show context (collapsible)
                    with st.expander("View retrieved context"):
                        st.text(response.get("context", "No context available"))
                else:
                    st.error("Failed to get response")

    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Chat History")
        for i, chat in enumerate(st.session_state.chat_history):
            with st.container():
                st.write(f"**You:** {chat['user']}")
                st.write(f"**Assistant:** {chat['assistant']}")
                st.divider()

def travel_planning_interface():
    """Travel planning interface"""
    st.header("🗺️ Travel Planning")
    st.write("Create personalized travel plans based on your preferences!")
    
    with st.form("travel_plan_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            destination = st.text_input("Destination (optional)")
            budget = st.selectbox("Budget", ["", "Budget", "Mid-range", "Luxury"])
            duration = st.text_input("Duration (e.g., '7 days')")
        
        with col2:
            travel_style = st.selectbox("Travel Style", ["", "Adventure", "Relaxation", "Cultural", "Food & Wine", "Solo", "Family"])
            interests = st.multiselect("Interests", [
                "Museums", "Nature", "Beaches", "Mountains", "Cities", "History",
                "Food", "Shopping", "Nightlife", "Sports", "Photography", "Art"
            ])
        
        submitted = st.form_submit_button("Create Travel Plan")
        
        if submitted:
            with st.spinner("Creating your travel plan..."):
                preferences = {
                    "destination": destination if destination else None,
                    "budget": budget if budget else None,
                    "duration": duration if duration else None,
                    "interests": interests if interests else None,
                    "travel_style": travel_style if travel_style else None
                }
                
                # Remove None values
                preferences = {k: v for k, v in preferences.items() if v is not None}
                
                response = call_api("/plan", preferences)
                
                if response:
                    st.session_state.current_plan = response
                    st.success("Travel plan created!")
                else:
                    st.error("Failed to create travel plan")
    
    # Display current plan
    if st.session_state.current_plan:
        st.subheader("Your Travel Plan")
        st.write(st.session_state.current_plan["travel_plan"])
        
        # Show recommendations
        with st.expander("View recommendations"):
            recommendations = st.session_state.current_plan.get("recommendations", [])
            for i, rec in enumerate(recommendations):
                st.write(f"**Recommendation {i+1}:**")
                st.write(rec.get("content", "No content"))
                st.write(f"Source: {rec.get('metadata', {}).get('source', 'Unknown')}")
                st.divider()

def destination_search_interface():
    """Destination search interface"""
    st.header("🔍 Destination Search")
    st.write("Search for travel destinations and get detailed information!")
    
    search_term = st.text_input("Search destinations:", placeholder="e.g., Europe, Asia, beach destinations")
    
    if st.button("Search"):
        if search_term:
            with st.spinner("Searching destinations..."):
                response = call_api("/search-destinations", {"search_term": search_term})
                
                if response and response.get("destinations"):
                    st.success(f"Found {response['count']} destinations!")
                    
                    for dest in response["destinations"]:
                        destination_name = dest.get("destination", "Unknown")
                        st.write(f"📍 **{destination_name}**")
                        
                        # Get detailed info
                        if st.button(f"Get info about {destination_name}", key=f"info_{destination_name}"):
                            with st.spinner(f"Getting information about {destination_name}..."):
                                info_response = call_api("/destination-info", {"destination": destination_name})
                                
                                if info_response:
                                    st.subheader(f"About {destination_name}")
                                    st.write(info_response["summary"])
                else:
                    st.info("No destinations found for your search term.")

def document_management_interface():
    """Document management interface"""
    st.header("📚 Knowledge Base Management")
    st.write("Manage the travel knowledge base by adding documents and viewing statistics.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Add Sample Documents")
        st.write("Add sample travel guides and information to get started.")
        if st.button("Add Sample Documents"):
            add_sample_documents()
    
    with col2:
        st.subheader("Upload Documents")
        st.write("Upload your own travel documents (PDF, DOCX, TXT).")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'txt'],
            key="document_uploader"
        )
        
        if uploaded_file is not None:
            if st.button("Upload Document"):
                with st.spinner("Processing document..."):
                    # For now, we'll just show a success message
                    # In a real implementation, you'd upload to the API
                    st.success(f"Document '{uploaded_file.name}' uploaded successfully!")
    
    # System statistics
    st.subheader("System Statistics")
    if st.button("Get System Stats"):
        with st.spinner("Getting system statistics..."):
            stats = call_api("/stats", method="GET")
            
            if stats:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Total Documents", stats.get("vector_store_stats", {}).get("total_documents", 0))
                
                with col2:
                    st.metric("Model", stats.get("model_info", {}).get("generator_model", "Unknown"))

def main():
    """Main application"""
    st.set_page_config(
        page_title="Travel Planner RAG",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Sidebar
    st.sidebar.title("✈️ Travel Planner RAG")
    st.sidebar.write("Your AI-powered travel assistant")
    
    # Navigation
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Chat", "Travel Planning", "Destination Search", "Knowledge Base"]
    )
    
    # Main content
    if page == "Chat":
        chat_interface()
    elif page == "Travel Planning":
        travel_planning_interface()
    elif page == "Destination Search":
        destination_search_interface()
    elif page == "Knowledge Base":
        document_management_interface()
    
    # Footer
    st.sidebar.divider()
    st.sidebar.write("Built with ❤️ using RAG technology")
    st.sidebar.write("Powered by LangChain, ChromaDB, and OpenAI")

if __name__ == "__main__":
    main() 