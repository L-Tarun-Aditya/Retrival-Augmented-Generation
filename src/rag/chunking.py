from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text_file(input_file_path, chunk_size=1000, chunk_overlap=200):
    """
    Read text file and split into chunks suitable for RAG application.
    
    Args:
        input_file_path: Path to the text file
        chunk_size: Maximum size of each chunk (default: 1000 characters)
        chunk_overlap: Overlap between chunks (default: 200 characters)
    
    Returns:
        List of text chunks
    """
    # Read the text file
    with open(input_file_path, 'r', encoding='utf-8') as f:
        document = f.read()
    
    # Use RecursiveCharacterTextSplitter for better semantic chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_text(document)
    return chunks


def chunk_all_text_files(output_folder=None):
    """
    Process all text files in the output folder and return chunks.
    
    Args:
        output_folder: Path to folder containing text files
    
    Returns:
        Dictionary mapping filename to list of chunks
    """
    if output_folder is None:
        output_folder = Path("/home/tarun/rag/Retrival-Augmented-Generation/data/output")
    else:
        output_folder = Path(output_folder)
    
    all_chunks = {}
    
    # Get all text files
    text_files = list(output_folder.glob("*.txt"))
    
    if not text_files:
        print("No text files found in output directory")
        return all_chunks
    
    # Process each text file
    for text_file in text_files:
        print(f"Chunking {text_file.name}...")
        chunks = chunk_text_file(text_file)
        all_chunks[text_file.name] = chunks
        print(f"Created {len(chunks)} chunks from {text_file.name}")
    
    return all_chunks


if __name__ == "__main__":
    # Chunk the mod-1-notes.txt file
    input_path = "/home/tarun/rag/Retrival-Augmented-Generation/data/output/mod-1-notes.txt"
    
    chunks = chunk_text_file(input_path, chunk_size=1000, chunk_overlap=200)
    
    print(f"\nTotal chunks created: {len(chunks)}")
    print(f"\nFirst chunk preview:\n{chunks[0][:200]}...")
    print(f"\nLast chunk preview:\n{chunks[-1][:200]}...")
