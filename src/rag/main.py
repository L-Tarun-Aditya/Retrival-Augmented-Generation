"""
Complete RAG Pipeline
Run this script to build the vector store and query it.
"""

from pathlib import Path
import sys

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import vector_store
import rag_system

build_vector_store_from_file = vector_store.build_vector_store_from_file
RAGSystem = rag_system.RAGSystem


def setup_rag_system():
    """Build vector store from documents."""
    print("="*80)
    print("STEP 1: Building Vector Store")
    print("="*80)
    
    input_path = "/home/tarun/rag/Retrival-Augmented-Generation/data/output/mod-1-notes.txt"
    build_vector_store_from_file(input_path, collection_name="rag_documents")
    
    print("\n✓ Vector store ready!")


def run_rag_queries():
    """Run RAG queries."""
    print("\n" + "="*80)
    print("STEP 2: Running RAG Queries")
    print("="*80)
    
    rag = RAGSystem(collection_name="rag_documents")
    
    # Interactive mode
    print("\nRAG System Ready! Ask questions about software engineering.")
    print("Type 'quit' to exit.\n")
    
    while True:
        question = input("Your question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
        
        try:
            response = rag.query(question, n_results=3, show_context=False)
            print("\n" + "-"*60)
            print("Answer:")
            print("-"*60)
            print(response)
            print("\n")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Build vector store (run once)
    setup_rag_system()
    
    # Run queries (interactive)
    run_rag_queries()
