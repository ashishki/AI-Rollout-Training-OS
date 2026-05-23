# AI Rollout Public Source Register

Version: 1.0
Last updated: 2026-05-23
Corpus version: public-demo-corpus-v1
Status: public demo source register

This register supports the Phase 15 solo/small-team showcase. Sources are
public pages or PDFs only. Extracted facts are short notes for role-pack and
demo-corpus design, not copied policy text. Public sources do not prove
enterprise adoption, productivity lift, compliance readiness, paid conversion,
or GA readiness.

## Source Register

| source_url_or_locator | captured_at | source_type | role_or_policy_use | extracted_fact | demo_use | limitation |
|---|---|---|---|---|---|---|
| https://openai.com/policies/usage-policies/ | 2026-05-23 | AI usage policy | Forbidden use and human review boundaries | OpenAI disallows licensed professional advice without appropriate professional involvement and high-stakes automation without human review. | Create guardrail quiz cases for regulated advice and human review routing. | Vendor policy for OpenAI services; not a customer internal policy. |
| https://www.nist.gov/itl/ai-risk-management-framework | 2026-05-23 | AI governance framework | Risk management structure | NIST AI RMF frames AI risk management around trustworthiness considerations across design, development, use, and evaluation. | Ground source-register fields for risk, evidence, and limitations. | Voluntary framework; not a compliance attestation. |
| https://learn.microsoft.com/en-us/legal/ai-code-of-conduct | 2026-05-23 | AI service code of conduct | Human oversight and content rights | Microsoft requires testing, appropriate human oversight, feedback channels, notices/consents, and security controls for AI service use. | Build reviewer checklist for AI-assisted lead-response output. | Service-specific conduct rules; not a general internal SOP. |
| https://aws.amazon.com/ai/responsible-ai/policy/ | 2026-05-23 | AI service policy | Consequential decision safeguards | AWS requires risk evaluation, human oversight, testing, and safeguards for consequential decisions. | Define forbidden autonomous decision examples for the role pack. | Applies to AWS AI/ML services; demo must not infer broader legal duties. |
| https://developers.google.com/machine-learning/guides/intro-responsible-ai | 2026-05-23 | Responsible AI guidance | Responsible AI dimensions | Google lists responsible AI dimensions including fairness, accountability, safety, and privacy. | Provide high-level rubric categories for safe AI use. | Training guidance; not an enforceable company policy. |
| https://doit.illinois.gov/content/dam/soi/en/web/doit/documents/support/policies/2021/20250401-DoIT-AI%20Policy-v2-%20A11Y.pdf | 2026-05-23 | Public-sector AI policy | Data protection and oversight | Illinois policy requires clear AI disclosure, human oversight roles, vetted data sources, and documented authorization for protected data use. | Model source limitations and protected-data handling in demo policy. | Public-sector policy; not directly transferable to private support teams. |
| https://www.testlio.com/ai-use-policy | 2026-05-23 | Company AI acceptable-use policy | Confidentiality and output review | Testlio's policy emphasizes protecting client confidential information, trade secrets, IP, bias awareness, and output accuracy. | Create allowed/forbidden examples around customer and client data. | One company example; not universal best practice. |
| https://www.ingenuiti.com/ai-usage-policy/ | 2026-05-23 | Company AI usage policy | First-draft and approved-tool rules | Ingenuiti treats AI output as preliminary, requires responsible employee review before external use, and routes new tools through approval. | Train learner to present AI drafts as draft-only until reviewed. | Public webpage summary; internal approved-tool list is not public. |
| https://www.approachmarketing.com/ai-usage-policy | 2026-05-23 | Company AI usage policy | Sensitive data and client delivery | Approach Marketing forbids sensitive client data in unapproved tools and autonomous publishing or client delivery without human review. | Add lead-response examples that require review before external sending. | Agency policy; role-pack must label it as example evidence. |
| https://www.avaya.com/en/trust-center/artificial-intelligence/ | 2026-05-23 | AI trust-center policy summary | AI tool registration and quality checking | Avaya describes AI use policy, tool registration, quality checking for factual errors, and privacy review for personal-data processing. | Add operator mission requiring tool/source check before reuse. | Trust-center summary, not full internal procedure. |
| https://workforce-central.org/policy/ai-usage/ | 2026-05-23 | Public AI usage policy | Public trust and accountability | WorkForce Central frames GenAI use around ethical, transparent, and accountable implementation. | Support concise policy language for public-demo guardrails. | High-level policy page with limited operational detail. |
| https://handbook.gitlab.com/handbook/support/workflows/ | 2026-05-23 | Support workflow index | Support workflow navigation | GitLab publishes support workflow categories, including AI workflow and ticket-closing workflows. | Identify support SOP areas to cite in lead-response role-pack design. | Index page; individual workflows require separate review. |
| https://handbook.gitlab.com/handbook/support/workflows/ticket_lifecycle/ | 2026-05-23 | Support SOP | Ticket lifecycle | GitLab describes ticket lifecycle as shared language from customer contact to closing the loop. | Create mission steps for acknowledging, tracking, and closing customer requests. | GitLab-specific workflow, not a generic SLA policy. |
| https://handbook.gitlab.com/handbook/support/workflows/customer_calls/ | 2026-05-23 | Support SOP | Customer call follow-up | GitLab customer-call workflow covers scheduling, preparation, follow-up, and post-call summary practices. | Add handoff mission for summarizing human calls and next steps. | Call workflow, not an inbound lead qualification SOP. |
| https://handbook.gitlab.com/handbook/customer-success/csm/support/ | 2026-05-23 | Customer success/support SOP | Support contact setup and ticket quality | GitLab CSM guidance covers establishing support users, SLA-guided tickets, and customer education on ticket best practices. | Add reviewer checklist for sufficient context before support escalation. | Customer-success context; adapt only as public workflow evidence. |
| https://www.salesforce.com/blog/sales/lead-qualification/ | 2026-05-23 | Lead qualification guidance | Lead fit and sales handoff | Salesforce describes lead qualification as judging fit based on factors such as fit, finances, interest, and need, with MQL/SQL handoff concepts. | Build lead-response qualification mission and handoff rubric. | Vendor blog guidance; not proof of conversion lift. |
| https://www.hubspot.com/improve-lead-quality-conversion | 2026-05-23 | Lead-management workflow guidance | Qualification tracking and handoff | HubSpot describes segmenting by qualification criteria, routing to sales, tracking qualified leads, and avoiding handoff gaps. | Add workflow mission for capturing qualification notes before routing. | Product marketing page with vendor claims; use workflow facts only. |
| https://blog.hubspot.com/sales/ultimate-guide-to-sales-qualification | 2026-05-23 | Sales qualification framework | BANT qualification | HubSpot summarizes BANT as Budget, Authority, Need, and Timeline, and notes limitations around stakeholders and timing. | Create qualification questions and limitations for synthetic lead responses. | Sales framework article; not a required standard. |

## Assumption Register

| assumption | demo_use | limitation |
|---|---|---|
| The showcase learner is a synthetic lead-response operator, not a real employee. | Allows end-to-end replay without private HR or customer data. | Does not prove adoption or training effectiveness. |
| Example leads and submissions are synthetic and must avoid real customer, employee, lead, or prospect data. | Keeps the mini-cohort safe for public artifacts. | Synthetic data cannot support productivity or conversion claims. |
| Public policies can shape guardrail examples but cannot replace a customer's approved internal policy. | Provides bootstrap evidence for T64. | Real deployment needs customer-approved policy/SOP snapshots. |

## Demo Use Rules

- Use extracted facts as short role-pack evidence only.
- Do not copy large source text into fixtures or reports.
- Do not use any public source to claim compliance, enterprise readiness,
  adoption, productivity lift, paid conversion, or GA readiness.
- If sources conflict or are too thin for a feedback claim, route to
  `insufficient_evidence` or human review.
