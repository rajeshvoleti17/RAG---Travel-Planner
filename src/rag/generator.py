"""
Generator for Travel RAG System
Handles LLM-based response generation for travel queries
"""

import os
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import logging

logger = logging.getLogger(__name__)

class TravelGenerator:
    def __init__(self, model_name: str = "gpt-3.5-turbo", temperature: float = 0.7):
        """Initialize the travel response generator"""
        self.model_name = model_name
        self.temperature = temperature
        
        # Initialize LLM
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("OPENAI_API_KEY not found. Using mock responses.")
            self.llm = None
        else:
            self.llm = ChatOpenAI(
                model_name=model_name,
                temperature=temperature,
                api_key=api_key
            )
    
    def generate_travel_response(self, query: str, context: str) -> str:
        """Generate a travel response using RAG"""
        try:
            if not self.llm:
                return self._generate_mock_response(query, context)
            
            # Create system prompt
            system_prompt = """You are an expert travel planner and guide. Use the provided context to answer travel-related questions accurately and helpfully. 

Your responses should be:
- Informative and detailed
- Practical and actionable
- Friendly and engaging
- Based on the provided context
- Include specific recommendations when possible

If the context doesn't contain enough information, acknowledge this and provide general travel advice."""

            # Create user message with context and query
            user_message = f"Context:\n{context}\n\nUser Question: {query}"
            
            # Generate response
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating travel response: {e}")
            return f"I apologize, but I encountered an error while processing your request. Please try again."
    
    def generate_travel_plan(self, user_preferences: Dict[str, Any], context: str) -> str:
        """Generate a comprehensive travel plan"""
        try:
            if not self.llm:
                return self._generate_mock_travel_plan(user_preferences, context)
            
            # Create system prompt for travel planning
            system_prompt = """You are an expert travel planner. Create detailed, personalized travel plans based on user preferences and available information.

Your travel plans should include:
- Day-by-day itinerary
- Recommended activities and attractions
- Budget considerations
- Practical tips and advice
- Alternative options when possible

Make the plan practical, enjoyable, and tailored to the user's preferences."""

            # Build user message
            preferences_text = self._format_preferences(user_preferences)
            user_message = f"Context:\n{context}\n\nUser Preferences:\n{preferences_text}\n\nPlease create a detailed travel plan."
            
            # Generate plan
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating travel plan: {e}")
            return f"I apologize, but I encountered an error while creating your travel plan. Please try again."
    
    def generate_destination_summary(self, destination: str, context: str) -> str:
        """Generate a summary for a specific destination"""
        try:
            if not self.llm:
                return self._generate_mock_destination_summary(destination, context)
            
            system_prompt = """You are a travel expert. Create engaging and informative destination summaries that highlight the key attractions, culture, and practical information for travelers."""

            user_message = f"Context:\n{context}\n\nCreate a comprehensive summary for {destination} that includes must-see attractions, local culture, practical tips, and why travelers should visit this destination."
            
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = self.llm.invoke(messages)
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating destination summary: {e}")
            return f"I apologize, but I encountered an error while creating the destination summary for {destination}."
    
    def _format_preferences(self, preferences: Dict[str, Any]) -> str:
        """Format user preferences for the LLM"""
        formatted = []
        for key, value in preferences.items():
            if value:
                if isinstance(value, list):
                    formatted.append(f"{key}: {', '.join(value)}")
                else:
                    formatted.append(f"{key}: {value}")
        return "\n".join(formatted)
    
    def _generate_mock_response(self, query: str, context: str) -> str:
        """Generate a mock response when LLM is not available"""
        return f"Based on the available travel information, here's what I found for your query: '{query}'. The context contains relevant travel details that would help answer your question. For a complete response, please ensure the OpenAI API key is configured."
    
    def _generate_mock_travel_plan(self, preferences: Dict[str, Any], context: str) -> str:
        """Generate a mock travel plan when LLM is not available"""
        return f"I would create a personalized travel plan based on your preferences: {preferences} and the available travel information. For a detailed plan, please ensure the OpenAI API key is configured."
    
    def _generate_mock_destination_summary(self, destination: str, context: str) -> str:
        """Generate a mock destination summary when LLM is not available"""
        return f"{destination} is a wonderful travel destination with many attractions and cultural experiences. Based on the available information, there are several interesting places to visit and activities to enjoy. For a detailed summary, please ensure the OpenAI API key is configured." 