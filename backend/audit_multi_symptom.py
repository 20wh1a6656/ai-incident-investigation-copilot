import os
import sys

# Ensure backend root is on sys.path
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.rag.chroma_manager import chroma_manager
from sentence_transformers import SentenceTransformer

def main():
    client = chroma_manager.client
    if not client:
        print("Error: ChromaDB client is not available.")
        sys.exit(1)
        
    collection = client.get_collection("incident_runbooks")
    encoder = SentenceTransformer("all-MiniLM-L6-v2")
    
    query = """Users cannot login to VPN.
SSO portal unavailable.
Email notifications failing.
Multiple services reporting authentication errors.
LDAP bind failures observed."""

    print("=== RETRIEVING TOP 10 CHUNKS ===")
    query_embedding = encoder.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )
    
    if results and results.get("documents") and len(results["documents"]) > 0:
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        ids = results["ids"][0]
        
        for rank, (doc_id, doc, meta, dist) in enumerate(zip(ids, documents, metadatas, distances)):
            similarity_pct = round((1.0 - (dist / 2.0)) * 100, 1) if dist else 85.0
            print(f"Rank {rank+1}: [{doc_id}] {meta['title']} | Section: {meta['section']} (Score: {similarity_pct}%)")
            # Print a snippet of the document
            snippet = doc.replace('\n', ' ')[:150]
            print(f"  Snippet: {snippet}...")
    else:
        print("No matches found.")

if __name__ == "__main__":
    main()
