from extracting import extract_pdf_text
from langchain_text_splitters import CharacterTextSplitter

document = extract_pdf_text("/home/tarun/rag/data/mod-1-notes.pdf")

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
    encoding_name="cl100k_base", chunk_size=1, chunk_overlap=0
)
texts = text_splitter.split_text(document)
def output():
    return texts
