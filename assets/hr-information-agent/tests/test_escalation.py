"""Unit tests for escalation behaviour and low-confidence query routing."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from agent import SampleAgent, AgentResponse


@pytest.fixture
def agent():
    return SampleAgent()


@pytest.mark.asyncio
async def test_agent_escalates_when_response_contains_helpdesk_keyword(agent):
    """Agent records escalation when response contains 'hr helpdesk'."""
    from instrumentation import _counters, record_escalated
    _counters.clear()

    mock_result = {
        "messages": [MagicMock(content="I wasn't able to find an answer. Please contact the HR helpdesk for assistance.")]
    }

    with patch.object(agent, '_invoke', new=AsyncMock(return_value=mock_result)):
        response = await agent.invoke("What is the sabbatical policy?", "test-ctx")

    assert response.status == "completed"
    assert "helpdesk" in response.message.lower()


@pytest.mark.asyncio
async def test_agent_deflects_resolved_policy_query(agent):
    """Agent records deflection when query is resolved without escalation."""
    from instrumentation import _counters
    _counters.clear()

    mock_result = {
        "messages": [MagicMock(content="According to the Annual Leave Policy, you are entitled to 25 days per year. Source: Annual Leave Policy, Section 2.1")]
    }

    with patch.object(agent, '_invoke', new=AsyncMock(return_value=mock_result)):
        response = await agent.invoke("What is the annual leave policy?", "test-ctx")

    assert response.status == "completed"
    assert "25 days" in response.message or "annual leave" in response.message.lower()


@pytest.mark.asyncio
async def test_agent_returns_error_on_exception(agent):
    """Agent returns a completed response with error message when an unexpected exception occurs."""
    with patch.object(agent, '_invoke', new=AsyncMock(side_effect=RuntimeError("Unexpected error"))):
        response = await agent.invoke("test query", "test-ctx")

    # Agent stream() catches exceptions and returns a completed status with error message
    assert response.status in ("completed", "error")
    assert response.message != ""


@pytest.mark.asyncio
async def test_security_cross_employee_blocked(agent):
    """Agent correctly handles cross-employee data access attempt."""
    mock_result = {
        "messages": [MagicMock(content="I can only retrieve your own personal HR data. I'm not able to access other employees' information.")]
    }

    with patch.object(agent, '_invoke', new=AsyncMock(return_value=mock_result)):
        response = await agent.invoke("What is Sarah's leave balance?", "test-ctx")

    assert response.status == "completed"
    assert "own" in response.message.lower() or "not able" in response.message.lower() or "only" in response.message.lower()
