from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path
import sys

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import chunking
chunk_text_file = chunking.chunk_text_file
chunk_all_text_files = chunking.chunk_all_text_files


class EmbeddingGenerator:
    """Generate embeddings for text chunks using sentence-transformers."""
    
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the embedding model.
        
        Args:
            model_name: Name of the sentence-transformer model to use
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully")
    
    def generate_embeddings(self, chunks):
        """
        Generate embeddings for a list of text chunks.
        
        Args:
            chunks: List of text chunks
        
        Returns:
            numpy array of embeddings with shape (num_chunks, embedding_dim)
        """
        print(f"Generating embeddings for {len(chunks)} chunks...")
        embeddings = self.model.encode(chunks, show_progress_bar=True)
        print(f"Embeddings shape: {embeddings.shape}")
        return embeddings
    
    def generate_single_embedding(self, text):
        """
        Generate embedding for a single text.
        
        Args:
            text: Single text string
        
        Returns:
            numpy array of embedding
        """
        return self.model.encode([text])[0]


def create_embeddings_from_file(input_file_path, chunk_size=1000, chunk_overlap=200):
    """
    Create embeddings from a text file.
    
    Args:
        input_file_path: Path to the text file
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
    
    Returns:
        tuple: (chunks, embeddings)
    """
    # Get chunks from the file
    chunks = chunk_text_file(input_file_path, chunk_size, chunk_overlap)
    
    # Generate embeddings
    embedding_gen = EmbeddingGenerator()
    embeddings = embedding_gen.generate_embeddings(chunks)
    
    return chunks, embeddings


def create_embeddings_from_all_files(output_folder=None):
    """
    Create embeddings from all text files in the output folder.
    
    Args:
        output_folder: Path to folder containing text files
    
    Returns:
        dict: Dictionary mapping filename to (chunks, embeddings) tuple
    """
    # Get all chunks
    all_chunks = chunk_all_text_files(output_folder)
    
    if not all_chunks:
        return {}
    
    # Generate embeddings for all chunks
    embedding_gen = EmbeddingGenerator()
    results = {}
    
    for filename, chunks in all_chunks.items():
        print(f"\nGenerating embeddings for {filename}...")
        embeddings = embedding_gen.generate_embeddings(chunks)
        results[filename] = (chunks, embeddings)
    
    return results


if __name__ == "__main__":
    # Process mod-1-notes.txt
    input_path = "/home/tarun/rag/Retrival-Augmented-Generation/data/output/mod-1-notes.txt"
    
    print("Creating embeddings from mod-1-notes.txt...\n")
    chunks, embeddings = create_embeddings_from_file(input_path)
    
    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"{'='*60}")
    print(f"Total chunks: {len(chunks)}")
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Embedding dimension: {embeddings.shape[1]}")
    print(f"\nFirst chunk preview:\n{chunks[0][:200]}...")
    print(f"\nFirst embedding (first 10 values):\n{embeddings[0][:10]}")
