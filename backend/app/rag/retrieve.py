import os
import sys

# Ensure backend root is on sys.path for relative imports
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if backend_dir not in sys.path:
    sys.path.append(backend_dir)

from app.rag.chroma_manager import chroma_manager
from app.rag.ingest import doc_ingestor
from app.logging_config import logger

class DocumentRetriever:
    def __init__(self):
        pass

    def retrieve_relevant_docs(self, query: str, limit: int = 3) -> list[dict]:
        collection = chroma_manager.get_collection()
        if not collection:
            logger.info("DocRetriever: Collection unavailable. Running keyword lookup fallback.")
            return self._keyword_lookup_fallback(query, limit)

        try:
            # Generate query embeddings if SentenceTransformer is active
            encoder = doc_ingestor.get_encoder()
            if encoder:
                query_embeddings = encoder.encode(query).tolist()
                results = collection.query(
                    query_embeddings=[query_embeddings],
                    n_results=limit
                )
            else:
                results = collection.query(
                    query_texts=[query],
                    n_results=limit
                )

            formatted_results = []
            if results and results.get("documents") and len(results["documents"]) > 0:
                documents = results["documents"][0]
                metadatas = results["metadatas"][0] if results.get("metadatas") else [{}] * len(documents)
                distances = results["distances"][0] if results.get("distances") else [0.0] * len(documents)
                ids = results["ids"][0]

                for doc_id, doc, meta, dist in zip(ids, documents, metadatas, distances):
                    # In ChromaDB, distance represents cosine/L2 distance. 
                    # Cosine distance ranges [0, 2] (0 = identical, 2 = opposite).
                    # We map this to a percentage similarity.
                    similarity_pct = round((1.0 - (dist / 2.0)) * 100, 1) if dist else 85.0
                    
                    formatted_results.append({
                        "id": doc_id,
                        "content": doc,
                        "title": meta.get("title", "Unknown Title"),
                        "source": meta.get("source", "Reference Documentation"),
                        "confidence_score": max(10.0, min(100.0, similarity_pct))
                    })
            
            if not formatted_results:
                return self._keyword_lookup_fallback(query, limit)
                
            return formatted_results

        except Exception as e:
            logger.error(f"DocRetriever: Search failed: {str(e)}")
            return self._keyword_lookup_fallback(query, limit)

    def _keyword_lookup_fallback(self, query: str, limit: int) -> list[dict]:
        # Return fallback items by checking for simple keywords matching documentation titles
        query_lower = query.lower()
        
        fallback_db = [
            {
                "id": "db_connectivity",
                "title": "SOP-094: PostgreSQL Connection Pool Exhaustion",
                "content": "Connection pool capacity drops below 5% or connection slots leak when connections are not released cleanly back to the HikariCP pool.\n\nDiagnostics:\n- PSQLException: FATAL: remaining connection slots are reserved\n\nMitigation:\n- ALTER SYSTEM SET max_connections = 400;",
                "source": "data/db_connectivity.md",
                "keywords": ["database", "connection", "postgresql", "hikari", "pool", "slots", "sql"]
            },
            {
                "id": "vpn_failure",
                "title": "SOP-101: Troubleshooting VPN Gateway Connection Failures",
                "content": "This standard operating procedure governs resolving network outages and authentication timeouts on the corporate VPN gateway clusters.\n\nDiagnostics:\n- IPSEC Tunnel Timeout\n\nMitigation:\n- systemctl restart ipsec-gateway",
                "source": "data/vpn_failure.md",
                "keywords": ["vpn", "gateway", "ipsec", "tunnel", "network", "timeout"]
            },
            {
                "id": "sso_failure",
                "title": "SOP-102: Single Sign-On (SSO) Authentication Failures",
                "content": "SSO failures occur when Okta / Active Directory credentials cannot synchronize or when SAML assertions expire.\n\nDiagnostics:\n- invalid_grant or signature_verification_failed\n\nMitigation:\n- okta-admin-sync --force-renew",
                "source": "data/sso_failure.md",
                "keywords": ["sso", "authentication", "okta", "saml", "active directory", "token", "sign-on"]
            },
            {
                "id": "app_crash",
                "title": "SOP-103: Application Crash Loop Backoff Failures",
                "content": "Occurs when deployment pods fail health checks or run out of memory (OOMKilled) under load.\n\nDiagnostics:\n- kubectl describe pod\n\nMitigation:\n- Increase pod resources memory limits.",
                "source": "data/app_crash.md",
                "keywords": ["crash", "loop", "backoff", "pod", "kubernetes", "kubectl", "oom", "memory"]
            },
            {
                "id": "email_failure",
                "title": "SOP-104: SMTP / Email Notification Delivery Failures",
                "content": "Occurs when downstream SMTP hosts drop notification socket attempts due to auth changes or load peaks.\n\nDiagnostics:\n- Connection refused or 535 Authentication failed\n\nMitigation:\n- telnet smtp.mail-provider.com 587",
                "source": "data/email_failure.md",
                "keywords": ["email", "smtp", "smtp host", "mail", "notification", "delivery"]
            }
        ]

        matches = []
        for doc in fallback_db:
            score = 0
            for kw in doc["keywords"]:
                if kw in query_lower:
                    score += 1
            if score > 0:
                doc_copy = doc.copy()
                doc_copy["confidence_score"] = min(75.0 + (score * 5.0), 99.0)
                matches.append(doc_copy)

        matches.sort(key=lambda x: x["confidence_score"], reverse=True)
        
        if not matches:
            return [{
                "id": "generic_sop",
                "title": "SOP-001: General Triaging Guide",
                "content": "For generic outages or unknown system behaviors, capture raw diagnostic stack traces, analyze memory dumps, query routing tables, and establish an incident triage channel on Slack.",
                "source": "data/generic_sop.md",
                "confidence_score": 50.0
            }]
            
        return matches[:limit]

document_retriever = DocumentRetriever()

def run_cli_retrieval():
    if len(sys.argv) < 2:
        print("Usage: python retrieve.py \"<your search query>\"")
        sys.exit(1)
        
    query = sys.argv[1]
    print(f"Searching index for: '{query}'\n")
    
    results = document_retriever.retrieve_relevant_docs(query, limit=2)
    
    for idx, match in enumerate(results):
        print(f"--- MATCH #{idx + 1} ---")
        print(f"Title:  {match['title']}")
        print(f"Source: {match['source']} (Match Score: {match['confidence_score']}%)")
        print(f"Content:\n{match['content']}")
        print("-" * 40 + "\n")

if __name__ == "__main__":
    run_cli_retrieval()
