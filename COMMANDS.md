# Command Reference

Quick reference for all commands needed to run the RAG application.

## Initial Setup (One Time)

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Environment File
```bash
echo "OPENAI_API_KEY=your_openrouter_api_key_here" > .env
```

Get your API key from: https://openrouter.ai/

### 3. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

## Running the Application

### Build Vector Store (Run once or when documents change)
```bash
./build_index.sh
```

### Start Backend API
```bash
./run_api.sh
```
Runs on: http://localhost:8000

### Start Frontend (in a new terminal)
```bash
cd frontend
npm run dev
```
Runs on: http://localhost:3000

## Working with Documents

### Extract PDFs to Text
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
cd src/rag
python3 extracting.py
cd ../..
```

### Rebuild Index After Adding Documents
```bash
./build_index.sh
```

Or via API:
```bash
curl -X POST http://localhost:8000/rebuild-index
```

## Testing

### Test API Health
```bash
curl http://localhost:8000
```

### Test Query
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is software engineering?", "n_results": 3}'
```

### View API Documentation
Open: http://localhost:8000/docs

## Troubleshooting

### Kill Process on Port
```bash
# Kill API (port 8000)
lsof -ti:8000 | xargs kill -9

# Kill Frontend (port 3000)
lsof -ti:3000 | xargs kill -9
```

### Check if Ports are in Use
```bash
lsof -i:8000  # Check API port
lsof -i:3000  # Check frontend port
```

### Verify Python Path
```bash
echo $PYTHONPATH
```

### Test Imports
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
python3 -c "from rag.rag_system import RAGSystem; print('Success!')"
```

## Development

### Run Individual Components

#### Just Chunking
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
cd src/rag
python3 chunking.py
```

#### Just Embeddings
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
cd src/rag
python3 embeddings.py
```

#### Just Vector Store
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
cd src/rag
python3 vector_store.py
```

#### CLI RAG System
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
cd src/rag
python3 main.py
```

## Production

### Build Frontend for Production
```bash
cd frontend
npm run build
npm start
```

### Run API with Gunicorn (Production)
```bash
pip install gunicorn
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
cd src/api
gunicorn server:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Environment Variables

### Required
- `OPENAI_API_KEY` - Your OpenRouter API key

### Optional
- `PYTHONPATH` - Set automatically by scripts, but can be set manually

## File Locations

- **PDFs**: `data/input/*.pdf`
- **Extracted Text**: `data/output/*.txt`
- **Vector DB**: `src/rag/chroma_db/`
- **Environment**: `.env` (root directory)
- **Frontend Build**: `frontend/.next/`

## Quick Commands Summary

```bash
# Setup
pip install -r requirements.txt
echo "OPENAI_API_KEY=your_key" > .env
cd frontend && npm install && cd ..

# Run
./build_index.sh          # Build index (once)
./run_api.sh              # Start API
cd frontend && npm run dev # Start frontend (new terminal)

# Access
# Frontend: http://localhost:3000
# API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```
