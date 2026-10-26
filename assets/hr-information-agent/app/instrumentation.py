"""Business instrumentation for HR Information Agent milestones and ticket deflection tracking."""
import logging
from collections import defaultdict
from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)

# In-memory counters for ticket deflection tracking (feeds M4/M5 measurement)
_counters: dict[str, int] = defaultdict(int)


# ---------------------------------------------------------------------------
# Milestone log helpers
# ---------------------------------------------------------------------------

def log_m1_achieved() -> None:
    """M1: Agent answers general policy questions."""
    logger.info("M1.achieved: agent answers general policy questions - RAG knowledge base operational and accuracy threshold met")


def log_m1_missed(reason: str = "") -> None:
    """M1 missed: knowledge base not operational."""
    logger.warning("M1.missed: agent policy Q&A not operational - knowledge base ingestion incomplete or accuracy below threshold. Reason: %s", reason)


def log_m2_achieved() -> None:
    """M2: Personal HR data retrieval operational."""
    logger.info("M2.achieved: personal HR data retrieval operational - SuccessFactors API integration verified for authenticated user")


def log_m2_missed(reason: str = "") -> None:
    """M2 missed: SuccessFactors API not operational."""
    logger.warning("M2.missed: personal HR data retrieval not operational - SuccessFactors API integration incomplete or authentication failure. Reason: %s", reason)


def log_m3_achieved() -> None:
    """M3: Agent embedded in SuccessFactors with SSO."""
    logger.info("M3.achieved: agent embedded in SuccessFactors - SSO verified, no additional login required")


def log_m3_missed(reason: str = "") -> None:
    """M3 missed: SuccessFactors embedding not complete."""
    logger.warning("M3.missed: SuccessFactors embedding not complete - SSO configuration or Joule endpoint not operational. Reason: %s", reason)


def log_m4_achieved() -> None:
    """M4: Helpdesk deflection tracking active."""
    logger.info("M4.achieved: helpdesk deflection tracking active - 1-month post-launch measurement recorded")


def log_m4_missed(reason: str = "") -> None:
    """M4 missed: deflection tracking not in place."""
    logger.warning("M4.missed: deflection tracking not in place - measurement not taken at 1-month mark. Reason: %s", reason)


def log_m5_achieved() -> None:
    """M5: 30pct ticket reduction confirmed."""
    logger.info("M5.achieved: 30pct ticket reduction confirmed - monthly ticket volume at or below 14 at 3-month review")


def log_m5_missed(reason: str = "") -> None:
    """M5 missed: 30pct ticket reduction not met."""
    logger.warning("M5.missed: 30pct ticket reduction target not met - monthly ticket volume above 14 at 3-month review. Reason: %s", reason)


# ---------------------------------------------------------------------------
# Ticket deflection tracking (R8)
# ---------------------------------------------------------------------------

def record_deflected(query_type: str = "general") -> None:
    """Record a query resolved by the agent (deflected from helpdesk)."""
    _counters["deflected"] += 1
    logger.info("[DEFLECTED] query_type=%s total_deflected=%d", query_type, _counters["deflected"])


def record_escalated(reason: str = "unresolved") -> None:
    """Record a query escalated to a human HR agent."""
    _counters["escalated"] += 1
    logger.info("[ESCALATED] reason=%s total_escalated=%d", reason, _counters["escalated"])


def get_metrics_summary() -> dict[str, int]:
    """Return current deflection/escalation counts."""
    return {
        "deflected": _counters["deflected"],
        "escalated": _counters["escalated"],
        "total": _counters["deflected"] + _counters["escalated"],
    }


# ---------------------------------------------------------------------------
# OpenTelemetry span helpers
# ---------------------------------------------------------------------------

def rag_span():
    """Context manager span for RAG retrieval steps."""
    return tracer.start_as_current_span("hr.rag_retrieval")


def sf_api_span(operation: str):
    """Context manager span for SuccessFactors API calls."""
    return tracer.start_as_current_span(f"hr.sf_api.{operation}")


def escalation_span():
    """Context manager span for escalation routing."""
    return tracer.start_as_current_span("hr.escalation_routing")
