# How Your RAG System Works

## Step 1: Document Processing (Indexing Phase)

1. **PDF Upload** → User uploads a PDF
2. **Text Extraction** → PyPDF2 extracts raw text from PDF
3. **Chunking** → Text is split into smaller chunks (1000 chars with 200 char overlap)
   - Uses `RecursiveCharacterTextSplitter` which tries to split on `\n\n`, then `\n`, then spaces
   - Overlap ensures context isn't lost at chunk boundaries
4. **Embedding Generation** → Each chunk is converted to a vector
   - Uses `all-MiniLM-L6-v2` model (384-dimensional embeddings)
   - This captures the semantic meaning of the text
5. **Vector Storage** → Embeddings stored in ChromaDB with metadata
   - Each chunk stored with its embedding and text
   - Uses cosine similarity for searching

## Step 2: Query Processing (Retrieval Phase)

When you ask a question:

1. **Query Embedding** → Your question is converted to the same 384-dimensional vector
   ```python
   query_embedding = self.embedding_gen.generate_single_embedding(query_text)
   ```

2. **Similarity Search** → ChromaDB finds the most similar chunks
   - Compares your query embedding with all stored chunk embeddings
   - Uses cosine similarity (measures angle between vectors)
   - Returns top N most similar chunks (default: 3)

3. **Context Retrieval** → Gets the actual text of those similar chunks
   ```python
   results = collection.query(
       query_embeddings=[query_embedding.tolist()],
       n_results=3
   )
   ```

## Step 3: Response Generation (Generation Phase)

1. **Context Assembly** → Combines retrieved chunks into context
   ```python
   context = "\n\n".join([f"Context {i+1}:\n{chunk}" 
                          for i, chunk in enumerate(context_chunks)])
   ```

2. **Prompt Construction** → Creates a prompt with context + question
   ```python
   prompt = f"""Use the following context to answer the question.
   
   Context:
   {context}
   
   Question: {query}
   
   Answer:"""
   ```

3. **LLM Generation** → Sends to LLM (Llama 3.3 70B via OpenRouter)
   - LLM reads the context and generates an answer
   - Only uses information from the provided context

## Why This Works

**Semantic Search:**
- Similar meanings = similar embeddings
- "What is software engineering?" and "Define software engineering" have similar embeddings
- Even if exact words don't match, semantic similarity does

**Example:**
```
Query: "What is agile methodology?"
↓ (embedding)
[0.23, -0.45, 0.67, ...] (384 numbers)
↓ (cosine similarity search)
Finds chunks about agile, scrum, iterative development
↓ (LLM generation)
"Agile is an iterative approach to software development..."
```

## Key Advantages

1. **No exact keyword matching needed** - Understands meaning
2. **Handles synonyms** - "car" and "automobile" are close in embedding space
3. **Context-aware** - LLM sees relevant chunks, not entire document
4. **Scalable** - Vector search is fast even with millions of chunks
5. **Accurate** - LLM only uses provided context, reduces hallucination

## The Math (Simplified)

Cosine similarity between two vectors:
```
similarity = (A · B) / (||A|| × ||B||)
```
- Returns value between -1 and 1
- 1 = identical direction (very similar)
- 0 = perpendicular (unrelated)
- -1 = opposite (contradictory)

Your system uses this to find chunks where the embedding "points in the same direction" as your query embeddin