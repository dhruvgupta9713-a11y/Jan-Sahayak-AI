import os
import shutil
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

def get_embeddings_model(google_api_key: str):
    """
    Creates and returns the Google Generative AI embeddings model.
    Model: models/gemini-embedding-001 (standard Gemini embedding model)
    """
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=google_api_key
    )

def get_vector_store(persist_directory: str, google_api_key: str):
    """
    Initializes or loads a persistent ChromaDB vector store.
    """
    embeddings = get_embeddings_model(google_api_key)
    
    # Load or create the database
    vector_store = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    return vector_store

def add_documents_to_store(vector_store, documents) -> bool:
    """
    Embeds and adds a list of Document chunks to the vector database.
    """
    if not documents:
        return False
    
    vector_store.add_documents(documents)
    
    # In older LangChain versions, manual persistence is needed
    if hasattr(vector_store, 'persist') and callable(getattr(vector_store, 'persist')):
        try:
            vector_store.persist()
        except Exception as e:
            # Modern ChromaDB auto-persists and might raise deprecation or execution warnings
            print(f"Chroma persistence handled automatically: {e}")
            
    return True

def get_chunk_count(vector_store) -> int:
    """
    Returns the total number of chunks (embeddings) stored in the database.
    """
    try:
        # Chroma allows counting records via the collection interface
        if hasattr(vector_store, '_collection') and vector_store._collection is not None:
            return vector_store._collection.count()
    except Exception as e:
        print(f"Error counting vector store elements: {e}")
    return 0

def reset_vector_store(persist_directory: str) -> bool:
    """
    Wipes the ChromaDB directory entirely and rebuilds it as empty.
    """
    try:
        if os.path.exists(persist_directory):
            shutil.rmtree(persist_directory)
        os.makedirs(persist_directory, exist_ok=True)
        print(f"Successfully cleared vector database at: {persist_directory}")
        return True
    except Exception as e:
        print(f"Error resetting vector database: {e}")
        return False
