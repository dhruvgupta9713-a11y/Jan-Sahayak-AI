import os
from langchain_community.document_loaders import PyPDFLoader

# Handle dynamic import locations for text splitters between different LangChain versions
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
except ImportError:
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
    except ImportError as e:
        raise ImportError("Could not import RecursiveCharacterTextSplitter. Please ensure langchain is installed.") from e

def extract_text_from_pdf(pdf_path: str):
    """
    Loads a PDF file from the local path and extracts documents.
    Each page of the PDF is loaded as a separate Document object
    with text and page metadata (e.g. source, page number).
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at: {pdf_path}")
    
    # PyPDFLoader parses the PDF and retains metadata like page numbers
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents

def chunk_documents(documents, chunk_size: int = 1000, chunk_overlap: int = 200):
    """
    Splits a list of Document objects into smaller overlapping chunks.
    Uses RecursiveCharacterTextSplitter to split by logical elements like paragraphs, 
    sentences, and words, preventing information loss across chunk boundaries.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        add_start_index=True  # Tracks exactly where the chunk begins in the page
    )
    chunks = text_splitter.split_documents(documents)
    return chunks
