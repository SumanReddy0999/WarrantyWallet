import uuid
from langchain_postgres.vectorstores import PGVector
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever

from ..core import config
# Import the shared SQLAlchemy engine from our existing database setup
from ..db.database import engine

def get_vector_store_retriever(warranty_id: uuid.UUID) -> VectorStoreRetriever:
    """
    Initializes and returns a retriever by connecting to the LangChain-managed
    index for a specific warranty_id.
    """
    embeddings = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL_NAME,
        google_api_key=config.GEMINI_API_KEY
    )
    
    # Initialize the PGVector store using our app's existing SQLAlchemy engine
    db_vector_store = PGVector(
        connection=engine, # Use the shared engine
        embeddings=embeddings,
        collection_name=str(warranty_id),
    )
    
    # The filter is no longer needed, as each warranty has its own collection
    retriever = db_vector_store.as_retriever()
    
    print(f"INFO: Retriever created for warranty_id: {warranty_id}")
    return retriever