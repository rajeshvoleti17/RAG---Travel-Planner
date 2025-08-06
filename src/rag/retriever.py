"""
Retriever for Travel RAG System
Handles document retrieval and context building
"""

from typing import List, Dict, Any, Optional
from .vector_store import TravelVectorStore
import logging

logger = logging.getLogger(__name__)

class TravelRetriever:
    def __init__(self, vector_store: TravelVectorStore):
        """Initialize the retriever with a vector store"""
        self.vector_store = vector_store
        
    def retrieve_relevant_context(self, query: str, n_results: int = 5, 
                                destination_filter: Optional[str] = None,
                                category_filter: Optional[str] = None) -> List[Dict]:
        """Retrieve relevant travel context for a query"""
        try:
            # Build filter dictionary
            filter_dict = {}
            if destination_filter:
                filter_dict["destination"] = destination_filter
            if category_filter:
                filter_dict["category"] = category_filter
            
            # Search vector store
            results = self.vector_store.search(
                query=query,
                n_results=n_results,
                filter_dict=filter_dict if filter_dict else None
            )
            
            logger.info(f"Retrieved {len(results)} relevant documents for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return []
    
    def build_context_prompt(self, query: str, retrieved_docs: List[Dict]) -> str:
        """Build a context prompt from retrieved documents"""
        if not retrieved_docs:
            return f"Query: {query}\n\nNo relevant travel information found."
        
        context_parts = [f"Query: {query}\n\nRelevant travel information:"]
        
        for i, doc in enumerate(retrieved_docs, 1):
            content = doc['content']
            metadata = doc['metadata']
            
            # Add metadata information
            source_info = f"Source: {metadata.get('source', 'Unknown')}"
            destination_info = f"Destination: {metadata.get('destination', 'General')}"
            category_info = f"Category: {metadata.get('category', 'General')}"
            
            context_parts.append(f"\n--- Document {i} ---")
            context_parts.append(f"{source_info} | {destination_info} | {category_info}")
            context_parts.append(f"Content: {content}")
        
        return "\n".join(context_parts)
    
    def get_travel_recommendations(self, user_preferences: Dict[str, Any]) -> List[Dict]:
        """Get personalized travel recommendations based on user preferences"""
        try:
            # Build query from preferences
            query_parts = []
            if user_preferences.get('destination'):
                query_parts.append(f"travel to {user_preferences['destination']}")
            if user_preferences.get('budget'):
                query_parts.append(f"budget {user_preferences['budget']}")
            if user_preferences.get('duration'):
                query_parts.append(f"{user_preferences['duration']} days")
            if user_preferences.get('interests'):
                query_parts.append(f"activities: {', '.join(user_preferences['interests'])}")
            
            query = " ".join(query_parts) if query_parts else "travel recommendations"
            
            # Retrieve relevant documents
            results = self.retrieve_relevant_context(
                query=query,
                n_results=8,
                destination_filter=user_preferences.get('destination')
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting travel recommendations: {e}")
            return []
    
    def search_destinations(self, search_term: str) -> List[Dict]:
        """Search for destinations matching the search term"""
        try:
            results = self.retrieve_relevant_context(
                query=f"destinations and places to visit in {search_term}",
                n_results=10
            )
            
            # Extract unique destinations
            destinations = set()
            for doc in results:
                dest = doc['metadata'].get('destination', '')
                if dest and dest.lower() != 'general':
                    destinations.add(dest)
            
            return [{'destination': dest} for dest in destinations]
            
        except Exception as e:
            logger.error(f"Error searching destinations: {e}")
            return []
    
    def get_destination_info(self, destination: str) -> List[Dict]:
        """Get detailed information about a specific destination"""
        try:
            results = self.retrieve_relevant_context(
                query=f"travel guide and information about {destination}",
                n_results=5,
                destination_filter=destination
            )
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting destination info: {e}")
            return [] 