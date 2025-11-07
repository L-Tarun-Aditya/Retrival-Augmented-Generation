from openai import OpenAI
from dotenv import load_dotenv
import os
from pathlib import Path
import sys

# Add current directory to path for imports
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Load .env from project root
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

import vector_store
VectorStore = vector_store.VectorStore


class RAGSystem:
    """Complete RAG system combining retrieval and generation."""
    
    def __init__(self, collection_name="rag_documents"):
        """
        Initialize RAG system.
        
        Args:
            collection_name: Name of the ChromaDB collection to use
        """
        # Check API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # Initialize OpenAI client
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        
        # Initialize vector store
        self.vector_store = VectorStore()
        self.collection_name = collection_name
        
        print("RAG System initialized")
    
    def retrieve_context(self, query, n_results=3):
        """
        Retrieve relevant context for a query.
        
        Args:
            query: User query
            n_results: Number of chunks to retrieve
        
        Returns:
            List of relevant text chunks
        """
        results = self.vector_store.query(self.collection_name, query, n_results)
        return results['documents'][0]
    
    def generate_response(self, query, context_chunks):
        """
        Generate response using LLM with retrieved context.
        
        Args:
            query: User query
            context_chunks: List of relevant text chunks
        
        Returns:
            Generated response
        """
        # Build context from chunks
        context = "\n\n".join([f"Context {i+1}:\n{chunk}" 
                               for i, chunk in enumerate(context_chunks)])
        
        # Create prompt with context
        prompt = f"""You are a helpful assistant. Use the following context to answer the question. If the answer is not in the context, say so.

Context:
{context}

Question: {query}

Answer:"""
        
        # Generate response
        try:
            completion = self.client.chat.completions.create(
                model="meta-llama/llama-3.3-70b-instruct:free",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers questions based on the provided context."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            print(f"LLM API Error: {str(e)}")
            raise Exception(f"Failed to generate response from LLM: {str(e)}")
    
    def query(self, question, n_results=3, show_context=False):
        """
        Complete RAG query: retrieve context and generate response.
        
        Args:
            question: User question
            n_results: Number of context chunks to retrieve
            show_context: Whether to print retrieved context
        
        Returns:
            Generated response
        """
        print(f"\nQuestion: {question}")
        print("\nRetrieving relevant context...")
        
        # Retrieve context
        context_chunks = self.retrieve_context(question, n_results)
        
        if show_context:
            print("\n" + "="*60)
            print("Retrieved Context:")
            print("="*60)
            for i, chunk in enumerate(context_chunks):
                print(f"\n--- Context {i+1} ---")
                print(chunk[:300] + "...")
        
        print("\nGenerating response...")
        
        # Generate response
        response = self.generate_response(question, context_chunks)
        
        return response


if __name__ == "__main__":
    # Initialize RAG system
    rag = RAGSystem(collection_name="rag_documents")
    
    # Example queries
    questions = [
        "What is software engineering?",
        "Explain the waterfall model",
        "What are software myths?"
    ]
    
    for question in questions:
        print("\n" + "="*80)
        response = rag.query(question, n_results=3, show_context=True)
        print("\n" + "="*60)
        print("Response:")
        print("="*60)
        print(response)
        print("="*80)
