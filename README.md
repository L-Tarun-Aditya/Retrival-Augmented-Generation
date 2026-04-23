# RAG Application - Retrieval-Augmented Generation

A complete RAG (Retrieval-Augmented Generation) system for querying software engineering documents using semantic search and LLM responses.

##  Features

-  **PDF Processing** - Extract text from PDF documents
-  **Smart Chunking** - Split documents into semantic chunks
-  **Vector Embeddings** - Generate embeddings using sentence-transformers
-  **Vector Database** - Store and retrieve with ChromaDB
-  **LLM Integration** - Generate answers using Llama 3.3 via OpenRouter
-  **Modern UI** - Beautiful chat interface with Next.js and shadcn/ui
-  **Fast API** - FastAPI backend for efficient processing

##  Project Structure

```
Retrival-Augmented-Generation/
├── data/
│   ├── input/              # Place PDF files here
│   └── output/             # Extracted text files
├── src/
│   ├── api/
│   │   └── server.py       # FastAPI backend
│   └── rag/
│       ├── extracting.py   # PDF extraction
│       ├── chunking.py     # Text chunking
│       ├── embeddings.py   # Generate embeddings
│       ├── vector_store.py # ChromaDB management
│       ├── rag_system.py   # Complete RAG pipeline
│       └── main.py         # CLI interface
├── frontend/               # Next.js frontend
│   ├── app/
│   ├── components/
│   └── package.json
├── requirements.txt
└── SETUP.md
```

##  Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- npm or yarn

### 1. Clone and Setup Backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_openrouter_api_key" > .env

# Build vector store
cd src/rag
python vector_store.py
cd ../..

# Start API server
cd src/api
python server.py
```

### 2. Setup Frontend

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev
```

### 3. Access the Application

- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Detailed Setup

See [SETUP.md](SETUP.md) for detailed instructions.

## Usage

### Extract PDFs
```bash
cd src/rag
python extracting.py
```

### Build Vector Store
```bash
python vector_store.py
```

### Run RAG System (CLI)
```bash
python main.py
```

### Query via API
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is software engineering?", "n_results": 3}'
```

## Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** - Modern web framework
- **sentence-transformers** - Embeddings (all-MiniLM-L6-v2)
- **ChromaDB** - Vector database
- **PyPDF2** - PDF processing
- **LangChain** - Text splitting
- **OpenAI SDK** - LLM integration (via OpenRouter)

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - UI components
- **Lucide React** - Icons

## API Endpoints

### `GET /`
Health check

### `POST /query`
Query the RAG system
```json
{
  "question": "What is software engineering?",
  "n_results": 3
}
```

Response:
```json
{
  "question": "What is software engineering?",
  "answer": "Software engineering is...",
  "context": ["chunk1", "chunk2", "chunk3"]
}
```

### `POST /rebuild-index`
Rebuild the vector store from documents

## 🎨 Frontend Features

- Real-time chat interface
- Message history
- Context viewer (show/hide retrieved chunks)
- Responsive design
- Loading states
- Error handling

## 🔧 Configuration

### Chunk Size
Edit `src/rag/chunking.py`:
```python
chunk_size=1000      # Characters per chunk
chunk_overlap=200    # Overlap between chunks
```

### Embedding Model
Edit `src/rag/embeddings.py`:
```python
model_name='all-MiniLM-L6-v2'  # Change to any sentence-transformer model
```

### LLM Model
Edit `src/rag/rag_system.py`:
```python
model="meta-llama/llama-3.3-70b-instruct:free"
```

## 📊 Performance

- **Embedding Model**: all-MiniLM-L6-v2 (384 dimensions)
- **Chunk Size**: 1000 characters with 200 overlap
- **Retrieval**: Top 3 most relevant chunks
- **Response Time**: ~2-5 seconds (depends on LLM)

## 🤝 Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- OpenRouter for LLM access
- Hugging Face for sentence-transformers
- ChromaDB for vector storage
- shadcn for beautiful UI components


