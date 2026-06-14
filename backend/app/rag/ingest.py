import os
import glob
import sys

# Ensure backend root is on sys.path for relative imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.rag.chroma_manager import chroma_manager
from app.logging_config import logger

if os.environ.get("LIGHTWEIGHT_MODE", "false").lower() == "true" or os.environ.get("ENVIRONMENT", "development").lower() == "production":
    EMBEDDINGS_AVAILABLE = False
    logger.info("SentenceTransformer library import bypassed due to LIGHTWEIGHT_MODE/production environment.")
else:
    try:
        from sentence_transformers import SentenceTransformer
        EMBEDDINGS_AVAILABLE = True
    except ImportError:
        EMBEDDINGS_AVAILABLE = False
        logger.warning("sentence-transformers not available. Embeddings generation will run in fallback mock mode.")

class DocIngestor:
    def __init__(self):
        self.encoder = None

    def get_encoder(self):
        if self.encoder is None and EMBEDDINGS_AVAILABLE:
            try:
                logger.info("DocIngestor: Lazy loading SentenceTransformer model...")
                self.encoder = SentenceTransformer("all-MiniLM-L6-v2")
                logger.info("DocIngestor: SentenceTransformer model loaded successfully.")
            except Exception as e:
                logger.error(f"DocIngestor: Failed to load sentence-transformers model: {str(e)}")
                self.encoder = None
        return self.encoder

    def ingest_document(self, doc_id: str, title: str, content: str, source: str) -> bool:
        collection = chroma_manager.get_collection()
        if not collection:
            logger.warning("DocIngestor: Cannot index; ChromaDB collection is unavailable.")
            return False

        try:
            # Generate real embeddings if encoder model is loaded
            embeddings = None
            encoder = self.get_encoder()
            if encoder:
                embeddings = encoder.encode(content).tolist()

            metadata = {
                "title": title,
                "source": source
            }

            # If document already exists, update/upsert it
            collection.upsert(
                ids=[doc_id],
                documents=[content],
                metadatas=[metadata],
                embeddings=[embeddings] if embeddings else None
            )
            logger.info(f"DocIngestor: Successfully upserted document '{title}' (ID: {doc_id})")
            return True
        except Exception as e:
            logger.error(f"DocIngestor: Ingestion failed for ID {doc_id}: {str(e)}")
            return False

doc_ingestor = DocIngestor()

def run_cli_ingestion():
    # Look for files inside data/ folder
    base_project_dir = os.path.dirname(backend_dir)
    data_dir = os.path.join(base_project_dir, "data")
    
    logger.info(f"RAG CLI Ingest: Scanning markdown SOP files in '{data_dir}'...")
    md_files = glob.glob(os.path.join(data_dir, "*.md"))
    
    if not md_files:
        logger.warning(f"RAG CLI Ingest: No markdown files discovered in '{data_dir}'.")
        return
        
    logger.info(f"RAG CLI Ingest: Found {len(md_files)} files. Initiating parsing & vector storage...")
    
    success_count = 0
    for file_path in md_files:
        file_name = os.path.basename(file_path)
        doc_id = file_name.replace(".md", "")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Extract title (first H1 line)
            title = doc_id.upper().replace("_", " ")
            for line in content.split("\n"):
                if line.startswith("# "):
                    title = line.replace("# ", "").strip()
                    break
                    
            success = doc_ingestor.ingest_document(
                doc_id=doc_id,
                title=title,
                content=content,
                source=f"data/{file_name}"
            )
            
            if success:
                success_count += 1
                print(f"[SUCCESS] Indexed: {file_name} -> '{title}'")
            else:
                print(f"[FAILED] Failed to index: {file_name}")
                
        except Exception as e:
            logger.error(f"RAG CLI Ingest: Failed parsing {file_name}: {str(e)}")
            
    print(f"\nIngestion Complete. Successfully indexed {success_count}/{len(md_files)} documents into ChromaDB.")

if __name__ == "__main__":
    run_cli_ingestion()
