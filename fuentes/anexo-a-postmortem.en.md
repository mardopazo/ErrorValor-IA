# Annex A. Blameless post-mortem template

**Note for the facilitator:** start the meeting by reading the Prime Directive (section 1) out loud. The goal is to understand **how the system allowed the error to happen**, not who pressed the button.

---

## Post-mortem report: [short name of the incident]

| Field | Value |
|---|---|
| Incident date | DD/MM/YYYY |
| Investigation lead | [name] |
| Status | Under review / Completed |

## 1. Prime Directive

> "Regardless of what we discover today, we start from the premise that everyone did the best job they could with the information, tools, time and resources available at that moment."

*Adapted from the "Prime Directive" of retrospectives (Norm Kerth, 2001).*

## 2. Executive summary

A short description of what happened, what impact it had on users or on the system, and, broadly, how it was resolved.

- **What failed?**
- **Impact:** (e.g., 15% of transactions failed for 2 hours).

## 3. Timeline of events

An objective timeline. Avoid personal names: use roles or system actions.

- 14:00 – Version X is deployed to production.
- 14:05 – The alerting system detects a spike of 500 errors in the payments module.
- 14:12 – The on-call team receives the notification and starts triage.
- 14:30 – The change to the `DB_TIMEOUT` environment variable is identified as the cause of the blockage.
- 14:45 – Rollback to the previous version. System stable.

## 4. Root cause analysis (the 5 whys)

A method for getting to the systemic problem. It works as a guide, not as a rule: an incident usually has **several** causes, which are collected in section 6.

1. Why did payments fail? *Because the database didn't respond in time.*
2. Why didn't it respond in time? *Because the timeout parameter was drastically reduced.*
3. Why was it reduced? *Because the configuration was unified with the testing environment.*
4. Why was it unified without validating the impact? *Because the review of environment variables is manual and isn't documented in the pipeline.*
5. Why is it manual? *Because there is no configuration management tool that validates limits per environment.*

## 5. AI involvement in the change

*Fill in if the code involved was generated or assisted by AI. This section doesn't aim to assign blame to the tool or to the person: it aims to understand which part of the process was left without human understanding.*

- **Tool and context:** which tool was used and what context (files, requirements, constraints) did it receive?
- **Prompt or instruction:** what exactly was asked? Was information about the business rule missing?
- **What was actually reviewed:** was there a line-by-line read, tests of our own, manual testing? Who approved?
- **Understanding:** can the team today explain what that change does and which cases it doesn't cover?
- **Cases not considered:** which edge cases or exceptional situations weren't taken into account?

## 6. Contributing factors (the environment)

Which elements of the environment or of the tools made it easier for the error to happen?

- **Lack of visibility:** monitoring didn't show the connection saturation right away.
- **Outdated documentation:** the deployment manual didn't mention the dependencies of that variable.
- **Pressure from deadlines or metrics:** (fill in if applicable).

## 7. Where we got lucky and what we still don't know

- **Luck:** what could have gone worse and didn't? (e.g., the incident happened outside peak hours).
- **Unknowns:** which questions remain open? What can't we explain yet?

## 8. Action and mitigation plan

Concrete tasks, **with an owner and a date**, to make the system more robust. **No action can be "the developer should be more careful".**

| Preventive or corrective action | Owner | Priority (High / Medium / Low) | Target date | Ticket |
|---|---|---|---|---|
| Automate the validation of variables in the CI/CD pipeline | [role or name] | High | DD/MM | PROD-1234 |
| Set up specific alerts for the database connection pool | [role or name] | Medium | DD/MM | PROD-1235 |
| Update the architecture documentation of the payments module | [role or name] | Low | DD/MM | PROD-1236 |

## 9. Learning to share

One or two sentences the team can take away, written without personal names and fit to be published.

---

*A post-mortem without closed actions is an empty ritual. Review the status of the table in section 8 at the next retrospective.*
