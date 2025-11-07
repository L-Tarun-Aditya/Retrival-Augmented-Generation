from PyPDF2 import PdfReader
import os
from pathlib import Path


def extract_pdf_to_text(pdf_path, output_path):
    """Extract text from a PDF file and save to output path."""
    reader = PdfReader(pdf_path)
    text = "".join(page.extract_text() for page in reader.pages)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    return text


def extract_all_pdfs():
    """Extract all PDFs from input folder to text files in output folder."""
    input_path = Path("/home/tarun/rag/Retrival-Augmented-Generation/data/input")
    output_path = Path("/home/tarun/rag/Retrival-Augmented-Generation/data/output")
    
    # Create directories if they don't exist
    input_path.mkdir(parents=True, exist_ok=True)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Get all PDF files from input directory
    pdf_files = list(input_path.glob("*.pdf"))
    
    if not pdf_files:
        print("No PDF files found in input directory")
        return []
    
    extracted_files = []
    
    # Process each PDF
    for pdf_file in pdf_files:
        output_file = output_path / f"{pdf_file.stem}.txt"
        print(f"Extracting {pdf_file.name} -> {output_file.name}")
        
        try:
            extract_pdf_to_text(pdf_file, output_file)
            print(f"Successfully extracted {pdf_file.name}")
            extracted_files.append(output_file)
        except Exception as e:
            print(f"Error extracting {pdf_file.name}: {e}")
    
    return extracted_files


if __name__ == "__main__":
    extract_all_pdfs()
