import os
from app.config import settings
from app.logging_config import logger

if os.environ.get("LIGHTWEIGHT_MODE", "false").lower() == "true" or os.environ.get("ENVIRONMENT", "development").lower() == "production":
    CHROMA_AVAILABLE = False
    logger.info("ChromaDB library import bypassed due to LIGHTWEIGHT_MODE/production environment.")
else:
    try:
        import chromadb
        CHROMA_AVAILABLE = True
    except ImportError:
        CHROMA_AVAILABLE = False
        logger.warning("ChromaDB library not found. RAG queries will fallback to standard text mapping index.")

class ChromaManager:
    def __init__(self):
        self.db_path = settings.CHROMA_DB_PATH
        self.client = None
        self.collection = None
        
        # Check folder presence
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path, exist_ok=True)
            
        self.initialize_client()

    def initialize_client(self):
        if not CHROMA_AVAILABLE:
            logger.info("ChromaDB client is disabled due to missing native library dependencies.")
            return
            
        try:
            # Persistent client configuration
            self.client = chromadb.PersistentClient(path=self.db_path)
            self.collection = self.client.get_or_create_collection(name="incident_runbooks")
            logger.info("ChromaDB persistent client connection established successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB persistent client: {str(e)}")
            self.client = None
            self.collection = None

    def get_collection(self):
        return self.collection

    def get_status(self) -> dict:
        return {
            "library_available": CHROMA_AVAILABLE,
            "connected": self.client is not None,
            "collection_exists": self.collection is not None,
            "storage_path": self.db_path
        }

chroma_manager = ChromaManager()
