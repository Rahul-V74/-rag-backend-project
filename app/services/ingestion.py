import docx2txt
from pypdf import PdfReader
from app.core.embeddings import embed_text
from app.core.vector_store import insert_vectors

def read_pdf(path):
    reader = PdfReader(path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

def read_docx(path):
    return docx2txt.process(path)

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def process_document(filepath, filename):
    if filename.endswith(".pdf"):
        text = read_pdf(filepath)
    elif filename.endswith(".docx"):
        text = read_docx(filepath)
    else:
        text = open(filepath, "r").read()

    chunks = chunk_text(text)
    embeddings = [embed_text(chunk) for chunk in chunks]

    insert_vectors(embeddings, chunks, metadata={"filename": filename})

    return len(chunks)
