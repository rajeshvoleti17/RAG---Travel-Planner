"""
Document Processor for Travel Knowledge Base
Handles various document formats and extracts travel information
"""

import os
import json
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging

# Document processing imports
try:
    import pypdf
    from docx import Document
    from bs4 import BeautifulSoup
    import requests
except ImportError:
    logging.warning("Some document processing libraries not available")

logger = logging.getLogger(__name__)

class TravelDocumentProcessor:
    def __init__(self, documents_path: str = "./data/documents"):
        """Initialize the document processor"""
        self.documents_path = Path(documents_path)
        self.documents_path.mkdir(parents=True, exist_ok=True)
        
    def process_text_file(self, file_path: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a text file containing travel information"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            return {
                'content': content,
                'source': file_path,
                'title': metadata.get('title', Path(file_path).stem),
                'destination': metadata.get('destination', 'general'),
                'category': metadata.get('category', 'guide')
            }
            
        except Exception as e:
            logger.error(f"Error processing text file {file_path}: {e}")
            return {}
    
    def process_pdf_file(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Process a PDF file containing travel information"""
        try:
            documents = []
            
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    
                    if text.strip():  # Only add non-empty pages
                        documents.append({
                            'content': text,
                            'source': f"{file_path} (page {page_num + 1})",
                            'title': metadata.get('title', Path(file_path).stem),
                            'destination': metadata.get('destination', 'general'),
                            'category': metadata.get('category', 'guide')
                        })
            
            return documents
            
        except Exception as e:
            logger.error(f"Error processing PDF file {file_path}: {e}")
            return []
    
    def process_docx_file(self, file_path: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a DOCX file containing travel information"""
        try:
            doc = Document(file_path)
            content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            return {
                'content': content,
                'source': file_path,
                'title': metadata.get('title', Path(file_path).stem),
                'destination': metadata.get('destination', 'general'),
                'category': metadata.get('category', 'guide')
            }
            
        except Exception as e:
            logger.error(f"Error processing DOCX file {file_path}: {e}")
            return {}
    
    def scrape_travel_website(self, url: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Scrape travel information from a website"""
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Extract text content
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            content = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                'content': content,
                'source': url,
                'title': metadata.get('title', soup.title.string if soup.title else 'Web Content'),
                'destination': metadata.get('destination', 'general'),
                'category': metadata.get('category', 'web_content')
            }
            
        except Exception as e:
            logger.error(f"Error scraping website {url}: {e}")
            return {}
    
    def create_sample_travel_documents(self) -> List[Dict[str, Any]]:
        """Create sample travel documents for testing"""
        sample_documents = [
            {
                'content': """Paris, the City of Light, is one of the most beautiful and romantic cities in the world. 
                The Eiffel Tower, standing at 324 meters tall, is the most iconic symbol of Paris. Visitors can climb 
                to the top for breathtaking views of the city. The Louvre Museum houses the famous Mona Lisa and thousands 
                of other masterpieces. The Champs-Élysées is a famous avenue lined with luxury shops and restaurants. 
                Notre-Dame Cathedral, despite the 2019 fire, remains a stunning example of Gothic architecture. 
                The Seine River runs through the heart of Paris, and boat tours offer a unique perspective of the city. 
                French cuisine is world-renowned, with croissants, baguettes, and fine dining experiences available throughout the city.""",
                'source': 'sample_paris_guide.txt',
                'title': 'Paris Travel Guide',
                'destination': 'Paris',
                'category': 'city_guide'
            },
            {
                'content': """Tokyo, Japan's bustling capital, is a fascinating blend of ultramodern and traditional. 
                The city is known for its cutting-edge technology, fashion, and cuisine. Shibuya Crossing is the world's 
                busiest pedestrian crossing, symbolizing Tokyo's energy. The Tokyo Skytree offers panoramic views of the 
                sprawling metropolis. Traditional temples like Senso-ji in Asakusa provide a glimpse into Japan's rich history. 
                Akihabara is a paradise for electronics and anime enthusiasts. The Tsukiji Outer Market is famous for fresh 
                seafood and sushi. Tokyo's efficient public transportation system makes it easy to explore different districts. 
                The city's food scene ranges from Michelin-starred restaurants to humble ramen shops.""",
                'source': 'sample_tokyo_guide.txt',
                'title': 'Tokyo Travel Guide',
                'destination': 'Tokyo',
                'category': 'city_guide'
            },
            {
                'content': """New York City, the Big Apple, is a global center of culture, finance, and entertainment. 
                Times Square is the heart of Manhattan, known for its bright lights and Broadway theaters. Central Park 
                offers 843 acres of green space in the middle of the concrete jungle. The Statue of Liberty stands as a 
                symbol of freedom and welcomes visitors to New York Harbor. The Empire State Building provides spectacular 
                views of the city skyline. Broadway shows offer world-class entertainment, while museums like the Metropolitan 
                Museum of Art and the Museum of Modern Art showcase incredible collections. NYC's diverse neighborhoods, 
                from Chinatown to Little Italy, offer authentic cultural experiences and cuisine.""",
                'source': 'sample_nyc_guide.txt',
                'title': 'New York City Travel Guide',
                'destination': 'New York',
                'category': 'city_guide'
            },
            {
                'content': """Budget travel tips for exploring the world on a shoestring: Stay in hostels or use 
                accommodation sharing platforms like Airbnb and Couchsurfing. Cook your own meals instead of eating out 
                every day. Use public transportation instead of taxis. Travel during off-peak seasons for lower prices. 
                Look for free activities like walking tours, museums with free admission days, and public parks. 
                Book flights and accommodation in advance for better deals. Consider traveling to less touristy destinations 
                where prices are lower. Use travel apps to find the best deals on flights, accommodation, and activities. 
                Pack light to avoid checked baggage fees. Learn basic phrases in the local language to avoid tourist traps.""",
                'source': 'sample_budget_tips.txt',
                'title': 'Budget Travel Tips',
                'destination': 'general',
                'category': 'travel_tips'
            },
            {
                'content': """Solo travel is an incredible way to discover yourself and the world. Safety should always 
                be a priority - research your destination thoroughly and stay in well-lit, populated areas. Hostels are 
                great for meeting other travelers and finding travel companions. Keep important documents and money in a 
                secure location, preferably a money belt or hidden pouch. Learn basic phrases in the local language to 
                navigate more easily. Trust your instincts and don't be afraid to say no to uncomfortable situations. 
                Take plenty of photos and keep a travel journal to document your experiences. Solo travel allows for 
                complete freedom in your itinerary and the opportunity to step out of your comfort zone.""",
                'source': 'sample_solo_travel.txt',
                'title': 'Solo Travel Guide',
                'destination': 'general',
                'category': 'travel_tips'
            }
        ]
        
        return sample_documents
    
    def process_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Process all documents in a directory"""
        documents = []
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory {directory_path} does not exist")
            return documents
        
        for file_path in directory.rglob('*'):
            if file_path.is_file():
                try:
                    if file_path.suffix.lower() == '.txt':
                        doc = self.process_text_file(str(file_path))
                        if doc:
                            documents.append(doc)
                    elif file_path.suffix.lower() == '.pdf':
                        docs = self.process_pdf_file(str(file_path))
                        documents.extend(docs)
                    elif file_path.suffix.lower() in ['.docx', '.doc']:
                        doc = self.process_docx_file(str(file_path))
                        if doc:
                            documents.append(doc)
                except Exception as e:
                    logger.error(f"Error processing file {file_path}: {e}")
        
        return documents 