# Travel Planner RAG System

A comprehensive Retrieval-Augmented Generation (RAG) system for intelligent travel planning, built with modern AI technologies. This system combines the power of Large Language Models (LLMs) with a knowledge base of travel information to provide personalized travel recommendations and planning assistance.

## 🚀 What This Project Does

### Core Features
- **AI-Powered Travel Planning**: Get personalized travel recommendations based on your preferences, budget, and interests
- **Intelligent Document Processing**: Automatically processes and understands travel guides, reviews, and destination information
- **Semantic Search**: Fast vector-based search through travel knowledge using advanced embeddings
- **Interactive Chat Interface**: Natural language conversations for travel planning
- **RESTful API**: Programmatic access to travel planning capabilities
- **Real-time Recommendations**: Instant responses to travel queries with context-aware suggestions

### How It Works
1. **Knowledge Base**: The system maintains a vector database of travel documents, guides, and destination information
2. **Query Processing**: When you ask a travel question, it searches the knowledge base for relevant information
3. **AI Generation**: Combines retrieved information with LLM capabilities to generate personalized responses
4. **Context-Aware Responses**: Provides recommendations based on your specific requirements and preferences

## 📋 Prerequisites

Before you begin, ensure you have:
- Python 3.8 or higher installed
- An OpenAI API key (get one from [OpenAI Platform](https://platform.openai.com/api-keys))
- Basic familiarity with command line operations

## 🛠️ Step-by-Step Setup Instructions

### Step 1: Clone or Download the Project
```bash
# If you have git installed
git clone <repository-url>
cd travel-planner-rag

# Or simply navigate to the project directory if already downloaded
cd /path/to/travel-planner-rag
```

### Step 2: Install Python Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

**Note**: If you encounter dependency conflicts, you may see warnings about existing packages. This is normal and shouldn't affect functionality.

### Step 3: Set Up Environment Variables
```bash
# Copy the example environment file
cp env.example .env
```

Now edit the `.env` file and add your OpenAI API key:
```bash
# Open the file in your preferred editor
nano .env
# or
code .env
# or
open .env
```

Replace `your_openai_api_key_here` with your actual OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 4: Verify Installation
```bash
# Test that Python can import the required packages
python -c "import langchain, openai, streamlit, fastapi; print('All packages installed successfully!')"
```

## 🚀 Running the Application

You have two ways to run the application:

### Option A: Web Interface (Recommended for Beginners)
```bash
# Start the Streamlit web application
streamlit run src/web/app.py
```
- **Access**: Open your browser and go to `http://localhost:8501`
- **Best for**: Interactive travel planning with a user-friendly interface

### Option B: API Server (For Developers)
```bash
# Start the FastAPI server
python src/api/main.py
```
- **Access**: API endpoints available at `http://localhost:8000`
- **Best for**: Programmatic access and integration with other applications

## 🎯 How to Use the Application

### Web Interface Usage
1. **Open the Application**: Navigate to `http://localhost:8501`
2. **Ask Travel Questions**: Type questions like:
   - "What are the best places to visit in Japan?"
   - "Plan a 5-day trip to Paris for a couple"
   - "What's the best time to visit Bali?"
   - "Recommend budget-friendly hotels in New York"
3. **Get AI Responses**: The system will provide personalized recommendations based on your query

### API Usage
The system provides several REST endpoints:

#### Chat Endpoint
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Plan a weekend trip to Barcelona"}'
```

#### Get Destinations
```bash
curl "http://localhost:8000/destinations"
```

#### Generate Travel Plan
```bash
curl -X POST "http://localhost:8000/plan" \
     -H "Content-Type: application/json" \
     -d '{"destination": "Tokyo", "duration": "7 days", "budget": "medium"}'
```

## 📁 Project Structure

```
travel-planner-rag/
├── src/
│   ├── rag/           # RAG pipeline components
│   ├── api/           # FastAPI endpoints
│   ├── web/           # Streamlit web interface
│   ├── data/          # Data processing utilities
│   └── utils/         # Utility functions
├── data/
│   ├── documents/     # Travel documents and guides
│   └── embeddings/    # Vector embeddings storage
├── static/            # Static web assets
├── templates/         # HTML templates
├── requirements.txt   # Python dependencies
├── env.example       # Environment variables template
└── README.md         # This file
```

## 🔧 Configuration Options

The `.env` file contains several configuration options:

```env
# Required: Your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here

# Database and storage paths
CHROMA_DB_PATH=./data/embeddings
DOCUMENTS_PATH=./data/documents

# Model configuration
DEFAULT_MODEL=gpt-3.5-turbo
DEFAULT_TEMPERATURE=0.7

# API configuration
API_HOST=0.0.0.0
API_PORT=8000

# Web interface
STREAMLIT_PORT=8501

# Vector store configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
MAX_RESULTS=5
```

## 🐛 Troubleshooting

### Common Issues and Solutions

**1. OpenAI API Key Error**
```
Error: Invalid API key
```
**Solution**: Ensure your API key is correctly set in the `.env` file and is valid.

**2. Port Already in Use**
```
Error: Address already in use
```
**Solution**: Change the port in `.env` file or stop the existing process:
```bash
# Find and kill the process using the port
lsof -ti:8501 | xargs kill -9
```

**3. Import Errors**
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

**4. Memory Issues**
```
OutOfMemoryError
```
**Solution**: Reduce the model size or increase system memory allocation.

### Getting Help
- Check the console output for error messages
- Ensure all environment variables are set correctly
- Verify your OpenAI API key has sufficient credits

## 🔒 Security Notes

- **Never commit your `.env` file** to version control
- **Keep your API keys secure** and don't share them
- **Monitor your OpenAI usage** to avoid unexpected charges

## 🚀 Advanced Usage

### Adding Custom Travel Documents
1. Place your travel documents (PDF, DOCX, TXT) in `data/documents/`
2. The system will automatically process and index them
3. Restart the application to include new documents

### Customizing the Model
Edit the `.env` file to change:
- `DEFAULT_MODEL`: Switch between different OpenAI models
- `DEFAULT_TEMPERATURE`: Adjust response creativity (0.0-1.0)
- `EMBEDDING_MODEL`: Change the embedding model for vector search

## 📈 Performance Tips

- **For better performance**: Use a machine with at least 8GB RAM
- **For faster responses**: Consider using GPT-3.5-turbo instead of GPT-4
- **For larger knowledge bases**: Ensure sufficient storage space for embeddings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

---

**Happy Travel Planning! 🌍✈️**

Start the application and begin exploring the world with AI-powered travel assistance! 