
from PyPDF2 import PdfReader

reader = PdfReader("/home/tarun/rag/data/mod-1-notes.pdf")
page = reader.pages[0]
print(page.extract_text())