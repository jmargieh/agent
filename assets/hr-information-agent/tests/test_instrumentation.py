"""Unit tests for business instrumentation (milestones and deflection tracking)."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

import pytest
from instrumentation import (
    log_m1_achieved, log_m1_missed,
    log_m2_achieved, log_m2_missed,
    log_m3_achieved,
    log_m4_achieved, log_m5_achieved,
    record_deflected, record_escalated,
    get_metrics_summary,
    _counters,
)


def setup_function():
    """Reset counters before each test."""
    _counters.clear()


def test_record_deflected_increments_counter():
    """Recording a deflected query increments the deflected counter."""
    record_deflected("policy")
    summary = get_metrics_summary()
    assert summary["deflected"] == 1
    assert summary["escalated"] == 0
    assert summary["total"] == 1


def test_record_escalated_increments_counter():
    """Recording an escalated query increments the escalated counter."""
    record_escalated("low_confidence")
    summary = get_metrics_summary()
    assert summary["escalated"] == 1
    assert summary["deflected"] == 0
    assert summary["total"] == 1


def test_metrics_summary_tracks_both_types():
    """Metrics summary correctly aggregates both deflected and escalated queries."""
    record_deflected("policy")
    record_deflected("personal_data")
    record_escalated("out_of_scope")
    summary = get_metrics_summary()
    assert summary["deflected"] == 2
    assert summary["escalated"] == 1
    assert summary["total"] == 3


def test_milestone_log_m1_achieved_does_not_raise(caplog):
    """M1 achieved log statement executes without error."""
    import logging
    with caplog.at_level(logging.INFO):
        log_m1_achieved()
    assert "M1.achieved" in caplog.text


def test_milestone_log_m1_missed_does_not_raise(caplog):
    """M1 missed log statement executes without error."""
    import logging
    with caplog.at_level(logging.WARNING):
        log_m1_missed("test reason")
    assert "M1.missed" in caplog.text


def test_milestone_log_m2_achieved_does_not_raise(caplog):
    """M2 achieved log statement executes without error."""
    import logging
    with caplog.at_level(logging.INFO):
        log_m2_achieved()
    assert "M2.achieved" in caplog.text


def test_milestone_log_m2_missed_does_not_raise(caplog):
    """M2 missed log statement executes without error."""
    import logging
    with caplog.at_level(logging.WARNING):
        log_m2_missed("api failure")
    assert "M2.missed" in caplog.text


def test_milestone_log_m3_achieved_does_not_raise(caplog):
    """M3 achieved (SSO) log statement executes without error."""
    import logging
    with caplog.at_level(logging.INFO):
        log_m3_achieved()
    assert "M3.achieved" in caplog.text


def test_counters_start_at_zero():
    """Counters start at zero before any recording."""
    summary = get_metrics_summary()
    assert summary["deflected"] == 0
    assert summary["escalated"] == 0
    assert summary["total"] == 0
