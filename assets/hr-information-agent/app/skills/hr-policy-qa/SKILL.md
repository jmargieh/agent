---
name: hr-policy-qa
description: |
  [WHAT] Enables the agent to answer HR policy questions using the RAG knowledge base.
  [WHEN] Use when the user asks about HR policies, leave rules, benefits, company guidelines, bereavement leave, parental leave, or any policy-related question.
  [NOT] Do not use for personal HR data like leave balance or employee profile — use hr-data-retrieval instead.
  Key terms: policy, leave rules, benefits, guidelines, bereavement, parental, annual leave policy, HR document.
allowed-tools:
  - rag_query
metadata:
  version: 1.0.0
  tags:
    - hr
    - policy
    - rag
  user-context-dependent: false
  requires-rbac-scope: false
---

# HR Policy Q&A Skill

## Purpose

This skill enables the agent to answer general HR policy questions by querying the RAG knowledge base, which contains ingested HR policy documents (PDF/Word). It ensures answers are grounded in source documents and that uncertainty is communicated clearly.

## When to use

- Employee asks about leave policies (annual, sick, parental, bereavement)
- Employee asks about benefits, health coverage, or company perks
- Employee asks about HR rules, procedures, or company guidelines
- Employee asks "What does the policy say about X?"

## When NOT to use

- Employee asks about their own personal leave balance — use hr-data-retrieval skill
- Employee asks about their own profile or employment details — use hr-data-retrieval skill
- Query is about submitting a leave request (out of scope for v1)

---

## Instructions

### Step 1 — Understand the question

Read the employee's question carefully and identify the HR topic. Classify it as one of:
- Leave policy (annual, sick, parental, bereavement, public holidays)
- Benefits (health, pension, perks)
- Company rules/procedures
- Other HR policy

### Step 2 — Query the knowledge base

Call the `rag_query` tool with the employee's question as the query. The tool returns:
- `answer`: the extracted answer from the most relevant document excerpts
- `sources`: list of source documents with document name and section
- `confidence`: retrieval confidence score (0.0–1.0)

### Step 3 — Evaluate confidence and respond

| Confidence | Action |
|---|---|
| ≥ 0.6 | Return the answer with source citations |
| < 0.6 | Acknowledge uncertainty; offer escalation |
| No results | State that the information was not found; offer escalation |

**Always include source citations** in the format:
> *Source: [Document Name], [Section/Page]*

### Step 4 — Offer escalation if needed

If confidence is below threshold or the question is outside available documents:
> "I wasn't able to find a confident answer to your question in the HR policy documents. I'd recommend reaching out to the HR helpdesk for assistance."

---

## Examples

### Example 1 — Annual leave policy question

**User:** "How many days of annual leave are employees entitled to?"

**Action:** Call `rag_query` with query "annual leave entitlement days"

**Response (with source):**
> "According to the Annual Leave Policy, full-time employees are entitled to 25 days of annual leave per year.
>
> *Source: Annual Leave Policy, Section 2.1 – Leave Entitlement*"

### Example 2 — Low confidence / not in documents

**User:** "What is the policy on sabbatical leave?"

**Action:** Call `rag_query` — low confidence result

**Response:**
> "I wasn't able to find information about sabbatical leave in the available HR policy documents. I'd recommend contacting the HR helpdesk who can provide accurate guidance on this topic."

---

## Gotchas

- **Never fabricate policy details** — if the document doesn't contain the answer, say so explicitly rather than guessing
- **Always cite sources** — employees need to verify information; source citations build trust
- **Confidence threshold is 0.6** — below this, escalate rather than risk giving wrong information
