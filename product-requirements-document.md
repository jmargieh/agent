# Product Requirements Document (PRD)

**Title:** HR Information Agent — My Awesome Agent  
**Date:** 2026-10-22  
**Owner:** HR Product Owner  
**Solution Category:** AI Agent

---

## Product Purpose & Value Proposition

**Elevator Pitch:**  
Employees waste time hunting for HR information and filing helpdesk tickets for questions that could be answered instantly. My Awesome Agent is an AI-powered HR self-service assistant embedded in SAP SuccessFactors that answers policy questions, retrieves personal HR data, and deflects 30% of monthly helpdesk tickets — freeing the HR team to focus on complex, high-value work.

**Business Need:**  
Employees regularly need answers about company HR policies, leave and time-off rules, and benefits. Today they must either search through disconnected documents or raise a helpdesk ticket. This generates avoidable, repetitive work for the HR team. An always-available AI agent resolves this by combining a policy knowledge base with live SuccessFactors data access — all from within the SuccessFactors UI.

**Expected Value:**  
- 30% reduction in monthly HR helpdesk ticket volume within 3 months of launch
- ≥30% of HR queries resolved autonomously without escalation
- HR team capacity freed from repetitive enquiries

**Product Objectives (Prioritized):**
1. Deflect 30% of monthly HR helpdesk tickets through employee self-service
2. Provide accurate, document-grounded answers to HR policy questions
3. Give employees instant access to their own personal HR data from SuccessFactors
4. Embed the agent seamlessly in SAP SuccessFactors with no additional login required

---

## Business Metrics

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Monthly HR helpdesk ticket volume | 20 tickets/month | 14 tickets/month (−30%) | 3 months post-launch | HR Employee Self-Service | user |
| Employee self-service resolution rate | — | ≥30% of HR queries resolved without escalation | 3 months post-launch | HR Information Access | agent-derived |

---

## User Profiles & Personas

### Primary Persona: Alex — Employee

Alex is a 34-year-old project manager at a mid-sized company. He works primarily in SAP SuccessFactors to manage his time, leave, and personal HR records. When he has an HR question — about how many days of leave he has left, whether a particular public holiday is covered, or what the parental leave policy is — he either searches the company intranet (rarely finding the right document) or emails the HR helpdesk and waits for a reply. He is comfortable with technology and expects answers in seconds, not hours. His biggest frustration is that basic questions take far too long to resolve.

**Goals:**
- Get immediate, accurate answers to HR policy questions without waiting for a helpdesk reply
- Check his own leave balance and HR profile data without navigating multiple screens

**Key Tasks:**
- Ask natural-language questions about HR policies, leave rules, and benefits
- Look up his personal leave balance and profile information
- Escalate to a human HR agent when the question is too complex for the agent

---

### Secondary Persona: Maria — HR Helpdesk Agent

Maria is a 41-year-old HR generalist who handles the company's helpdesk queue. Currently more than half her weekly tickets are simple, repetitive questions about policies or leave balances — questions she answers from memory or by copy-pasting from the same documents. She wants to focus on complex cases: performance issues, sensitive personal matters, and policy exceptions. She is the escalation point when the AI agent cannot resolve a query.

**Goals:**
- Spend less time on repetitive, low-complexity HR enquiries
- Receive only escalated cases that genuinely require human judgement

**Key Tasks:**
- Review and respond to queries escalated by the agent
- Monitor agent resolution rate and quality
- Upload updated HR policy documents to keep the knowledge base current

---

### Other User Types

- **HR Administrator**: Responsible for maintaining the policy document library. Uploads new or revised PDF/Word documents to keep the agent's knowledge base accurate and current.

---

## User Goals & Tasks

### For Alex (Employee):

**Goals:**
- Resolve HR questions independently without raising a helpdesk ticket
- Access personal HR data (leave balance, profile) instantly from within SuccessFactors

**Key Tasks:**
- Type a natural-language question into the agent (e.g. "How many days of annual leave do I have left?")
- Ask policy questions (e.g. "What is the bereavement leave policy?")
- Receive a clear, sourced answer or be offered escalation to a human agent

### For Maria (HR Helpdesk Agent):

**Goals:**
- Focus on high-complexity cases
- Ensure the agent's responses are accurate and up to date

**Key Tasks:**
- Respond to escalated cases routed from the agent
- Upload updated HR policy documents (PDF/Word) to the knowledge base

---

## Product Principles

1. **Self-service first**: Every question the agent can answer confidently should never reach the helpdesk.
2. **Accuracy over completeness**: It is better to say "I don't know" and escalate than to give a confident but wrong answer.
3. **Personal data stays personal**: The agent must only ever return the authenticated employee's own data — never another employee's records.
4. **Seamless experience**: The agent is part of SuccessFactors, not a separate tool. No extra logins, no context switching.
5. **Human in the loop**: When confidence is low or the query is outside the agent's scope, it routes to a human without friction.

---

## Business Context

**Current State:**  
Employees find HR information through a fragmented mix of intranet pages, emailed documents, and helpdesk tickets. The HR helpdesk receives approximately 20 tickets per month, the majority of which are repeat questions about policies, leave balances, and benefits. There is no conversational self-service channel today.

**Strategic Alignment:**  
This initiative supports the company's HR digital transformation agenda by reducing manual workload on the HR team, improving the employee experience, and demonstrating measurable ROI from AI tooling within 3 months.

---

## Goals and Non-Goals

### Goals (In Scope)

- Answer general HR policy questions (leave rules, benefits, company policies) from ingested PDF/Word documents using RAG
- Retrieve the authenticated employee's personal HR data (leave balance, profile) from SAP SuccessFactors Employee Central APIs
- Embed the agent in the SAP SuccessFactors UI with single sign-on (no separate login)
- Escalate unresolved queries to a human HR agent
- Track helpdesk ticket volume before and after launch to measure deflection

### Non-Goals (Out of Scope)

- HR analytics and reporting (planned for a future release)
- Leave request submission or any write actions in SuccessFactors (v1 is read-only)
- Accessing or displaying another employee's HR data
- Integration with systems other than SAP SuccessFactors (v1)

---

## Requirements

### Must-Have Requirements

**R1: HR Policy Question Answering**

- **Problem to Solve**: Employees cannot quickly find answers to HR policy questions without contacting the helpdesk.
- **User Story**: As an employee, I need to ask natural-language questions about HR policies, leave rules, and benefits so that I receive an accurate answer immediately without raising a helpdesk ticket.
- **Acceptance Criteria**:
  - Given a question about a policy covered in an ingested document, when the employee asks the agent, then the agent returns an accurate, document-grounded answer within 10 seconds.
  - Given a question the agent cannot answer confidently, when the employee asks, then the agent acknowledges the limit and offers escalation.
- **Maps to Objective**: Objective 1 (ticket deflection), Objective 2 (accurate policy answers)
- **Priority Rank**: 1

---

**R2: Personal HR Data Retrieval**

- **Problem to Solve**: Employees cannot instantly check their own HR data (leave balance, profile) without navigating multiple SuccessFactors screens.
- **User Story**: As an employee, I need to ask the agent about my leave balance and personal HR profile so that I can get the information instantly without navigating multiple screens.
- **Acceptance Criteria**:
  - Given an authenticated employee asks "How many days of leave do I have left?", when the agent calls the SuccessFactors API, then the correct leave balance for that employee is returned.
  - Given an API call fails, when the agent cannot retrieve data, then the employee is informed and offered alternative support.
- **Maps to Objective**: Objective 3 (personal HR data access)
- **Priority Rank**: 2

---

**R3: SuccessFactors Embedding with Single Sign-On**

- **Problem to Solve**: Employees should not need to leave SuccessFactors or log in separately to use the agent.
- **User Story**: As an employee, I need the agent to be accessible directly from the SuccessFactors UI so that I can get HR help without switching tools or logging in again.
- **Acceptance Criteria**:
  - Given an employee is logged in to SuccessFactors, when they open the agent, then no additional authentication step is required.
  - The agent correctly identifies the authenticated user and scopes all personal data queries to that user only.
- **Maps to Objective**: Objective 4 (seamless SuccessFactors embedding)
- **Priority Rank**: 3

---

**R4: Human Escalation**

- **Problem to Solve**: Some queries are beyond the agent's capability and must reach a human HR agent without friction.
- **User Story**: As an employee, I need to be seamlessly handed off to a human HR agent when the AI cannot resolve my query so that I am never left without support.
- **Acceptance Criteria**:
  - Given the agent's confidence is below threshold or the query is out of scope, when the agent decides to escalate, then the employee is offered a clear path to reach a human HR agent.
- **Maps to Objective**: Objective 1 (ticket deflection — ensure only unresolvable queries reach the helpdesk)
- **Priority Rank**: 4

---

**R5: HR Policy Document Ingestion**

- **Problem to Solve**: The agent's knowledge base must reflect the company's current HR policies and be maintainable by HR administrators.
- **User Story**: As an HR administrator, I need to upload and update HR policy documents (PDF/Word) so that the agent's answers stay accurate and current.
- **Acceptance Criteria**:
  - Given an HR admin uploads a new or updated PDF/Word document, when the ingestion process completes, then the agent's answers reflect the updated content.
- **Maps to Objective**: Objective 2 (accurate policy answers)
- **Priority Rank**: 5

---

**R6: Personal Data Scoping & Security**

- **Problem to Solve**: The agent must never expose one employee's HR data to another employee.
- **User Story**: As the business, I need the agent to only ever return the authenticated employee's own data so that personal HR data is never exposed to unauthorised users.
- **Acceptance Criteria**:
  - The agent uses the authenticated user's session token for all SuccessFactors API calls.
  - No cross-employee data access is possible through any query path.
- **Maps to Objective**: Objective 3 (personal HR data access — security constraint)
- **Priority Rank**: 1 (security — non-negotiable)

---

### High-Want Requirements

**R7: Source Citation in Policy Answers**

- **Problem to Solve**: Employees want to trust the agent's answers and know which document they came from.
- **User Story**: As an employee, I need the agent to cite the source document for policy answers so that I can verify the information if needed.
- **Priority Rank**: 1

---

**R8: Ticket Deflection Reporting**

- **Problem to Solve**: The business needs to measure whether the agent is achieving its 30% deflection target.
- **User Story**: As an HR manager, I need a simple view of agent resolution rate vs. escalation rate so that I can track progress toward the 30% ticket reduction target.
- **Priority Rank**: 2

---

## Non-Functional Requirements

### Performance

- **Latency**: Agent responses within 10 seconds for 95% of queries
- **Throughput**: Support concurrent use by all employees during business hours

### Reliability

- **Availability**: Agent available whenever SuccessFactors is available
- **Fallback**: If the agent is unavailable, the employee is directed to the standard HR helpdesk contact

### Security

- **Data Scoping**: All SuccessFactors API calls are scoped to the authenticated user's token; no service-account-level cross-employee access
- **Data in Transit**: All API communication over HTTPS

### Explainability

- **Traceability**: Policy answers include the source document name and section where possible
- **Uncertainty Communication**: When the agent is not confident, it says so explicitly and offers escalation

---

## Solution Architecture

**Architecture Overview:**  
A Python AI agent built on the A2A protocol, deployed on SAP BTP. The agent combines a RAG-based knowledge base (for policy documents) with direct integration to SAP SuccessFactors Employee Central APIs (for personal HR data). It is exposed as a Joule-compatible endpoint and embedded in the SAP SuccessFactors UI via SSO.

**Key Components:**

- **Python AI Agent (SAP BTP)**: Core agent logic, intent classification, tool orchestration, escalation routing
- **RAG Knowledge Base**: Document ingestion pipeline and vector store for HR policy PDFs/Word documents
- **SAP SuccessFactors Employee Central API Integration**: Authenticated API calls for leave balance and employee profile data
- **Joule-compatible Endpoint**: A2A-protocol endpoint enabling embedding in the SuccessFactors UI

**Integration Points:**

- SAP SuccessFactors Employee Central (`sap.sf:apiResource:EmployeeCentralEC:v1`): read personal HR data for the authenticated employee
- SAP SuccessFactors Employee Profile (`sap.sf:apiResource:ECEmployeeProfile:v1`): read employee profile information
- HR Policy Document Store: ingestion of PDF/Word documents from an HR-managed file location

**Deployment:**

- SAP BTP (Cloud Foundry or Kyma runtime)
- Dev / QA / Prod environments with data isolation; production uses live SuccessFactors data only

---

### Agent Extensibility & Instrumentation

**Agent Extensibility:**
- The agent is designed with extension points to support future capabilities including: HR analytics queries, leave request submission, onboarding assistance, and payslip access.
- Extension points are defined at the tool layer — new SuccessFactors API integrations or knowledge sources can be added without redesigning the core agent.
- The knowledge base supports additional document types and future data product integrations.

**Business Step Instrumentation:**
- All business logic steps are instrumented with structured log statements following the pattern: `[MILESTONE_ID].[achieved|missed]: [description]`
- Logs are emitted at each milestone boundary to enable production monitoring and debugging
- See the Milestones section for the full log statement definitions

---

### Automation & Agent Behaviour

**Automation Level:** Autonomous agent with human escalation fallback

**Actions the agent performs without human approval:**
- Answering general HR policy questions from the knowledge base
- Retrieving the authenticated employee's leave balance and profile from SuccessFactors
- Routing to escalation when confidence is below threshold

**Actions that require human review or approval:**
- All queries escalated to the HR helpdesk
- Any write action in SuccessFactors (out of scope for v1)

**Model or engine used:** Large language model via SAP Generative AI Hub (GPT-4o or equivalent); RAG retrieval via vector store on SAP BTP

**Knowledge & data sources accessed:**

- HR Policy Document Store: PDF and Word documents containing company HR policies, leave rules, and benefits information. Owned and maintained by HR Administration.
- SAP SuccessFactors Employee Central: Live personal HR data (leave balance, profile) for the authenticated employee. Authoritative system of record.

**Tools or connectors invoked:**

- **SuccessFactors Employee Central API** (read-only): Retrieves leave balance and employee profile for the authenticated user
- **RAG Knowledge Base retrieval tool** (read-only): Queries the vector store to find relevant policy document excerpts for the employee's question

**Guardrails & fail-safes:**

- Agent never performs write actions on SuccessFactors in v1 (read-only)
- Personal data is strictly scoped to the authenticated employee — no cross-employee queries permitted
- When the agent's confidence in a policy answer is below threshold, it acknowledges uncertainty and offers escalation
- If the SuccessFactors API is unavailable, the agent informs the employee and directs them to the HR helpdesk
- No PII is logged in agent trace output

---

## Governance, Risk & Compliance

**Data Handling:**
- Personal HR data (leave balances, profiles) is fetched live from SuccessFactors and not persisted by the agent
- No employee PII is stored in the vector store or agent logs
- Data residency follows SAP BTP regional settings aligned with the company's SuccessFactors tenant region

**Compliance Frameworks:**
- GDPR: personal data access scoped strictly to the authenticated employee; no data stored beyond the session
- Internal HR data governance: document ingestion managed by HR Administration with a defined review cycle

**Approval Flows:**
- HR policy document updates require HR Administrator approval before ingestion

---

## Release Criteria

- **Accuracy**: Agent correctly answers ≥80% of test policy questions from ingested documents
- **Data Security**: No cross-employee data access demonstrated in security test
- **Performance**: 95th percentile response time ≤10 seconds under expected load
- **SSO**: Agent accessible from SuccessFactors UI without additional login step
- **Escalation**: All low-confidence queries successfully route to HR helpdesk
- **Monitoring**: Milestone log statements operational and visible in BTP logging tooling

---

## Schedule & Timeline Context

**Target Timeline:** 3 months to first measurable ticket deflection result

**Business Drivers:**
- HR team capacity is constrained; every month of delay is another month of avoidable repetitive ticket handling
- The 30% deflection target is the primary business case justification; it must be measurable within 3 months of launch

---

## Milestones

### M1: Agent Answers General Policy Questions

- **Description**: The agent's RAG knowledge base is populated with HR policy documents and the agent correctly responds to policy, leave, and benefits questions.
- **Achieved when**: The agent answers ≥80% of test policy questions accurately from ingested documents in a controlled test.
- **Log on achievement**: `M1.achieved: agent answers general policy questions — RAG knowledge base operational and accuracy threshold met`
- **Log on miss**: `M1.missed: agent policy Q&A not operational — knowledge base ingestion incomplete or accuracy below threshold`

### M2: Agent Retrieves Personal HR Data

- **Description**: The agent successfully calls SAP SuccessFactors Employee Central APIs to retrieve the authenticated employee's leave balance and profile.
- **Achieved when**: The agent returns correct leave balance and profile data for a test user via authenticated SuccessFactors API call.
- **Log on achievement**: `M2.achieved: personal HR data retrieval operational — SuccessFactors API integration verified for authenticated user`
- **Log on miss**: `M2.missed: personal HR data retrieval not operational — SuccessFactors API integration incomplete or authentication failure`

### M3: Agent Embedded in SAP SuccessFactors

- **Description**: The agent is accessible from within the SuccessFactors UI with no additional login step required.
- **Achieved when**: An employee logged in to SuccessFactors can open and interact with the agent without a separate authentication prompt.
- **Log on achievement**: `M3.achieved: agent embedded in SuccessFactors — SSO verified, no additional login required`
- **Log on miss**: `M3.missed: SuccessFactors embedding not complete — SSO configuration or Joule endpoint not operational`

### M4: Helpdesk Ticket Deflection Tracked

- **Description**: Baseline helpdesk ticket volume is recorded and first post-launch measurement is taken at the 1-month mark.
- **Achieved when**: 1-month post-launch ticket volume is measured and compared to the 20 tickets/month baseline.
- **Log on achievement**: `M4.achieved: helpdesk deflection tracking active — 1-month post-launch measurement recorded`
- **Log on miss**: `M4.missed: deflection tracking not in place — measurement not taken at 1-month mark`

### M5: 30% Ticket Reduction Confirmed

- **Description**: The target of ≤14 helpdesk tickets/month is achieved and confirmed at the 3-month review.
- **Achieved when**: Monthly helpdesk ticket volume at month 3 post-launch is ≤14.
- **Log on achievement**: `M5.achieved: 30% ticket reduction confirmed — monthly ticket volume at or below 14 at 3-month review`
- **Log on miss**: `M5.missed: 30% ticket reduction target not met — monthly ticket volume above 14 at 3-month review`

---

## Risks, Assumptions, and Dependencies

### Risks

- **Policy document quality**: If HR policy documents are outdated or inconsistently maintained, the agent's answers will be unreliable. Mitigation: establish a document review cadence alongside the agent launch.
- **SuccessFactors API authentication in embedded context**: Passing the authenticated employee's session token from SuccessFactors to the BTP-hosted agent requires careful OAuth/SSO configuration. This is the highest technical risk in the project.
- **RAG accuracy on edge-case queries**: Retrieval-augmented generation may not handle ambiguous or multi-topic questions well. Mitigation: define clear escalation behaviour for low-confidence responses.

### Assumptions

- HR policy documents are available in PDF or Word format and can be provided to the ingestion pipeline.
- The company's SAP SuccessFactors tenant supports the Employee Central API endpoints identified in the fit-gap analysis.
- SAP BTP is available as the deployment platform with the required runtime and AI services.
- The HR team will assign an administrator responsible for maintaining the document library.

### Dependencies

- SAP SuccessFactors Employee Central API access (`sap.sf:apiResource:EmployeeCentralEC:v1`)
- SAP SuccessFactors Employee Profile API access (`sap.sf:apiResource:ECEmployeeProfile:v1`)
- SAP Generative AI Hub access on SAP BTP for the LLM and embedding model
- HR Administration team to provide initial policy document set and maintain it post-launch

---

## Open Questions

- What is the preferred escalation channel for the HR helpdesk — email, a ticketing system, or a chat queue?
- Is there an existing document management system where HR policy documents are stored, or will documents be uploaded directly to the agent?
- Which SAP BTP runtime is preferred for deployment — Cloud Foundry or Kyma?

---

## Appendix

### Glossary

- **RAG (Retrieval-Augmented Generation)**: A technique where the AI agent searches a knowledge base of documents to find relevant excerpts before generating an answer, grounding responses in source material rather than relying solely on the model's training data.
- **A2A Protocol**: Agent-to-Agent protocol — the standard used to build and expose AI agents in a way that is compatible with SAP Joule and the SuccessFactors embedding.
- **SSO (Single Sign-On)**: Authentication mechanism that allows users to access the agent using their existing SuccessFactors login without a separate credential prompt.
- **Employee Central**: The core HR module in SAP SuccessFactors that stores personal HR records including leave balances and employee profiles.

### References

- SAP SuccessFactors Employee Central API: `sap.sf:apiResource:EmployeeCentralEC:v1`
- SAP SuccessFactors Employee Profile API: `sap.sf:apiResource:ECEmployeeProfile:v1`
- SAP BTP — AI Agent Development (A2A Protocol)
- SAP Generative AI Hub
