import chromadb
from chromadb.config import Settings
from pathlib import Path
import sys

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

import embeddings
EmbeddingGenerator = embeddings.EmbeddingGenerator
create_embeddings_from_file = embeddings.create_embeddings_from_file


class VectorStore:
    """Manage vector storage and retrieval using ChromaDB."""
    
    def __init__(self, persist_directory=None):
        """
        Initialize ChromaDB client.
        
        Args:
            persist_directory: Directory to persist the database
        """
        if persist_directory is None:
            # Use absolute path relative to this file
            persist_directory = str(Path(__file__).parent / "chroma_db")
        
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embedding_gen = EmbeddingGenerator()
        print(f"ChromaDB initialized at {persist_directory}")
    
    def create_collection(self, collection_name="rag_documents"):
        """
        Create or get a collection.
        
        Args:
            collection_name: Name of the collection
        
        Returns:
            ChromaDB collection
        """
        # Delete existing collection if it exists
        try:
            self.client.delete_collection(collection_name)
            print(f"Deleted existing collection: {collection_name}")
        except:
            pass
        
        collection = self.client.create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )
        print(f"Created collection: {collection_name}")
        return collection
    
    def add_documents(self, collection_name, chunks, embeddings, metadata=None):
        """
        Add documents to the collection.
        
        Args:
            collection_name: Name of the collection
            chunks: List of text chunks
            embeddings: Numpy array of embeddings
            metadata: Optional list of metadata dicts for each chunk
        """
        collection = self.client.get_or_create_collection(collection_name)
        
        # Prepare data
        ids = [f"doc_{i}" for i in range(len(chunks))]
        
        if metadata is None:
            metadata = [{"chunk_id": i} for i in range(len(chunks))]
        
        # Add to collection
        collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=chunks,
            metadatas=metadata
        )
        
        print(f"Added {len(chunks)} documents to collection '{collection_name}'")
    
    def query(self, collection_name, query_text, n_results=3):
        """
        Query the collection for similar documents.
        
        Args:
            collection_name: Name of the collection
            query_text: Query text
            n_results: Number of results to return
        
        Returns:
            dict with 'documents', 'distances', 'metadatas'
        """
        collection = self.client.get_collection(collection_name)
        
        # Generate embedding for query
        query_embedding = self.embedding_gen.generate_single_embedding(query_text)
        
        # Query the collection
        results = collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )
        
        return results


def build_vector_store_from_file(input_file_path, collection_name="rag_documents"):
    """
    Build a complete vector store from a text file.
    
    Args:
        input_file_path: Path to the text file
        collection_name: Name for the ChromaDB collection
    
    Returns:
        VectorStore instance
    """
    print("Building vector store...\n")
    
    # Create embeddings
    chunks, embeddings = create_embeddings_from_file(input_file_path)
    
    # Initialize vector store
    vector_store = VectorStore()
    
    # Create collection and add documents
    vector_store.create_collection(collection_name)
    vector_store.add_documents(collection_name, chunks, embeddings)
    
    print("\nVector store built successfully!")
    return vector_store


def build_vector_store_from_all_texts(output_dir, collection_name="rag_documents"):
    """
    Build vector store from all text files in output directory.
    
    Args:
        output_dir: Path to directory containing text files
        collection_name: Name for the ChromaDB collection
    
    Returns:
        VectorStore instance
    """
    from pathlib import Path
    
    output_path = Path(output_dir)
    txt_files = list(output_path.glob("*.txt"))
    
    if not txt_files:
        raise ValueError(f"No text files found in {output_dir}")
    
    print(f"Found {len(txt_files)} text file(s) to process\n")
    
    # Initialize vector store
    vector_store = VectorStore()
    vector_store.create_collection(collection_name)
    
    # Process each text file
    all_chunks = []
    all_embeddings = []
    
    for txt_file in txt_files:
        print(f"Processing {txt_file.name}...")
        chunks, embeddings_array = create_embeddings_from_file(str(txt_file))
        all_chunks.extend(chunks)
        all_embeddings.append(embeddings_array)
    
    # Combine all embeddings
    import numpy as np
    combined_embeddings = np.vstack(all_embeddings)
    
    # Add all documents to collection
    vector_store.add_documents(collection_name, all_chunks, combined_embeddings)
    
    print(f"\nVector store built successfully with {len(all_chunks)} total chunks!")
    return vector_store


if __name__ == "__main__":
    # Build vector store from mod-1-notes.txt
    input_path = "/home/tarun/rag/Retrival-Augmented-Generation/data/output/mod-1-notes.txt"
    
    vector_store = build_vector_store_from_file(input_path)
    
    # Test query
    print("\n" + "="*60)
    print("Testing retrieval...")
    print("="*60)
    
    query = "What is software engineering?"
    results = vector_store.query("rag_documents", query, n_results=3)
    
    print(f"\nQuery: {query}")
    print(f"\nTop {len(results['documents'][0])} relevant chunks:\n")
    
    for i, (doc, distance) in enumerate(zip(results['documents'][0], results['distances'][0])):
        print(f"\n--- Result {i+1} (similarity: {1-distance:.4f}) ---")
        print(doc[:300] + "...")
