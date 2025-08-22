import os
from pathlib import Path
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredPDFLoader, UnstructuredImageLoader
from ..core.config import TESSERACT_PATH
from langsmith import traceable

@traceable(name="local extractor")
def load_text_from_document(file_path: str) -> List[str]:
    """
    Loads raw text from a document using a tiered strategy for optimal performance.
    1. Tries the fast PyMuPDFLoader.
    2. Falls back to the more robust UnstructuredPDFLoader if the first fails.
    """
    print(f"INFO: Attempting to load text locally from '{file_path}'...")
    path = Path(file_path)
    file_suffix = path.suffix.lower()

    page_contents = []

    if file_suffix == ".pdf":
        # Tier 1: Try the fastest loader first
        try:
            print("INFO: Tier 1 - Attempting fast extraction with PyMuPDFLoader...")
            loader = PyMuPDFLoader(str(path))
            docs = loader.load()
            page_contents = [doc.page_content for doc in docs if doc.page_content.strip()]
            if page_contents:
                print("SUCCESS: Tier 1 - Text extracted successfully with PyMuPDFLoader.")
                return page_contents
            else:
                print("WARNING: Tier 1 - PyMuPDFLoader extracted no content. Falling back.")
        except Exception as e:
            print(f"WARNING: Tier 1 - PyMuPDFLoader failed: {e}. Falling back.")

        # Tier 2: Fallback to the more powerful but slower loader
        try:
            print("INFO: Tier 2 - Attempting extraction with UnstructuredPDFLoader...")
            if TESSERACT_PATH and os.path.exists(TESSERACT_PATH):
                os.environ["TESSDATA_PREFIX"] = os.path.dirname(TESSERACT_PATH)
            
            loader = UnstructuredPDFLoader(str(path), mode="paged", strategy="fast")
            docs = loader.load()
            page_contents = [doc.page_content for doc in docs if doc.page_content.strip()]
            if page_contents:
                print("SUCCESS: Tier 2 - Text extracted with UnstructuredPDFLoader.")
                return page_contents
        except Exception as e:
            print(f"WARNING: Tier 2 - UnstructuredPDFLoader also failed: {e}")

    elif file_suffix in [".jpg", ".jpeg", ".png", ".webp"]:
        # For images, we go straight to UnstructuredImageLoader
        try:
            print("INFO: Attempting image extraction with UnstructuredImageLoader...")
            if TESSERACT_PATH and os.path.exists(TESSERACT_PATH):
                os.environ["TESSDATA_PREFIX"] = os.path.dirname(TESSERACT_PATH)

            loader = UnstructuredImageLoader(str(path), mode="paged")
            docs = loader.load()
            page_contents = [doc.page_content for doc in docs if doc.page_content.strip()]
            if page_contents:
                print("SUCCESS: Image text extracted locally.")
        except Exception as e:
            print(f"WARNING: UnstructuredImageLoader failed: {e}")
    else:
        raise ValueError(f"Unsupported file type: {file_suffix}")

    if not page_contents:
        print("WARNING: All local extraction methods failed to produce content.")
    
    return page_contents