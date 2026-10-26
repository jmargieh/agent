"""RAG (Retrieval-Augmented Generation) tool for HR policy Q&A."""
import logging
import os
from typing import Any

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# In-memory document store for development.
# In production, this would be replaced with a persistent vector store.
_document_store: list[dict[str, Any]] = []
_sample_policies_loaded: bool = False

CONFIDENCE_THRESHOLD = 0.6


def _load_sample_policies() -> None:
    """Load sample HR policy documents into the in-memory store (development only)."""
    global _document_store, _sample_policies_loaded
    if _sample_policies_loaded:
        return  # Already loaded
    _sample_policies_loaded = True

    sample_data_dir = os.path.join(os.path.dirname(__file__), "data", "sample-policies")
    if not os.path.isdir(sample_data_dir):
        logger.warning("Sample policies directory not found at %s", sample_data_dir)
        return

    import glob

    for filepath in glob.glob(os.path.join(sample_data_dir, "*.txt")):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        doc_name = os.path.basename(filepath).replace(".txt", "")
        # Split into chunks (simple paragraph-based chunking for dev)
        chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
        for i, chunk in enumerate(chunks):
            _document_store.append(
                {
                    "document": doc_name,
                    "section": f"Section {i + 1}",
                    "content": chunk,
                }
            )
    logger.info("Loaded %d document chunks from sample policies", len(_document_store))


def _simple_keyword_search(query: str, top_k: int = 3) -> list[dict[str, Any]]:
    """Simple keyword-based search for development (replaced by vector search in production)."""
    _load_sample_policies()
    query_lower = query.lower()
    query_terms = query_lower.split()

    scored = []
    for doc in _document_store:
        content_lower = doc["content"].lower()
        # Count matching terms
        match_count = sum(1 for term in query_terms if term in content_lower)
        if match_count > 0:
            score = match_count / len(query_terms)
            scored.append({"score": score, **doc})

    # Sort by score descending
    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


@tool
def rag_query(question: str) -> dict[str, Any]:
    """Query the HR policy knowledge base for answers to HR policy questions.

    Use this tool for questions about HR policies, leave rules, benefits,
    company guidelines, and any other HR policy topics.

    Args:
        question: The HR policy question to answer.

    Returns:
        A dict with keys: answer (str), sources (list of dicts with document/section),
        confidence (float 0-1).
    """
    logger.info("RAG query: %s", question[:100])

    results = _simple_keyword_search(question)

    if not results:
        logger.info("RAG: no results found for query")
        return {
            "answer": "I was not able to find information about this topic in the HR policy documents.",
            "sources": [],
            "confidence": 0.0,
        }

    top_result = results[0]
    confidence = top_result["score"]

    # Build answer from top results
    answer_parts = []
    sources = []
    for r in results:
        if r["score"] > 0.2:
            answer_parts.append(r["content"])
            sources.append({"document": r["document"], "section": r["section"]})

    answer = "\n\n".join(answer_parts) if answer_parts else top_result["content"]

    logger.info(
        "RAG: found %d relevant chunks, top confidence=%.2f",
        len(results),
        confidence,
    )

    return {
        "answer": answer,
        "sources": sources,
        "confidence": confidence,
    }


def ingest_document(file_path: str) -> dict[str, Any]:
    """Ingest a document (PDF or .txt) into the knowledge base.

    Args:
        file_path: Path to the document file to ingest.

    Returns:
        A dict with keys: success (bool), chunks_added (int), document (str).
    """
    global _document_store

    if not os.path.exists(file_path):
        return {"success": False, "chunks_added": 0, "document": file_path, "error": "File not found"}

    doc_name = os.path.basename(file_path).rsplit(".", 1)[0]

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as exc:
        return {"success": False, "chunks_added": 0, "document": doc_name, "error": str(exc)}

    # Remove existing chunks for this document (update scenario) — mutate in-place
    existing = [d for d in _document_store if d["document"] != doc_name]
    _document_store.clear()
    _document_store.extend(existing)

    # Chunk content
    chunks = [c.strip() for c in content.split("\n\n") if c.strip()]
    for i, chunk in enumerate(chunks):
        _document_store.append(
            {
                "document": doc_name,
                "section": f"Section {i + 1}",
                "content": chunk,
            }
        )

    logger.info("Ingested document '%s': %d chunks added", doc_name, len(chunks))
    return {"success": True, "chunks_added": len(chunks), "document": doc_name}
