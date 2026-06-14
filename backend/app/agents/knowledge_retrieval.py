from app.schemas.investigation_state import InvestigationState
from app.rag.retrieve import document_retriever
from app.logging_config import logger

class KnowledgeRetrievalAgent:
    def execute(self, state: InvestigationState) -> InvestigationState:
        # Mandatory logs requirement
        logger.info("[Knowledge Retrieval Agent] Started")
        
        state.console_audit.append("Knowledge Retrieval Agent: Initializing semantic index query...")

        # Construct a search query from description and classification
        query_text = f"{state.classification} {state.description}"
        state.console_audit.append("Knowledge Retrieval Agent: Querying runbooks matching context terms...")

        # Call RAG retriever to fetch top 10 SOP chunks
        matching_docs = document_retriever.retrieve_relevant_docs(query_text, limit=10)
        state.evidence["retrieved_chunks"] = matching_docs
        
        if matching_docs:
            top_doc = matching_docs[0]
            state.evidence.update({
                "sopName": top_doc["title"],
                "snippet": top_doc["content"],
                "source": top_doc["source"],
                "strength": f"{top_doc['confidence_score']}% Match"
            })
            state.console_audit.append(f"Knowledge Retrieval Agent: Retrieved {len(matching_docs)} relevant SOP chunks. Top match: {top_doc['title']} (Score: {top_doc['confidence_score']}%)")
        else:
            state.evidence.update({
                "sopName": "SOP-001: General Triaging Guide",
                "snippet": "No specific runbooks found in the local Chroma indexing paths. Please review logs manually.",
                "source": "Standard Operating System Playbook",
                "strength": "50% Match"
            })
            state.console_audit.append("Knowledge Retrieval Agent: No specific matches found. Using general SOP.")

        # Mandatory logs requirement
        logger.info("[Knowledge Retrieval Agent] Completed")
        return state

knowledge_retrieval_agent = KnowledgeRetrievalAgent()
