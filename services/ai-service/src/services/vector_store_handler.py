from typing import List, Dict, Any
from langchain.docstore.document import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ..core import config
from ..schemas.warranty import WarrantyData

def create_chunks_and_embeddings(
    raw_text: str,
    metadata: WarrantyData
) -> List[Dict[str, Any]]:
    """
    Splits raw text into chunks and creates a vector embedding for each chunk.

    Args:
        raw_text: The full, raw text extracted from the document.
        metadata: The structured Pydantic object containing extracted warranty data.

    Returns:
        A list of dictionaries, where each dictionary represents a chunk
        and contains its text, vector, and combined metadata.
    """
    print("INFO: Starting chunking and embedding process...")
    if not raw_text or not raw_text.strip():
        print("WARNING: No raw text provided to chunk. Skipping embedding process.")
        return []

    # The splitter works on a list of Document objects
    docs_for_splitting = [Document(page_content=raw_text)]

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_documents(docs_for_splitting)
    print(f"INFO: Split document into {len(chunks)} chunks.")

    if not chunks:
        print("WARNING: Text splitting resulted in zero chunks.")
        return []

    # Initialize the embeddings model
    embeddings_model = GoogleGenerativeAIEmbeddings(
        model=config.EMBEDDING_MODEL_NAME,
        google_api_key=config.GEMINI_API_KEY
    )

    # Get the text content of each chunk
    chunk_texts = [chunk.page_content for chunk in chunks]

    # Create embeddings for all chunks in a single batch call
    print(f"INFO: Creating {len(chunk_texts)} embeddings in a single batch...")
    chunk_embeddings = embeddings_model.embed_documents(chunk_texts)
    print("SUCCESS: Embeddings created.")

    if len(chunks) != len(chunk_embeddings):
        raise ValueError("Mismatch between the number of chunks and the number of embeddings generated.")

    # Combine chunks with their vectors and metadata
    chunks_with_vectors = []
    # Convert Pydantic model to a dictionary for metadata
    structured_metadata_dict = metadata.model_dump(mode='json')

    for i, chunk in enumerate(chunks):
        # Combine the document-level structured metadata with any chunk-specific metadata
        combined_metadata = {**structured_metadata_dict, **chunk.metadata}
        chunks_with_vectors.append({
            "text": chunk.page_content,
            "vector": chunk_embeddings[i],
            "chunk_metadata": combined_metadata
        })

    return chunks_with_vectors