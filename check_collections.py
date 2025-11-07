#!/usr/bin/env python3
import chromadb

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./src/rag/chroma_db")

# List all collections
collections = client.list_collections()

print(f"Found {len(collections)} collection(s):")
for collection in collections:
    print(f"  - {collection.name} (count: {collection.count()})")

if len(collections) == 0:
    print("\nNo collections found. The vector store will be built automatically when you:")
    print("  1. Place PDFs in data/input/ and run ./start.sh")
    print("  2. Upload PDFs via the web interface")
    print("  3. Use the /upload-document API endpoint")
