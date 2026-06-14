import os
import sys

# Ensure backend root is on sys.path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.rag.ingest import run_cli_ingestion
from app.rag.retrieve import document_retriever

def main():
    print("====================================================")
    print("     RAG Pipeline Vector Search Verification Tool    ")
    print("====================================================\n")

    # Step 1: Run Ingestion
    print("[STEP 1] Running document parser & Chroma indexing...")
    try:
        run_cli_ingestion()
    except Exception as e:
        print(f"[ERROR] Ingestion failed: {str(e)}")
        print("Falling back to simulated keyword index query flow...\n")

    print("\n" + "=" * 50)
    
    # Step 2: Query Tests
    test_queries = [
        "okta saml credential sync invalid_grant",
        "hikari database transaction connection slots are reserved error",
        "vpn tunnel ipsec timeout alert symptom"
    ]

    print("[STEP 2] Running validation queries against the index...")
    for idx, query in enumerate(test_queries):
        print(f"\nQUERY #{idx+1}: '{query}'")
        try:
            results = document_retriever.retrieve_relevant_docs(query, limit=1)
            if results:
                best_match = results[0]
                print(f"Matched Title: {best_match['title']}")
                print(f"Matched Source: {best_match['source']} ({best_match['confidence_score']}% Match)")
                print(f"Content Chunk Snippet:\n{best_match['content'][:150]}...")
            else:
                print("No relevant SOP matches found.")
        except Exception as e:
            print(f"[ERROR] Search failed for query '{query}': {str(e)}")
            
    print("\nVerification execution complete.")

if __name__ == "__main__":
    main()
