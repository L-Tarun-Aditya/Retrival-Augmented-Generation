# RAG Application Setup Guide

## Project Structure
```
Retrival-Augmented-Generation/
├── data/
│   ├── input/          # Place PDF files here
│   └── output/         # Extracted text files
├── src/
│   ├── api/            # FastAPI backend
│   └── rag/            # RAG pipeline modules
├── frontend/           # Next.js frontend
└── requirements.txt
```

## Backend Setup

### 1. Install Python Dependencies
```bash
cd Retrival-Augmented-Generation
pip install -r requirements.txt
```

### 2. Setup Environment Variables
Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openrouter_api_key_here
```

### 3. Build the Vector Store
```bash
./build_index.sh
```

This will:
- Read text files from `data/output/`
- Create embeddings
- Store them in ChromaDB

### 4. Start the API Server
```bash
./run_api.sh
```

The API will run on `http://localhost:8000`

## Frontend Setup

### 1. Install Node Dependencies
```bash
cd frontend
npm install
```

### 2. Start the Development Server
```bash
npm run dev
```

The frontend will run on `http://localhost:3000`

## Usage

### Extract PDFs (if needed)
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
cd src/rag
python3 extracting.py
cd ../..
```

### Full Pipeline
1. Place PDFs in `data/input/`
2. Extract: `export PYTHONPATH="${PYTHONPATH}:$(pwd)/src" && cd src/rag && python3 extracting.py && cd ../..`
3. Build vector store: `./build_index.sh`
4. Start API: `./run_api.sh`
5. Start frontend: `cd frontend && npm run dev`
6. Open browser to `http://localhost:3000`

## API Endpoints

- `GET /` - Health check
- `POST /query` - Query the RAG system
  ```json
  {
    "question": "What is software engineering?",
    "n_results": 3
  }
  ```
- `POST /rebuild-index` - Rebuild the vector store

## Features

- 📚 PDF text extraction
- 🔍 Semantic search with embeddings
- 💬 Chat interface with context
- 🎨 Modern UI with shadcn/ui
- ⚡ Fast retrieval with ChromaDB
- 🤖 LLM responses via OpenRouter

## Troubleshooting

### API not connecting
- Ensure the API server is running on port 8000
- Check CORS settings in `src/api/server.py`

### No results from queries
- Rebuild the vector store: `POST http://localhost:8000/rebuild-index`
- Check that text files exist in `data/output/`

### Frontend build errors
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Clear Next.js cache: `rm -rf .next`
