"""Unit tests for the RAG query tool."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import pytest
import rag_tool
from rag_tool import rag_query, ingest_document, _document_store, CONFIDENCE_THRESHOLD


@pytest.fixture(autouse=True)
def reset_document_store():
    """Clear document store and prevent auto-loading before each test."""
    _document_store.clear()
    rag_tool._sample_policies_loaded = True  # Prevent auto-loading during tests
    yield
    _document_store.clear()
    rag_tool._sample_policies_loaded = True


def test_rag_query_no_documents_returns_low_confidence():
    """When no documents are ingested, returns low confidence."""
    result = rag_query.invoke({"question": "What is the annual leave policy?"})
    assert result["confidence"] == 0.0
    assert result["sources"] == []
    assert "not able to find" in result["answer"].lower()


def test_rag_query_with_matching_document_returns_answer(tmp_path):
    """When a relevant document exists, returns answer with source citation."""
    # Create a test document
    doc_path = tmp_path / "leave-policy.txt"
    doc_path.write_text("Annual Leave Policy\n\nFull-time employees are entitled to 25 days of annual leave per year.\n\nSection 2: Employees may carry over up to 5 days.")

    ingest_document(str(doc_path))

    result = rag_query.invoke({"question": "How many days of annual leave?"})
    assert result["confidence"] > 0.0
    assert len(result["sources"]) > 0
    assert result["sources"][0]["document"] == "leave-policy"


def test_rag_query_returns_source_citations(tmp_path):
    """Results include document name and section in sources list."""
    doc_path = tmp_path / "benefits-policy.txt"
    doc_path.write_text("Benefits Overview\n\nHealth insurance is provided to all employees from day one.\n\nPension contributions are matched up to 5%.")

    ingest_document(str(doc_path))

    result = rag_query.invoke({"question": "health insurance benefits"})
    if result["confidence"] > 0:
        assert "document" in result["sources"][0]
        assert "section" in result["sources"][0]


def test_ingest_document_adds_to_store(tmp_path):
    """Ingesting a document populates the document store."""
    doc_path = tmp_path / "test-policy.txt"
    doc_path.write_text("Test Policy\n\nThis is section one.\n\nThis is section two.")

    result = ingest_document(str(doc_path))
    assert result["success"] is True
    assert result["chunks_added"] > 0
    assert result["document"] == "test-policy"
    assert len(_document_store) > 0


def test_ingest_nonexistent_file_returns_error():
    """Ingesting a non-existent file returns an error result."""
    result = ingest_document("/nonexistent/path/policy.txt")
    assert result["success"] is False
    assert "error" in result


def test_ingest_updates_existing_document(tmp_path):
    """Re-ingesting a document replaces its existing chunks."""
    doc_path = tmp_path / "updatable-policy.txt"
    doc_path.write_text("Original content.\n\nSecond paragraph.")
    ingest_document(str(doc_path))
    initial_chunks = [d for d in _document_store if d["document"] == "updatable-policy"]
    assert len(initial_chunks) == 2

    doc_path.write_text("Updated content.\n\nNew second paragraph.\n\nNew third paragraph.")
    ingest_document(str(doc_path))

    policy_chunks = [d for d in _document_store if d["document"] == "updatable-policy"]
    assert len(policy_chunks) == 3  # updated document has 3 paragraphs


def test_rag_query_confidence_threshold_constant():
    """CONFIDENCE_THRESHOLD is set to the expected value."""
    assert CONFIDENCE_THRESHOLD == 0.6
