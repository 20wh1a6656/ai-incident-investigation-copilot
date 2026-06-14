import os
import sys

# Ensure backend root is on PATH
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.rag.chroma_manager import chroma_manager
from app.rag.retrieve import document_retriever

def main():
    print("====================================================")
    print("          ChromaDB RAG Audit Diagnostic              ")
    print("====================================================\n")

    # 1. Check database connectivity
    status = chroma_manager.get_status()
    print("ChromaDB Status:")
    for k, v in status.items():
        print(f"  {k}: {v}")

    collection = chroma_manager.get_collection()
    if not collection:
        print("\n[ALERT] ChromaDB collection is unavailable or empty.")
        print("Falling back to simulated keyword retrieval.")
        inspect_fallback()
        return

    # 2. Query all items in ChromaDB
    try:
        data = collection.get()
        ids = data.get("ids", [])
        documents = data.get("documents", [])
        metadatas = data.get("metadatas", [])
        
        print(f"\nIngested Document IDs count: {len(ids)}")
        print("Stored Document IDs:")
        for doc_id, meta in zip(ids, metadatas):
            title = meta.get("title", "No Title")
            source = meta.get("source", "No Source")
            print(f"  - ID: {doc_id} | Title: '{title}' | Source: {source}")

    except Exception as e:
        print(f"\n[ERROR] Failed to query ChromaDB collection: {str(e)}")
        ids = []

    # 3. Test Retrieval Queries (Retrieve Top 3)
    queries = [
        "Users cannot login to VPN",
        "SMTP authentication failing",
        "Database connection pool exhausted"
    ]

    print("\nRetrieval Matches (Top 3 for each query):")
    for q in queries:
        print(f"\nQuery: '{q}'")
        try:
            results = document_retriever.retrieve_relevant_docs(q, limit=3)
            for idx, r in enumerate(results):
                print(f"  Match #{idx+1}: ID: {r['id']} | Title: '{r['title']}' | Score: {r['confidence_score']}%")
        except Exception as e:
            print(f"  [ERROR] Retrieval query failed: {str(e)}")

def inspect_fallback():
    # Helper to check keyword fallback results
    queries = [
        "Users cannot login to VPN",
        "SMTP authentication failing",
        "Database connection pool exhausted"
    ]
    print("\nFallback Retrieval Matches (Top 3 for each query):")
    for q in queries:
        print(f"\nQuery: '{q}'")
        results = document_retriever._keyword_lookup_fallback(q, limit=3)
        for idx, r in enumerate(results):
            print(f"  Match #{idx+1}: ID: {r['id']} | Title: '{r['title']}' | Score: {r['confidence_score']}%")

if __name__ == "__main__":
    main()
