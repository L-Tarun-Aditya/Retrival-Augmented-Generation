# Quick Start Guide

Get your RAG application running in 5 minutes!

## Step 1: Install Backend Dependencies (2 min)

```bash
cd Retrival-Augmented-Generation
pip install -r requirements.txt
```

## Step 2: Setup Environment (30 sec)

Create `.env` file:
```bash
echo "OPENAI_API_KEY=your_openrouter_api_key_here" > .env
```

Get your API key from: https://openrouter.ai/

## Step 3: Build Vector Store (1 min)

```bash
./build_index.sh
```

This creates embeddings from your documents.

## Step 4: Start Backend API (30 sec)

```bash
./run_api.sh
```

Keep this terminal open. API runs on http://localhost:8000

## Step 5: Setup Frontend (1 min)

Open a new terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on http://localhost:3000

## Step 6: Start Chatting! 

1. Open http://localhost:3000 in your browser
2. Ask questions like:
   - "What is software engineering?"
   - "Explain the waterfall model"
   - "What are software myths?"

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "Port already in use"
Kill the process:
```bash
# For API (port 8000)
lsof -ti:8000 | xargs kill -9

# For frontend (port 3000)
lsof -ti:3000 | xargs kill -9
```

### "No documents found"
Make sure you have text files in `data/output/`:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
cd src/rag
python3 extracting.py  # Extract PDFs first
cd ../..
./build_index.sh  # Then build index
```

### API not connecting
Check if API is running:
```bash
curl http://localhost:8000
```

Should return: `{"status":"ok",...}`

## Next Steps

- Add more PDFs to `data/input/`
- Run `python src/rag/extracting.py` to extract them
- Rebuild index: `curl -X POST http://localhost:8000/rebuild-index`
- Customize the UI in `frontend/components/chat.tsx`

## Need Help?

See [SETUP.md](SETUP.md) for detailed instructions or [README.md](README.md) for full documentation.
