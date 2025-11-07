from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path
import shutil

# Add src directory to path to import rag modules
src_path = Path(__file__).parent.parent
sys.path.insert(0, str(src_path))

from rag.rag_system import RAGSystem
from rag.vector_store import build_vector_store_from_file, build_vector_store_from_all_texts
from rag.extracting import extract_pdf_to_text, extract_all_pdfs

app = FastAPI(title="RAG API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = None


class QueryRequest(BaseModel):
    question: str
    n_results: int = 3


class QueryResponse(BaseModel):
    question: str
    answer: str
    context: list[str] = []


@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup."""
    global rag_system
    
    # Check if output folder is empty and process PDFs if needed
    output_dir = Path("/home/tarun/rag/Retrival-Augmented-Generation/data/output")
    input_dir = Path("/home/tarun/rag/Retrival-Augmented-Generation/data/input")
    
    # Check if output directory has any text files
    txt_files = list(output_dir.glob("*.txt")) if output_dir.exists() else []
    
    if not txt_files:
        print("Output folder is empty. Checking for PDFs in input folder...")
        pdf_files = list(input_dir.glob("*.pdf")) if input_dir.exists() else []
        
        if pdf_files:
            print(f"Found {len(pdf_files)} PDF(s). Extracting text...")
            extract_all_pdfs()
            print("PDF extraction complete. Building vector store...")
            
            try:
                build_vector_store_from_all_texts(
                    str(output_dir),
                    collection_name="rag_documents"
                )
                print("Vector store built successfully from extracted PDFs")
            except Exception as e:
                print(f"Error building vector store: {e}")
        else:
            print("No PDFs found in input folder. Waiting for document upload...")
    
    # Initialize RAG system
    try:
        rag_system = RAGSystem(collection_name="rag_documents")
        print("RAG System initialized successfully")
    except Exception as e:
        print(f"Warning: Could not initialize RAG system: {e}")
        print("Upload documents to get started!")


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "ok",
        "message": "RAG API is running",
        "rag_ready": rag_system is not None
    }


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    """Query the RAG system."""
    if rag_system is None:
        raise HTTPException(
            status_code=503,
            detail="RAG system not initialized. Please run vector store setup first."
        )
    
    try:
        # Retrieve context
        context_chunks = rag_system.retrieve_context(
            request.question,
            n_results=request.n_results
        )
        
        # Generate response
        answer = rag_system.generate_response(request.question, context_chunks)
        
        return QueryResponse(
            question=request.question,
            answer=answer,
            context=context_chunks
        )
    
    except Exception as e:
        import traceback
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF document and process it."""
    global rag_system
    
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    try:
        input_dir = Path("/home/tarun/rag/Retrival-Augmented-Generation/data/input")
        output_dir = Path("/home/tarun/rag/Retrival-Augmented-Generation/data/output")
        
        # Ensure directories exist
        input_dir.mkdir(parents=True, exist_ok=True)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save uploaded PDF to input directory
        pdf_path = input_dir / file.filename
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"Saved PDF: {file.filename}")
        
        # Extract text from PDF
        txt_filename = pdf_path.stem + ".txt"
        txt_path = output_dir / txt_filename
        extract_pdf_to_text(str(pdf_path), str(txt_path))
        
        print(f"Extracted text to: {txt_filename}")
        
        # Rebuild vector store with all text files
        build_vector_store_from_all_texts(
            str(output_dir),
            collection_name="rag_documents"
        )
        
        # Reinitialize RAG system
        rag_system = RAGSystem(collection_name="rag_documents")
        
        return {
            "status": "success",
            "message": f"Document '{file.filename}' uploaded and processed successfully",
            "filename": file.filename
        }
    
    except Exception as e:
        import traceback
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/rebuild-index")
async def rebuild_index():
    """Rebuild the vector store index from all text files."""
    global rag_system
    
    try:
        output_dir = Path("/home/tarun/rag/Retrival-Augmented-Generation/data/output")
        
        # Check if there are text files
        txt_files = list(output_dir.glob("*.txt"))
        if not txt_files:
            raise HTTPException(
                status_code=400,
                detail="No text files found in output directory. Upload documents first."
            )
        
        # Rebuild vector store from all text files
        build_vector_store_from_all_texts(
            str(output_dir),
            collection_name="rag_documents"
        )
        
        # Reinitialize RAG system
        rag_system = RAGSystem(collection_name="rag_documents")
        
        return {
            "status": "success",
            "message": f"Vector store rebuilt successfully from {len(txt_files)} document(s)"
        }
    
    except Exception as e:
        import traceback
        print(f"ERROR: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents")
async def list_documents():
    """List all PDF documents in the input folder."""
    try:
        input_dir = Path("/home/tarun/rag/Retrival-Augmented-Generation/data/input")
        
        # Get PDF files from input directory
        pdf_files = list(input_dir.glob("*.pdf")) if input_dir.exists() else []
        
        documents = [{"filename": f.name, "size": f.stat().st_size} for f in pdf_files]
        
        return {
            "status": "success",
            "count": len(documents),
            "documents": documents
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
