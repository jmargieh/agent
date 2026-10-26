# Specification: hr-information-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [ ] Read `product-requirements-document.md` and `intent.md` for full context before starting
- [ ] Bootstrap agent code in `assets/hr-information-agent/` using instructions from the sap-agent-bootstrap section (invoke from inside `assets/hr-information-agent/`, use copy commands — do NOT create files manually)
- [ ] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

> **Before proceeding**, read [guidelines-agent-skills.md](../guidelines-agent-skills.md) and decide — based on the PRD/intent — whether the agent needs runtime skills.

The following runtime skills are required based on the PRD's business logic:

- [ ] Create `assets/hr-information-agent/app/skills/hr-policy-qa/SKILL.md` — provides instructions for answering HR policy questions using RAG retrieval, including how to cite source documents, when to acknowledge uncertainty, and when to escalate
- [ ] Create `assets/hr-information-agent/app/skills/hr-data-retrieval/SKILL.md` — provides instructions for retrieving personal HR data (leave balance, profile) from SuccessFactors, scoping all queries strictly to the authenticated employee
- [ ] Create `assets/hr-information-agent/app/skills/escalation/SKILL.md` — provides instructions for when and how to escalate to a human HR agent, including the escalation message format and confidence threshold logic

---

## Project-Specific Tasks

### R1 — HR Policy Question Answering (RAG Knowledge Base)

- [ ] Implement a RAG knowledge base tool (`rag_query`) in the agent that accepts a natural-language question and returns relevant excerpts from ingested HR policy documents
- [ ] Configure the RAG tool to use SAP Generative AI Hub for both the embedding model (document ingestion) and the LLM (answer generation)
- [ ] Ensure each answer includes the source document name and section/page number as a citation (R7 — source citation)
- [ ] Set a confidence threshold: if retrieval score is below the threshold, the agent must acknowledge it cannot answer confidently and offer escalation (R4)
- [ ] Implement document ingestion pipeline accepting PDF and Word (.docx) files; write ingested vectors to an in-memory vector store (development) with a clear seam for swapping to a persistent store at deployment
- [ ] Add a seed set of at least 3 sample HR policy documents to `assets/hr-information-agent/app/data/sample-policies/` for development and testing (leave policy, benefits overview, bereavement policy)

### R2 — Personal HR Data Retrieval (SuccessFactors API)

- [ ] Implement MCP-based tool (`get_leave_balance`) that retrieves the authenticated employee's leave balance by calling the generated MCP server for `sap.sf:apiResource:ECTimeOff:v1`
- [ ] Implement MCP-based tool (`get_employee_profile`) that retrieves the authenticated employee's personal profile by calling the generated MCP server for `sap.sf:apiResource:ECEmployeeProfile:v1`
- [ ] Implement MCP-based tool (`get_employee_global_info`) that retrieves general employment information from `sap.sf:apiResource:EmployeeCentralEC:v1`
- [ ] All SuccessFactors API calls MUST use the authenticated employee's session token — never a service account or generic credential (R6 — personal data scoping)
- [ ] Implement graceful degradation: if a SuccessFactors API call fails, the agent informs the employee and directs them to the HR helpdesk (R2 acceptance criteria — API failure path)
- [ ] Never return another employee's data regardless of query phrasing — enforce scoping at the tool layer (R6)

### R3 — SuccessFactors Embedding & SSO

- [ ] Configure the agent's A2A endpoint to accept and forward the SuccessFactors SSO token for all downstream API calls — document the token-passing mechanism in `assets/hr-information-agent/app/auth/README.md`
- [ ] Expose the agent as a Joule-compatible A2A endpoint (`.well-known/agent.json` must include Joule-compatible metadata)
- [ ] Verify the agent correctly identifies the authenticated user from the incoming SSO token and sets `userId` in all SuccessFactors API calls

### R4 — Human Escalation

- [ ] Implement escalation logic: when agent confidence is below threshold OR query is out of scope, respond with a clear escalation message and provide the HR helpdesk contact information
- [ ] Escalation trigger conditions: (a) RAG confidence below threshold, (b) SuccessFactors API unavailable, (c) query topic outside the agent's defined scope
- [ ] Log each escalation event for ticket deflection tracking (feeds M4/M5 milestone measurement)

### R5 — HR Policy Document Ingestion

- [ ] Implement a document ingestion entry point (`ingest_document(file_path)`) that accepts PDF and Word files, chunks them, embeds them, and stores vectors in the knowledge base
- [ ] Expose ingestion as an admin-only endpoint (not accessible to regular employees) — document the expected admin workflow in the skill file
- [ ] Ingestion must handle both PDF (`.pdf`) and Word (`.docx`) formats

### R6 — Personal Data Scoping & Security

- [ ] Add a guardrail check at the agent layer: before any SuccessFactors API call, assert that `userId` matches the authenticated session user — reject any attempt to query another employee's data
- [ ] Ensure no PII is written to agent logs or telemetry spans (redact `userId`, names, leave values from log output; log only anonymised metrics)
- [ ] Write a security unit test that verifies cross-employee data access is blocked

### R7 — Source Citation in Policy Answers

- [ ] Ensure `rag_query` tool returns both the answer text and a `sources` list (document name + section) for each policy answer
- [ ] Agent system prompt must instruct the agent to always include source citations when answering policy questions

### R8 — Ticket Deflection Tracking

- [ ] Implement a simple resolution tracker: log `[DEFLECTED]` for queries resolved by the agent and `[ESCALATED]` for queries routed to a human — these logs feed the M4/M5 measurement
- [ ] Add a lightweight metrics endpoint (`/metrics/summary`) returning counts of deflected vs escalated queries (in-memory counters for development)

---

## MCP Tool Integration

> Read [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) for complete MCP integration patterns.

- [ ] Verify `specification/hr-information-agent/api-specs/` contains the following downloaded spec files:
  - `employee-central-ec.edmx` (ORD ID: `sap.sf:apiResource:EmployeeCentralEC:v1`)
  - `employee-profile.edmx` (ORD ID: `sap.sf:apiResource:ECEmployeeProfile:v1`)
  - `time-off.edmx` (ORD ID: `sap.sf:apiResource:ECTimeOff:v1`)
- [ ] Invoke `mcp-translation-file` skill for each API spec to generate MCP translation cards:
  - `employee-central-ec.edmx` → MCP server for employee global information
  - `employee-profile.edmx` → MCP server for employee profile data
  - `time-off.edmx` → MCP server for leave/time-off balance
- [ ] Invoke `setup-solution` skill to register each generated MCP asset in `solution.yaml` and `asset.yaml`
- [ ] Wire MCP tool loading in `agent.py` using `get_mcp_tools()` from the `mcp_tools` module — NEVER import directly from `sap_cloud_sdk.agentgateway`; NEVER use direct HTTP clients for SAP APIs
- [ ] Add all 3 MCP server dependencies to `asset.yaml` under `requires` using the exact ORD IDs from the generated assets
- [ ] Generate `mcp-mock.json` using the `mcp-mock-config` skill (required before tests can run)

**MCP API: sap.sf:apiResource:EmployeeCentralEC:v1**
MCP tool scope: read-only
Resources in scope: EmpGlobalAssignment, EmpJob, EmpEmployment

**MCP API: sap.sf:apiResource:ECEmployeeProfile:v1**
MCP tool scope: read-only
Resources in scope: EmpProfile, PerPersonal, PerEmail

**MCP API: sap.sf:apiResource:ECTimeOff:v1**
MCP tool scope: read-only
Resources in scope: TimeAccountDetail, TimeAccountSnapshot, TimeType

---

## Business Instrumentation

- [ ] Implement milestone log statements following `[MILESTONE_ID].[achieved|missed]: [description]` pattern:
  - `M1.achieved: agent answers general policy questions — RAG knowledge base operational and accuracy threshold met`
  - `M1.missed: agent policy Q&A not operational — knowledge base ingestion incomplete or accuracy below threshold`
  - `M2.achieved: personal HR data retrieval operational — SuccessFactors API integration verified for authenticated user`
  - `M2.missed: personal HR data retrieval not operational — SuccessFactors API integration incomplete or authentication failure`
  - `M3.achieved: agent embedded in SuccessFactors — SSO verified, no additional login required`
  - `M3.missed: SuccessFactors embedding not complete — SSO configuration or Joule endpoint not operational`
  - `M4.achieved: helpdesk deflection tracking active — 1-month post-launch measurement recorded`
  - `M4.missed: deflection tracking not in place — measurement not taken at 1-month mark`
  - `M5.achieved: 30% ticket reduction confirmed — monthly ticket volume at or below 14 at 3-month review`
  - `M5.missed: 30% ticket reduction target not met — monthly ticket volume above 14 at 3-month review`
- [ ] Add OpenTelemetry custom spans for each business step (RAG retrieval, SuccessFactors API call, escalation routing)
- [ ] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## Testing

> See [guidelines-agent-python.md](../guidelines-agent-python.md) for Python testing setup and patterns.

- [ ] `conftest.py` only sets `IBD_TESTING=true` — this causes the agent to run with mock MCP tool results during tests
- [ ] Write unit tests in `assets/hr-information-agent/tests/` — one per tool:
  - `test_rag_query.py` — verify policy question returns answer with source citation
  - `test_get_leave_balance.py` — verify leave balance retrieval for authenticated user
  - `test_get_employee_profile.py` — verify profile retrieval for authenticated user
  - `test_get_employee_global_info.py` — verify global employment info retrieval
  - `test_escalation.py` — verify low-confidence queries trigger escalation
  - `test_security.py` — verify cross-employee data access is blocked
- [ ] Write one integration test executing end-to-end agent flow (policy Q&A and HR data retrieval) with mocked LLM responses and mocked MCP tool responses (must run offline)
- [ ] Run `pytest` from `assets/hr-information-agent/` (no args) — if coverage < 70%, add tests until threshold met
- [ ] Run `pytest` again from `assets/hr-information-agent/` (no args) to generate final `test_report.json`
- [ ] Verify `test_report.json` exists in `assets/hr-information-agent/`
