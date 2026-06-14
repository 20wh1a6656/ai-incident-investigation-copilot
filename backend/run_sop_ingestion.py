import os
import sys
import glob

# Set working directory to backend root if run from elsewhere
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.rag.chroma_manager import chroma_manager
from sentence_transformers import SentenceTransformer

def main():
    # 1. Reset collection
    print("Initializing ChromaDB collection...")
    client = chroma_manager.client
    if not client:
        print("Error: ChromaDB client is not available.")
        sys.exit(1)
        
    collection_name = "incident_runbooks"
    try:
        client.delete_collection(collection_name)
        print(f"Deleted existing collection '{collection_name}'.")
    except Exception as e:
        print(f"No existing collection '{collection_name}' to delete, or deletion failed: {e}")
        
    collection = client.create_collection(name=collection_name)
    print(f"Created new collection '{collection_name}'.")

    # Load sentence-transformers model
    print("Loading sentence-transformers model (all-MiniLM-L6-v2)...")
    encoder = SentenceTransformer("all-MiniLM-L6-v2")
    print("Model loaded successfully.")

    # 2. Find all markdown files in data/sops/
    # Since we are running in backend/, the relative path to data/sops/ is ../data/sops/
    project_root = os.path.dirname(backend_dir)
    sops_dir = os.path.join(project_root, "data", "sops")
    print(f"Scanning SOP files in: {sops_dir}")
    sop_files = glob.glob(os.path.join(sops_dir, "*.md"))
    
    if not sop_files:
        print(f"Error: No SOP files found in {sops_dir}")
        sys.exit(1)
        
    print(f"Found {len(sop_files)} SOP files.")

    total_chunks = 0
    all_documents = []
    all_metadatas = []
    all_ids = []
    
    # 3. Read and chunk each SOP
    for filepath in sop_files:
        filename = os.path.basename(filepath)
        doc_id_base = filename.replace(".md", "")
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        lines = content.split("\n")
        title = ""
        for line in lines:
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if not title:
            title = doc_id_base.replace("_", " ").title()
            
        # Parse sections
        current_section = "Header"
        current_lines = []
        sections = []
        
        for line in lines:
            if line.startswith("# ") and line.strip() != f"# {title}":
                if current_lines:
                    sections.append((current_section, "\n".join(current_lines).strip()))
                current_section = line[2:].strip()
                current_lines = [line]
            else:
                current_lines.append(line)
        if current_lines:
            sections.append((current_section, "\n".join(current_lines).strip()))
            
        # Process chunks
        for idx, (section_title, section_content) in enumerate(sections):
            if not section_content.strip():
                continue
                
            chunk_doc = f"SOP Title: {title}\nSection: {section_title}\n\n{section_content}"
            chunk_id = f"{doc_id_base}_chunk_{idx}"
            
            metadata = {
                "title": title,
                "section": section_title,
                "source": f"data/sops/{filename}"
            }
            
            all_documents.append(chunk_doc)
            all_metadatas.append(metadata)
            all_ids.append(chunk_id)
            total_chunks += 1
            
    print(f"Total chunks created: {total_chunks}")
    
    # 4. Generate embeddings and store vectors in ChromaDB
    print("Generating embeddings and inserting vectors into ChromaDB...")
    # Generate embeddings in batch
    embeddings = encoder.encode(all_documents, show_progress_bar=True).tolist()
    
    # Add to ChromaDB in batches to prevent payload limits
    batch_size = 100
    for i in range(0, len(all_ids), batch_size):
        end = min(i + batch_size, len(all_ids))
        collection.add(
            ids=all_ids[i:end],
            documents=all_documents[i:end],
            metadatas=all_metadatas[i:end],
            embeddings=embeddings[i:end]
        )
        print(f"Inserted batch {i//batch_size + 1}: {i} to {end}...")

    # Get count of vectors in ChromaDB
    vector_count = collection.count()
    print("\n=== INGESTION METRICS ===")
    print(f"Number of SOP files: {len(sop_files)}")
    print(f"Number of chunks:    {total_chunks}")
    print(f"Number of vectors:   {vector_count}")
    print("=========================\n")

    # 5. Run retrieval tests
    test_queries = [
        "Users cannot login to VPN",
        "LDAP bind failures observed",
        "SMTP authentication failing",
        "NXDOMAIN DNS lookup failures",
        "Database connection pool exhausted"
    ]
    
    print("=== RUNNING RETRIEVAL TESTS ===")
    for query in test_queries:
        print(f"\nQuery: '{query}'")
        query_embedding = encoder.encode(query).tolist()
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=5
        )
        
        if results and results.get("documents") and len(results["documents"]) > 0:
            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]
            ids = results["ids"][0]
            
            for rank, (doc_id, doc, meta, dist) in enumerate(zip(ids, documents, metadatas, distances)):
                # Map distance to similarity score percentage
                # cosine distance is [0, 2], similarity = (1 - dist/2) * 100
                similarity_pct = round((1.0 - (dist / 2.0)) * 100, 1) if dist else 85.0
                print(f"  {rank+1}. [{doc_id}] {meta['title']} | Section: {meta['section']} (Score: {similarity_pct}%)")
        else:
            print("  No matching documents found.")
            
if __name__ == "__main__":
    main()
