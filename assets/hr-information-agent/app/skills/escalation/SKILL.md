---
name: escalation
description: |
  [WHAT] Enables the agent to gracefully escalate unresolved queries to a human HR agent.
  [WHEN] Use when the agent cannot answer confidently, the SuccessFactors API is unavailable, the query is out of scope, or the employee explicitly requests a human.
  [NOT] Do not use if the agent can answer the question confidently — try hr-policy-qa or hr-data-retrieval first.
  Key terms: speak to a human, contact HR, escalate, can't help, not sure, helpdesk.
allowed-tools: []
metadata:
  version: 1.0.0
  tags:
    - escalation
    - helpdesk
    - human-in-the-loop
  user-context-dependent: false
  requires-rbac-scope: false
---

# Escalation Skill

## Purpose

This skill handles graceful escalation when the agent cannot resolve a query. It ensures employees are never left without support and provides a clear path to a human HR agent.

## When to use

- RAG confidence score is below 0.6 and the question is policy-related
- SuccessFactors API is unavailable and the question requires personal HR data
- The employee's question is outside the agent's defined scope
- The employee explicitly asks to speak with a human
- The query involves sensitive HR matters (performance issues, disciplinary action)

## When NOT to use

- The agent can answer the question confidently — do not escalate prematurely
- A simple API retry might resolve the issue — try once more before escalating

---

## Instructions

### Step 1 — Confirm escalation is warranted

Escalate when ANY of these conditions are true:
1. RAG tool returned confidence < 0.6
2. SuccessFactors API returned an error on the second attempt
3. Employee question is out of scope (write actions, payroll, performance)
4. Employee explicitly says "speak to a human" or "contact HR helpdesk"

### Step 2 — Provide the escalation message

Use this exact format:

> "I wasn't able to fully resolve your query through self-service. Here's how to reach the HR helpdesk:
>
> 📧 **Email**: hr-helpdesk@company.com
> 🕐 **Hours**: Monday–Friday, 9:00–17:00
>
> Please include a brief description of your question when you reach out. Our HR team typically responds within 1 business day."

*Note: Replace the contact details above with your company's actual HR helpdesk contact information.*

### Step 3 — Log the escalation

The escalation must be logged as `[ESCALATED]` for ticket deflection tracking.

---

## Gotchas

- **Do not escalate prematurely** — always attempt to answer with the available tools first
- **Always provide actionable next steps** — the employee must know what to do next, not just be told "I can't help"
- **Sensitive matters always escalate** — performance, disciplinary, payroll disputes must go to a human regardless of confidence
