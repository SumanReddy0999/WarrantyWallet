import os
from pathlib import Path
from typing import List
from langchain_community.document_loaders import UnstructuredPDFLoader, UnstructuredImageLoader
from ..core.config import TESSERACT_PATH

def load_text_from_document(file_path: str) -> List[str]:
    """
    Loads raw text from a document (PDF or image) using local parsers.
    This is the primary, fast, and free method for text extraction.
    It returns a list of strings, where each string is the content of a page.
    """
    print(f"INFO: Attempting to load text locally from '{file_path}'...")
    path = Path(file_path)
    file_suffix = path.suffix.lower()

    # Set Tesseract path if provided in config, as unstructured may need it
    if TESSERACT_PATH and os.path.exists(TESSERACT_PATH):
        os.environ["TESSDATA_PREFIX"] = os.path.dirname(TESSERACT_PATH)

    try:
        if file_suffix == ".pdf":
            # Using "paged" strategy to get one document per page
            loader = UnstructuredPDFLoader(str(path), mode="paged")
        elif file_suffix in [".jpg", ".jpeg", ".png", ".webp"]:
            loader = UnstructuredImageLoader(str(path), mode="paged")
        else:
            raise ValueError(f"Unsupported file type: {file_suffix}")

        docs = loader.load()
        
        page_contents = [doc.page_content for doc in docs if doc.page_content.strip()]

        if page_contents:
            print(f"SUCCESS: Text extracted locally from {len(page_contents)} page(s).")
        else:
            print("WARNING: Local text extraction resulted in empty content.")
            
        return page_contents
        
    except Exception as e:
        print(f"WARNING: Local text extraction failed. Reason: {e}")
        return [] # Return empty list on failure to allow fallback