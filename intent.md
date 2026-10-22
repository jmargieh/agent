# HR Information Agent

My Awesome Agent — AI-powered assistant for employee HR self-service

## Business challenge

Employees struggle to find HR information on their own — covering company policies, leave and time-off rules, and benefits. This results in avoidable helpdesk tickets, with the HR team spending time on repetitive enquiries. An AI agent embedded in SAP SuccessFactors should answer both general policy questions and personal HR data queries, reducing the monthly helpdesk ticket volume by 30% within 3 months of launch.

## Business Goals & Success Criteria

| Metric | Baseline | Target | Timeline | Process / Capability | Source |
|--------|----------|--------|----------|----------------------|--------|
| Monthly HR helpdesk ticket volume | 20 tickets/month | 14 tickets/month (−30%) | 3 months post-launch | HR Employee Self-Service | user |
| Employee self-service resolution rate | — | ≥30% of HR queries resolved without escalation | 3 months post-launch | HR Information Access | agent-derived |

## Key Milestones

1. **Agent answers general policy questions** — agent correctly responds to questions about HR policies, leave rules, and benefits from ingested PDF/Word documents.
2. **Agent retrieves personal HR data** — agent looks up the logged-in employee's leave balance and personal profile via SAP SuccessFactors APIs.
3. **Agent embedded in SAP SuccessFactors** — agent is accessible from within the SuccessFactors UI without any additional login step.
4. **Helpdesk ticket deflection tracked** — baseline ticket volume measured and first reduction reported at the 1-month mark post-launch.
5. **30% ticket reduction confirmed** — target achieved and confirmed at the 3-month review.

## Business Architecture (RBA)

### End-to-End Process

Recruit to Retire

### Process Hierarchy

```
Recruit to Retire
└── Manage Workforce (generic)
    └── Manage Employee Information and Reporting (BPS-385)
        └── Manage HR reports
        └── Employee self-service information access
        └── HR policy Q&A
```

### Summary

The business challenge maps to the Recruit to Retire E2E, specifically the Manage Workforce phase. The agent addresses the "Manage Employee Information and Reporting" sub-process by giving employees direct, conversational access to HR data and policy knowledge without involving the HR helpdesk.

## Fit Gap Analysis

| Requirement (business) | Standard asset(s) found | API ORD ID | MCP Server ORD ID | MCP Server Version | Webhook API ORD ID | Data Product ORD ID | Gap? | Notes / assumptions |
|------------------------|-------------------------|------------|-------------------|--------------------|--------------------|---------------------|------|---------------------|
| Look up personal HR data (leave balance, profile, benefits) | SAP SuccessFactors Employee Central | `sap.sf:apiResource:EmployeeCentralEC:v1` | — | — | — | — | No | Available API; no MCP server found — custom integration required |
| Retrieve employee profile information | SAP SuccessFactors Employee Profile | `sap.sf:apiResource:ECEmployeeProfile:v1` | — | — | — | — | No | Available API; no MCP server found — custom integration required |
| Answer general HR policy questions (policies, leave, benefits) | — | — | — | — | — | — | Yes | No standard SAP asset; requires document ingestion + RAG-based knowledge base |
| HR analytics / reporting | SAP SuccessFactors HCM Core, SAP Analytics Cloud | — | — | — | — | — | Maybe | Out of scope for v1; can be extended later |

### Key findings

- SAP SuccessFactors Employee Central is the authoritative system for personal HR data; APIs are available but require custom MCP-style integration.
- No ready-made MCP servers were found for SuccessFactors APIs — the agent will call these APIs directly via authenticated HTTP.
- HR policy documents (PDF/Word) are a key knowledge source with no structured system behind them; a retrieval-augmented generation (RAG) knowledge base must be built.
- The knowledge base is the primary gap and the most impactful component for ticket deflection.
- The agent will be embedded in SAP SuccessFactors, requiring an A2A-compatible deployment on SAP BTP.
- Personal data access must be scoped to the authenticated employee only — no cross-employee data access.

## Recommendations

### HR Information AI Agent

#### Executive Summary

Python AI agent embedded in SuccessFactors for HR self-service Q&A

#### Recommended Solution

Build a pro-code Python agent following the A2A protocol, deployed on SAP BTP. The agent combines two capabilities: (1) a RAG-based knowledge base ingesting HR policy documents (PDF/Word) to answer general policy, leave, and benefits questions; (2) direct integration with SAP SuccessFactors Employee Central APIs to retrieve personal HR data for the authenticated employee. The agent is exposed as a Joule-compatible endpoint and embedded in SAP SuccessFactors.

#### Problem Statement

Employees cannot easily locate HR information independently, leading to repetitive helpdesk tickets that consume HR team capacity. The primary topics are company HR policies, leave & time-off rules, and benefits questions.

#### Affected User Roles

- All employees (primary users of the agent)
- HR helpdesk team (beneficiaries of reduced ticket volume)
- HR administrators (owners of policy documents)

#### Important factors

##### Reduces repetitive HR helpdesk workload through automation

By deflecting common questions to a self-service agent, the HR team can focus on complex, high-value cases rather than answering the same policy questions repeatedly.

##### Dual knowledge mode — structured data + unstructured documents

The agent must handle both live SuccessFactors API data (personal records) and static document knowledge (policies), requiring a combined retrieval approach.

#### Potential risks

##### Policy document quality and freshness

If HR policy documents are outdated or inconsistently maintained, the agent's answers will be unreliable. An HR document governance process should be established alongside the agent.

##### SuccessFactors API authentication in embedded context

Passing the authenticated employee's session token from SuccessFactors to the agent requires careful OAuth/SSO configuration on SAP BTP.

#### Recommended solution category

AI Agent

#### Intent fit

90%
