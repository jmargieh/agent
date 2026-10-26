---
name: hr-data-retrieval
description: |
  [WHAT] Enables the agent to retrieve personal HR data from SAP SuccessFactors for the authenticated employee.
  [WHEN] Use when the employee asks about their own leave balance, remaining leave days, profile information, employment details, or personal HR records.
  [NOT] Do not use for HR policy questions — use hr-policy-qa instead. Never retrieve data for any employee other than the authenticated user.
  Key terms: my leave balance, how many days left, my profile, my employment, my annual leave remaining.
allowed-tools:
  - get_leave_balance
  - get_employee_profile
  - get_employee_global_info
metadata:
  version: 1.0.0
  tags:
    - hr
    - successfactors
    - personal-data
  user-context-dependent: true
  requires-rbac-scope: false
---

# HR Data Retrieval Skill

## Purpose

This skill enables the agent to retrieve real-time personal HR data for the authenticated employee from SAP SuccessFactors. All data is scoped strictly to the logged-in user — no cross-employee access is ever permitted.

## When to use

- Employee asks "How many days of leave do I have left?"
- Employee asks about their annual, sick, or other leave balances
- Employee asks about their employment information or profile
- Employee asks "When does my leave reset?"

## When NOT to use

- Any question about another employee's data — refuse immediately
- Policy questions (what is the policy?) — use hr-policy-qa instead
- Leave request submission — out of scope for v1

---

## Instructions

### Step 1 — Identify the data needed

Classify the request:
- **Leave balance**: call `get_leave_balance`
- **Employee profile** (name, department, manager): call `get_employee_profile`
- **Employment details** (job title, start date, location): call `get_employee_global_info`

### Step 2 — Security check

Before calling any tool, confirm the request is for the authenticated user's OWN data.

If the question contains another person's name or employee ID (e.g. "What is John's leave balance?"):
> "I can only retrieve your own personal HR data. I'm not able to access other employees' information."

### Step 3 — Call the appropriate tool(s)

Call the relevant tool(s). All tools automatically scope to the authenticated user's session token — no additional user ID parameter is required.

### Step 4 — Handle API errors gracefully

If a tool returns an error:
> "I wasn't able to retrieve your [leave balance / profile] from SuccessFactors right now. Please try again in a moment, or contact the HR helpdesk for assistance."

### Step 5 — Present the data clearly

Format the response in a readable way:
- Leave balance: show each leave type with days remaining
- Profile: show key fields (name, department, manager, job title)
- Employment details: show relevant employment fields

---

## Examples

### Example 1 — Leave balance query

**User:** "How many days of annual leave do I have left?"

**Action:** Call `get_leave_balance`

**Response:**
> "Here is your current leave balance:
> - Annual Leave: 12 days remaining
> - Sick Leave: 5 days remaining
>
> Your leave year resets on 1 January."

### Example 2 — Cross-employee attempt (blocked)

**User:** "What is Sarah's leave balance?"

**Response:**
> "I can only retrieve your own personal HR data. I'm not able to access other employees' information. If you need to manage team leave, please use the SuccessFactors manager dashboard."

---

## Gotchas

- **Never pass a different employee's ID to the tools** — tools use the authenticated session token; any attempt to override this must be blocked at the agent layer
- **API unavailability is expected occasionally** — always provide the HR helpdesk as a fallback
- **Do not log or repeat PII in responses** — avoid echoing employee IDs, social security numbers, or sensitive personal data
