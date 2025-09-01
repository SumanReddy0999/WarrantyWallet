import sys
import os
import uuid
import pprint

# --- SCRIPT SETUP ---
# Add the ai-service 'src' directory to the Python path
ai_service_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'services/ai-service'))
sys.path.insert(0, ai_service_path)
# --- END SETUP ---

from src.services.rag_graph_service import app # Import the compiled graph

def run_test():
    """Tests the RAG graph service."""
    
    # Use the same warranty_id you used for the retriever test
    TEST_WARRANTY_ID = "0a2eedeb-fe1a-4b08-9bc7-c71138490148"
    
    # A sample question to test the full RAG flow
    TEST_QUESTION = "What is the warranty period for the NovaSound speaker?"

    print("--- STARTING TEST FOR: RAG Graph ---")

    try:
            
        # This is the input to our graph
        inputs = {"question": TEST_QUESTION, "warranty_id": uuid.UUID(TEST_WARRANTY_ID)}
        
        # Invoke the graph and stream the output
        for output in app.stream(inputs):
            for key, value in output.items():
                print(f"--- Output from node: {key} ---")
                pprint.pprint(value, indent=2)
                print("\n")

        print(f"\n--- TEST SUCCEEDED ---")

    except Exception as e:
        print(f"\n--- TEST FAILED ---")
        print(f"Error: {e}")

if __name__ == "__main__":
    run_test()