# Authentication: SuccessFactors SSO Token Passing

## Overview

The HR Information Agent uses the authenticated employee's SuccessFactors session token (JWT Bearer token) for all downstream SAP SuccessFactors API calls. This ensures personal HR data is always scoped to the authenticated user.

## Token Flow

1. Employee logs into SAP SuccessFactors (SSO via IAS/XSUAA)
2. SuccessFactors embeds the agent (Joule) with the employee's Bearer JWT in the `Authorization` header
3. The agent's `JWTContextMiddleware` in `main.py` extracts this token and stores it in a context variable
4. The `mcp_providers/agw.py` module reads the context variable and forwards the token to Agent Gateway for all MCP tool calls
5. Agent Gateway uses the token when calling SuccessFactors APIs, ensuring data is scoped to that employee

## Security Properties

- No service-account or admin-level credentials are used for personal data retrieval
- The `userId` is derived from the JWT sub-claim — never accepted as a user-supplied parameter
- Cross-employee data access is blocked at the tool layer (tools use session-scoped token)
- Tokens are never logged or persisted beyond the request lifecycle

## Local Development

During local development (`IBD_TESTING=true`), MCP tool calls are mocked via `mcp-mock.json`. No real SuccessFactors connection is made. See `conftest.py` for the mock patching mechanism.

## Deployment

At deployment time, the SAP BTP platform injects AI Core credentials via environment variables. The SuccessFactors connection is wired through SAP Agent Gateway, which handles credential rotation and mutual TLS.
