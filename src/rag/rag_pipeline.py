"""
Main RAG Pipeline for Travel Planner
Combines retrieval and generation components
"""

from typing import List, Dict, Any, Optional
from .vector_store import TravelVectorStore
from .retriever import TravelRetriever
from .generator import TravelGenerator
import logging

logger = logging.getLogger(__name__)

class TravelRAGPipeline:
    def __init__(self, vector_store_path: str = "./data/embeddings"):
        """Initialize the complete RAG pipeline"""
        self.vector_store = TravelVectorStore(vector_store_path)
        self.retriever = TravelRetriever(self.vector_store)
        self.generator = TravelGenerator()
        
    def process_query(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Process a travel query through the complete RAG pipeline"""
        try:
            # Step 1: Retrieve relevant context
            retrieved_docs = self.retriever.retrieve_relevant_context(query, n_results)
            
            # Step 2: Build context prompt
            context = self.retriever.build_context_prompt(query, retrieved_docs)
            
            # Step 3: Generate response
            response = self.generator.generate_travel_response(query, context)
            
            return {
                'query': query,
                'response': response,
                'retrieved_documents': retrieved_docs,
                'context': context
            }
            
        except Exception as e:
            logger.error(f"Error in RAG pipeline: {e}")
            return {
                'query': query,
                'response': f"I apologize, but I encountered an error while processing your request: {str(e)}",
                'retrieved_documents': [],
                'context': ""
            }
    
    def create_travel_plan(self, user_preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Create a comprehensive travel plan"""
        try:
            # Step 1: Get travel recommendations based on preferences
            recommendations = self.retriever.get_travel_recommendations(user_preferences)
            
            # Step 2: Build context from recommendations
            context = self.retriever.build_context_prompt(
                f"travel plan for {user_preferences.get('destination', 'travel')}",
                recommendations
            )
            
            # Step 3: Generate travel plan
            plan = self.generator.generate_travel_plan(user_preferences, context)
            
            return {
                'user_preferences': user_preferences,
                'travel_plan': plan,
                'recommendations': recommendations,
                'context': context
            }
            
        except Exception as e:
            logger.error(f"Error creating travel plan: {e}")
            return {
                'user_preferences': user_preferences,
                'travel_plan': f"I apologize, but I encountered an error while creating your travel plan: {str(e)}",
                'recommendations': [],
                'context': ""
            }
    
    def get_destination_info(self, destination: str) -> Dict[str, Any]:
        """Get detailed information about a destination"""
        try:
            # Step 1: Retrieve destination-specific information
            destination_docs = self.retriever.get_destination_info(destination)
            
            # Step 2: Build context
            context = self.retriever.build_context_prompt(
                f"information about {destination}",
                destination_docs
            )
            
            # Step 3: Generate destination summary
            summary = self.generator.generate_destination_summary(destination, context)
            
            return {
                'destination': destination,
                'summary': summary,
                'documents': destination_docs,
                'context': context
            }
            
        except Exception as e:
            logger.error(f"Error getting destination info: {e}")
            return {
                'destination': destination,
                'summary': f"I apologize, but I encountered an error while getting information about {destination}: {str(e)}",
                'documents': [],
                'context': ""
            }
    
    def search_destinations(self, search_term: str) -> Dict[str, Any]:
        """Search for destinations matching a search term"""
        try:
            destinations = self.retriever.search_destinations(search_term)
            
            return {
                'search_term': search_term,
                'destinations': destinations,
                'count': len(destinations)
            }
            
        except Exception as e:
            logger.error(f"Error searching destinations: {e}")
            return {
                'search_term': search_term,
                'destinations': [],
                'count': 0,
                'error': str(e)
            }
    
    def add_travel_documents(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Add travel documents to the knowledge base"""
        try:
            self.vector_store.add_documents(documents)
            
            return {
                'status': 'success',
                'documents_added': len(documents),
                'message': f"Successfully added {len(documents)} documents to the travel knowledge base"
            }
            
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return {
                'status': 'error',
                'documents_added': 0,
                'message': f"Error adding documents: {str(e)}"
            }
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system"""
        try:
            vector_stats = self.vector_store.get_collection_stats()
            
            return {
                'vector_store_stats': vector_stats,
                'model_info': {
                    'generator_model': self.generator.model_name,
                    'temperature': self.generator.temperature
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting system stats: {e}")
            return {
                'error': str(e)
            } 