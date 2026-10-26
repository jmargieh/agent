"""HR data retrieval tools using MCP tools for SAP SuccessFactors integration."""
import logging
from typing import Any

from langchain_core.tools import tool
from util import call_mcp_tool

logger = logging.getLogger(__name__)


@tool
async def get_leave_balance() -> dict[str, Any]:
    """Retrieve the authenticated employee's current leave balance from SAP SuccessFactors.

    Returns leave balances for all leave types (annual, sick, etc.) for the
    currently authenticated employee. Never retrieves data for other employees.

    Returns:
        A dict with the employee's leave balance information.
    """
    logger.info("Fetching leave balance for authenticated employee")
    try:
        result = await call_mcp_tool(
            "sap-sf-time-off-mcp-server",
            "listTimeAccountDetail",
            {},
        )
        logger.info("Leave balance retrieved successfully")
        return result
    except Exception as exc:
        logger.error("Failed to retrieve leave balance: %s", str(exc))
        return {
            "error": str(exc),
            "message": "Unable to retrieve leave balance from SuccessFactors.",
        }


@tool
async def get_employee_profile() -> dict[str, Any]:
    """Retrieve the authenticated employee's personal profile from SAP SuccessFactors.

    Returns profile information (name, contact details, department, manager)
    for the currently authenticated employee only.

    Returns:
        A dict with the employee's profile information.
    """
    logger.info("Fetching employee profile for authenticated employee")
    try:
        result = await call_mcp_tool(
            "sap-sf-employee-profile-mcp-server",
            "listEmpProfile",
            {},
        )
        logger.info("Employee profile retrieved successfully")
        return result
    except Exception as exc:
        logger.error("Failed to retrieve employee profile: %s", str(exc))
        return {
            "error": str(exc),
            "message": "Unable to retrieve employee profile from SuccessFactors.",
        }


@tool
async def get_employee_global_info() -> dict[str, Any]:
    """Retrieve the authenticated employee's global employment information from SAP SuccessFactors.

    Returns employment details (job title, start date, company, location)
    for the currently authenticated employee only.

    Returns:
        A dict with the employee's global employment information.
    """
    logger.info("Fetching employee global info for authenticated employee")
    try:
        result = await call_mcp_tool(
            "sap-sf-employee-central-ec-mcp-server",
            "listEmpGlobalAssignment",
            {},
        )
        logger.info("Employee global info retrieved successfully")
        return result
    except Exception as exc:
        logger.error("Failed to retrieve employee global info: %s", str(exc))
        return {
            "error": str(exc),
            "message": "Unable to retrieve employment information from SuccessFactors.",
        }
