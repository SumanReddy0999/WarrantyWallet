import os
import sys
import uuid

# This block adds the ai-service directory to the Python path
ai_service_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'services/ai-service'))
sys.path.insert(0, ai_service_path)

# Now, we can import from 'src' as if it were a top-level package
from src.services.retrieval_service import get_vector_store_retriever

def run_test():
    """Tests the retriever service."""
    
    # The valid warranty_id from your API response
    TEST_WARRANTY_ID = "0a2eedeb-fe1a-4b08-9bc7-c71138490148"
    
    # A sample question to test retrieval
    TEST_QUESTION = "What is the warranty period?"

    print("--- STARTING TEST FOR: Retrieval Service ---")

    try:
        warranty_uuid = uuid.UUID(TEST_WARRANTY_ID)
        
        # 1. Get the retriever for the specific warranty
        retriever = get_vector_store_retriever(warranty_uuid)
        
        # 2. Use the retriever to find relevant documents
        print(f"\nSearching for documents related to: '{TEST_QUESTION}'")
        relevant_docs = retriever.invoke(TEST_QUESTION)
        
        # 3. Verify the output
        if not relevant_docs:
            print("\nWARNING: Retriever returned no documents.")
        else:
            print(f"\nSUCCESS: Retriever found {len(relevant_docs)} relevant document(s).")
            print("\n--- Content of First Document ---")
            print(relevant_docs[0].page_content)
            print("\n--- Metadata of First Document ---")
            print(relevant_docs[0].metadata)

        print(f"\n--- TEST SUCCEEDED ---")

    except Exception as e:
        print(f"\n--- TEST FAILED ---")
        print(f"Error: {e}")

if __name__ == "__main__":
    run_test()