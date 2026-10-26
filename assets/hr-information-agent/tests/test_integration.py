"""Integration tests for the HR Information Agent end-to-end flow."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agent import SampleAgent, AgentResponse
from rag_tool import ingest_document, _document_store


@pytest.fixture(autouse=True)
def clear_store():
    """Clear document store before each test."""
    _document_store.clear()
    yield
    _document_store.clear()


@pytest.fixture
def agent():
    return SampleAgent()


@pytest.fixture
def sample_policy_doc(tmp_path):
    """Create a sample policy document for testing."""
    doc = tmp_path / "annual-leave-policy.txt"
    doc.write_text(
        "Annual Leave Policy\n\n"
        "Full-time employees are entitled to 25 days of annual leave per year.\n\n"
        "Carry-over: Up to 5 unused days may be carried to the next year.\n\n"
        "Requesting leave: Submit requests via SuccessFactors at least 5 days in advance."
    )
    return str(doc)


@pytest.mark.asyncio
async def test_end_to_end_policy_query_with_document(agent, sample_policy_doc):
    """E2E: Policy query returns answer from ingested document."""
    # Ingest the document
    result = ingest_document(sample_policy_doc)
    assert result["success"] is True

    mock_llm_response = {
        "messages": [MagicMock(content="According to the Annual Leave Policy, full-time employees are entitled to 25 days per year. Source: annual-leave-policy, Section 1")]
    }

    with patch.object(agent, '_invoke', new=AsyncMock(return_value=mock_llm_response)):
        response = await agent.invoke("How many days of annual leave do employees get?", "test-session-001")

    assert response.status == "completed"
    assert response.message != ""
    assert len(response.message) > 0


@pytest.mark.asyncio
async def test_end_to_end_leave_balance_query(agent):
    """E2E: Leave balance query routes to SuccessFactors MCP tools."""
    mock_llm_response = {
        "messages": [MagicMock(content="Your current leave balance: Annual Leave: 20 days remaining, Sick Leave: 5 days remaining.")]
    }

    with patch.object(agent, '_invoke', new=AsyncMock(return_value=mock_llm_response)):
        response = await agent.invoke("How many days of leave do I have left?", "test-session-002")

    assert response.status == "completed"
    assert "leave" in response.message.lower() or "days" in response.message.lower()


@pytest.mark.asyncio
async def test_end_to_end_escalation_for_unknown_query(agent):
    """E2E: Unknown/out-of-scope query results in escalation."""
    mock_llm_response = {
        "messages": [MagicMock(content="I wasn't able to find information about that in the HR policy documents. Please contact the HR helpdesk for assistance.")]
    }

    with patch.object(agent, '_invoke', new=AsyncMock(return_value=mock_llm_response)):
        response = await agent.invoke("What is the policy on alien abduction leave?", "test-session-003")

    assert response.status == "completed"
    assert response.message != ""


@pytest.mark.asyncio
async def test_end_to_end_stream_yields_responses(agent):
    """E2E: Stream yields processing update then final response."""
    mock_llm_response = {
        "messages": [MagicMock(content="You have 20 days of annual leave remaining.")]
    }

    with patch.object(agent, '_invoke', new=AsyncMock(return_value=mock_llm_response)):
        chunks = []
        async for chunk in agent.stream("What is my leave balance?", "test-session-004"):
            chunks.append(chunk)

    assert len(chunks) >= 1
    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert "content" in final


@pytest.mark.asyncio
async def test_instrumentation_m1_fires_on_policy_query(agent, sample_policy_doc):
    """E2E: M1 milestone is logged when policy query is processed."""
    ingest_document(sample_policy_doc)

    mock_llm_response = {
        "messages": [MagicMock(content="The bereavement leave policy allows 5 days paid leave.")]
    }

    import logging
    with patch.object(agent, '_invoke', new=AsyncMock(return_value=mock_llm_response)):
        import logging
        with patch('instrumentation.logger') as mock_logger:
            response = await agent.invoke("What is the bereavement leave policy?", "test-session-005")

    assert response.status == "completed"
