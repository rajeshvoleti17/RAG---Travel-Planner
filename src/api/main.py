"""
FastAPI Application for Travel Planner RAG System
Provides RESTful API endpoints for travel planning functionality
"""

import os
import logging
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import RAG components
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.rag_pipeline import TravelRAGPipeline
from data.document_processor import TravelDocumentProcessor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Travel Planner RAG API",
    description="A comprehensive RAG system for travel planning",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG pipeline
rag_pipeline = TravelRAGPipeline()
document_processor = TravelDocumentProcessor()

# Pydantic models for request/response
class ChatRequest(BaseModel):
    query: str
    n_results: Optional[int] = 5

class ChatResponse(BaseModel):
    query: str
    response: str
    retrieved_documents: List[Dict[str, Any]]
    context: str

class TravelPlanRequest(BaseModel):
    destination: Optional[str] = None
    budget: Optional[str] = None
    duration: Optional[str] = None
    interests: Optional[List[str]] = None
    travel_style: Optional[str] = None

class TravelPlanResponse(BaseModel):
    user_preferences: Dict[str, Any]
    travel_plan: str
    recommendations: List[Dict[str, Any]]
    context: str

class DestinationInfoRequest(BaseModel):
    destination: str

class DestinationInfoResponse(BaseModel):
    destination: str
    summary: str
    documents: List[Dict[str, Any]]
    context: str

class SearchDestinationsRequest(BaseModel):
    search_term: str

class SearchDestinationsResponse(BaseModel):
    search_term: str
    destinations: List[Dict[str, Any]]
    count: int

class AddDocumentsRequest(BaseModel):
    documents: List[Dict[str, Any]]

class AddDocumentsResponse(BaseModel):
    status: str
    documents_added: int
    message: str

class SystemStatsResponse(BaseModel):
    vector_store_stats: Dict[str, Any]
    model_info: Dict[str, Any]

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Travel Planner RAG API",
        "version": "1.0.0",
        "endpoints": [
            "/chat",
            "/plan",
            "/destination-info",
            "/search-destinations",
            "/add-documents",
            "/stats"
        ]
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a travel-related query"""
    try:
        result = rag_pipeline.process_query(request.query, request.n_results)
        return ChatResponse(**result)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/plan", response_model=TravelPlanResponse)
async def create_travel_plan(request: TravelPlanRequest):
    """Create a comprehensive travel plan"""
    try:
        # Convert request to preferences dict
        preferences = {
            'destination': request.destination,
            'budget': request.budget,
            'duration': request.duration,
            'interests': request.interests,
            'travel_style': request.travel_style
        }
        
        # Remove None values
        preferences = {k: v for k, v in preferences.items() if v is not None}
        
        result = rag_pipeline.create_travel_plan(preferences)
        return TravelPlanResponse(**result)
    except Exception as e:
        logger.error(f"Error in travel plan endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/destination-info", response_model=DestinationInfoResponse)
async def get_destination_info(request: DestinationInfoRequest):
    """Get detailed information about a destination"""
    try:
        result = rag_pipeline.get_destination_info(request.destination)
        return DestinationInfoResponse(**result)
    except Exception as e:
        logger.error(f"Error in destination info endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search-destinations", response_model=SearchDestinationsResponse)
async def search_destinations(request: SearchDestinationsRequest):
    """Search for destinations matching a search term"""
    try:
        result = rag_pipeline.search_destinations(request.search_term)
        return SearchDestinationsResponse(**result)
    except Exception as e:
        logger.error(f"Error in search destinations endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-documents", response_model=AddDocumentsResponse)
async def add_documents(request: AddDocumentsRequest):
    """Add travel documents to the knowledge base"""
    try:
        result = rag_pipeline.add_travel_documents(request.documents)
        return AddDocumentsResponse(**result)
    except Exception as e:
        logger.error(f"Error in add documents endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add-sample-documents")
async def add_sample_documents():
    """Add sample travel documents for testing"""
    try:
        sample_docs = document_processor.create_sample_travel_documents()
        result = rag_pipeline.add_travel_documents(sample_docs)
        return result
    except Exception as e:
        logger.error(f"Error adding sample documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", response_model=SystemStatsResponse)
async def get_system_stats():
    """Get system statistics"""
    try:
        stats = rag_pipeline.get_system_stats()
        return SystemStatsResponse(**stats)
    except Exception as e:
        logger.error(f"Error getting system stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a travel document"""
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Process document based on file type
        documents = []
        if file.filename.endswith('.txt'):
            doc = document_processor.process_text_file(temp_path)
            if doc:
                documents.append(doc)
        elif file.filename.endswith('.pdf'):
            documents = document_processor.process_pdf_file(temp_path)
        elif file.filename.endswith(('.docx', '.doc')):
            doc = document_processor.process_docx_file(temp_path)
            if doc:
                documents.append(doc)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Add to knowledge base
        if documents:
            result = rag_pipeline.add_travel_documents(documents)
            return result
        else:
            raise HTTPException(status_code=400, detail="No content extracted from document")
            
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 