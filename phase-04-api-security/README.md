# Phase 4 - API Security

**Status:** Started - 2026-10-19  
**Prerequisite:** Phase 3 Authorization complete  
**Project base:** The Phase 3 Notes/JWT/RBAC API  
**Roadmap position:** Final phase of the foundation layer before Databases

## Goal

Harden the existing API against real attack classes using the OWASP API Security Top 10 as the main reference.

By the end of this phase, the API should not only work correctly. It should also be able to resist common misuse, reject unsafe requests, limit abusive traffic, expose only intended data, and document the security decisions made.

## Roadmap Scope

Phase 4 covers exactly these core areas:

1. OWASP API Security Top 10, applied to the existing API
2. Rate limiting and throttling
3. Input validation and output sanitization/control
4. Secure headers and HTTPS enforcement
5. Basic security testing of our own endpoints

## Skills to Gain

By the end of Phase 4, I should be able to:

- audit an API against a known security checklist
- explain the difference between authentication, authorization, throttling, validation, and transport security
- identify where an OWASP API risk applies to my own API
- add and verify DRF throttling
- reject malformed or unsafe input correctly
- control what fields the API accepts and returns
- inspect and reason about security-related HTTP headers
- explain why HTTPS matters and how Django supports HTTPS enforcement
- perform basic manual security tests against my own API
- deliberately reproduce one controlled vulnerability locally, fix it, and prove the fix works
- document a security finding as: problem → risk → reproduction → fix → verification

## Teaching Method for This Phase

This phase must be taught with a security-first, concept-first workflow.

### 1. Retrieve before teaching

Before a new lesson, quickly recall only the Phase 1–3 knowledge that the new security concept depends on.

Examples:
- before BOLA: recall object-level permissions
- before broken authentication: recall JWT validation
- before broken function-level authorization: recall admin role checks

Do not re-teach old material unless recall exposes a real gap.

### 2. Official-source gate

Before every genuinely new security concept, provide:

1. the current official primary-source link
2. one short exact quote
3. a simple-English explanation
4. one tiny example using the current API

Primary sources should be OWASP, Django, and Django REST Framework documentation.

### 3. Threat → weakness → consequence → control

Every security idea should be taught in this order:

- What is the attacker trying to do?
- What weakness makes it possible?
- What can go wrong?
- What control prevents or reduces it?

Do not begin with configuration syntax before the security problem is understood.

### 4. Safe local lab

All attack-style experiments must be performed only against my own local development API or an intentionally vulnerable training app.

For each lab:

1. predict what should happen
2. send the request with curl/Postman
3. read status code, response body, and relevant headers
4. explain why the result happened
5. change one security control
6. run the same request again
7. compare before vs after

### 5. Progressive help

If I get stuck:

- attempt 1 → small hint
- attempt 2 → stronger hint
- attempt 3 → solution with explanation

Do not give a full solution immediately unless I ask for it.

### 6. Evidence before completion

A topic is not complete just because the code exists.

It must have at least one of:

- a successful security check
- a denied malicious/invalid request
- a before/after comparison
- a curl/Postman result
- a Django security-check result
- a clear explanation from memory

### 7. Document each finding

For every meaningful security issue, record:

- issue
- risk
- affected endpoint
- reproduction
- expected secure behavior
- fix
- verification result

## Safety Rules for Security Labs

- Test only systems I own or have explicit permission to test.
- Use local development endpoints for deliberate vulnerabilities.
- Never leave a deliberately vulnerable version as the final committed state.
- Never push real access tokens, passwords, API keys, or production secrets.
- Use dummy users and disposable tokens for experiments.
- A vulnerability is introduced only to understand and prove the fix.
- Fix and re-test the vulnerability before the final Git milestone.
- Do not treat DRF throttling as full DDoS or brute-force protection.

## Course Outline

## Module 0 - Phase 4 Security Baseline

**Purpose:** Know what is already protected before changing anything.

### Topics

- map current endpoints
- identify authentication and authorization controls already present
- inspect current response headers
- record current security assumptions
- establish a baseline OWASP audit table

### Current API areas to inspect

- JWT registration/login/refresh/logout
- protected `/me/` endpoint
- Notes CRUD
- viewer/editor/admin authorization
- object ownership checks
- role assign/remove endpoints

### Deliverable

A short baseline document showing what already exists and what Phase 4 still needs to harden.

---

## Module 1 - OWASP API Security Top 10

**Goal:** Understand the ten major API risk categories and map each one to the current API.

### OWASP API Security Top 10 - 2023

1. API1 - Broken Object Level Authorization (BOLA)
2. API2 - Broken Authentication
3. API3 - Broken Object Property Level Authorization
4. API4 - Unrestricted Resource Consumption
5. API5 - Broken Function Level Authorization
6. API6 - Unrestricted Access to Sensitive Business Flows
7. API7 - Server Side Request Forgery (SSRF)
8. API8 - Security Misconfiguration
9. API9 - Improper Inventory Management
10. API10 - Unsafe Consumption of APIs

### How each risk will be studied

For every risk:

1. simple meaning
2. attacker goal
3. vulnerable example
4. whether it applies to the current API
5. existing protection, if any
6. missing protection, if any
7. one practical check where relevant
8. audit-table entry

### Initial mapping to our API

| OWASP risk | Current API connection |
| --- | --- |
| API1 BOLA | Notes object ownership and `IsOwnerOrAdmin` |
| API2 Broken Authentication | JWT login, access/refresh tokens, protected endpoints |
| API3 Broken Object Property Level Authorization | Serializer field exposure, writable fields, owner control |
| API4 Unrestricted Resource Consumption | Request throttling/rate limits |
| API5 Broken Function Level Authorization | Admin-only role-management endpoints |
| API6 Sensitive Business Flows | Repeated abuse of sensitive actions such as role changes or authentication flows |
| API7 SSRF | Likely not directly applicable yet because this API does not currently accept URLs for server-side fetching; record as not applicable unless a relevant endpoint exists |
| API8 Security Misconfiguration | Django security settings, headers, DEBUG/deployment checks, HTTPS configuration |
| API9 Improper Inventory Management | Endpoint inventory, stale/forgotten routes, API documentation/version awareness |
| API10 Unsafe Consumption of APIs | Awareness now; deeper practical relevance arrives when external APIs are introduced later |

**Rule:** Do not invent a feature just to force every OWASP category into the current API. Mark a risk as not applicable or future-relevant when appropriate.

### Module checkpoint

I can explain all ten risks at a practical developer level and map each one to the current API as applicable, protected, missing, not applicable, or future-relevant.

---

## Module 2 - Rate Limiting and Throttling

**Goal:** Control how frequently clients can call the API and understand the limits of application-level throttling.

### Topics

- rate limiting vs DRF throttling terminology
- why unlimited requests are dangerous
- authenticated-user vs anonymous-client limits
- `AnonRateThrottle`
- `UserRateThrottle`
- scoped/per-endpoint throttling where appropriate
- throttle rates
- HTTP `429 Too Many Requests`
- `Retry-After`
- why DRF throttling is basic over-use protection, not complete DDoS/brute-force defense

### Practical lab

- add a deliberately low local throttle rate
- send repeated requests with curl
- observe successful requests first
- trigger `429`
- inspect the response
- explain which client identity is being throttled
- restore a sensible documented configuration after the experiment

### Evidence

- throttle configuration
- repeated curl requests
- captured `429` response
- explanation of what throttling can and cannot protect against

---

## Module 3 - Input Validation and Output Control

**Goal:** Never trust client-controlled data and expose only fields the client should see.

### Topics

- trusted vs untrusted data
- serializer validation
- field-level validation
- object-level validation
- type, length, range, and allowed-value checks
- required fields
- unexpected/malicious values
- server-controlled fields such as ownership
- controlling response fields
- avoiding sensitive-data exposure
- difference between API data validation and HTML-context escaping/sanitization

### Practical checks

Use curl to try inputs such as:

- missing required values
- invalid role names
- excessive string lengths
- unexpected values
- attempts to control server-owned fields
- malformed JSON

For each request, predict and verify the correct response, usually `400 Bad Request` when validation fails.

### Evidence

- at least one validation improvement
- one invalid request rejected correctly
- one check proving a server-controlled/sensitive field cannot be improperly changed or exposed

---

## Module 4 - Secure Headers and HTTPS Enforcement

**Goal:** Understand transport security and the security protections Django can add to HTTP responses.

### Topics

- why HTTP traffic needs HTTPS protection
- TLS/HTTPS mental model at developer level
- Django `SecurityMiddleware`
- existing response security headers
- `X-Content-Type-Options`
- `X-Frame-Options`
- Referrer Policy
- Cross-Origin-Opener-Policy
- HSTS concept
- `SECURE_SSL_REDIRECT`
- production vs local-development security settings
- `manage.py check --deploy`

### Important rule

Do not blindly force production HTTPS/HSTS behavior into local development. Learn the setting, understand where it belongs, and verify it safely.

### Practical lab

- inspect current headers with `curl -i`
- identify which protections already exist
- trace them to Django middleware/settings
- run Django deployment security checks
- interpret relevant warnings
- document which HTTPS/security settings belong in production

### Evidence

- current header audit
- explanation of at least three relevant headers/settings
- deployment security-check output interpreted correctly
- written HTTPS enforcement plan

---

## Module 5 - Basic Security Testing

**Goal:** Learn a repeatable developer security-testing loop against my own API.

### Security testing loop

1. identify expected security rule
2. create a negative/adversarial request
3. predict the secure result
4. send the request
5. inspect status/body/headers
6. determine whether the control worked
7. fix the problem if it failed
8. repeat the same request
9. document evidence

### Practical security cases

- unauthenticated access attempt
- expired/invalid JWT
- viewer attempting editor/admin action
- editor attempting another user's object modification
- non-admin attempting role management
- invalid role/input values
- repeated requests until throttled
- output-field exposure checks
- selected security-header checks

**Testing scope:** Phase 4 uses targeted manual security testing and Django security checks. The full automated backend test suite remains a later Testing phase.

---

## Required Practical Project - Phase 3 API Security Pass

Run a documented security pass on the Phase 3 API.

### Required work

- complete an OWASP-style audit of the current API
- add DRF throttling and prove it works
- improve or verify input validation
- verify output/data exposure controls
- inspect secure headers
- document HTTPS enforcement requirements
- deliberately introduce at least one controlled vulnerability locally
- reproduce the vulnerability
- fix it
- prove the fix with the same request
- document the complete before/after result

### Deliberate vulnerability choice

Preferred vulnerability for this phase:

**Broken Object Level Authorization (BOLA)**

Reason: the Phase 3 Notes API already has object ownership rules, so it gives a clear before/after security experiment without inventing a new domain.

The vulnerable state must remain local and temporary. The final committed state must contain the fix.

## OWASP Audit Table Template

| Risk | Applies? | Current protection | Finding | Action | Evidence |
| --- | --- | --- | --- | --- | --- |
| API1 BOLA |  |  |  |  |  |
| API2 Broken Authentication |  |  |  |  |  |
| API3 Broken Object Property Level Authorization |  |  |  |  |  |
| API4 Unrestricted Resource Consumption |  |  |  |  |  |
| API5 Broken Function Level Authorization |  |  |  |  |  |
| API6 Sensitive Business Flows |  |  |  |  |  |
| API7 SSRF |  |  |  |  |  |
| API8 Security Misconfiguration |  |  |  |  |  |
| API9 Improper Inventory Management |  |  |  |  |  |
| API10 Unsafe Consumption of APIs |  |  |  |  |  |

## Security Finding Template

### Finding

**Name:**  
**Affected endpoint:**  
**OWASP category:**  
**Risk:**  
**Expected secure behavior:**  
**Observed vulnerable behavior:**  
**Reproduction request:**  
**Root cause:**  
**Fix:**  
**Verification request:**  
**Result after fix:**  

## Progress Checklist

### Baseline

- [ ] Current endpoint inventory recorded
- [ ] Current authentication/authorization protections mapped
- [ ] Current response headers inspected

### OWASP

- [ ] API1 BOLA
- [ ] API2 Broken Authentication
- [ ] API3 Broken Object Property Level Authorization
- [ ] API4 Unrestricted Resource Consumption
- [ ] API5 Broken Function Level Authorization
- [ ] API6 Unrestricted Access to Sensitive Business Flows
- [ ] API7 SSRF
- [ ] API8 Security Misconfiguration
- [ ] API9 Improper Inventory Management
- [ ] API10 Unsafe Consumption of APIs
- [ ] OWASP audit table completed

### Throttling

- [ ] Throttling mental model understood
- [ ] DRF throttle configuration added
- [ ] `429 Too Many Requests` reproduced locally
- [ ] Throttling limitations explained from memory

### Validation / Output

- [ ] Input-validation rules reviewed
- [ ] At least one validation improvement made or verified
- [ ] Invalid request rejected correctly
- [ ] Server-controlled fields protected
- [ ] Output field exposure reviewed

### Headers / HTTPS

- [ ] Existing security headers inspected
- [ ] SecurityMiddleware behavior understood
- [ ] HTTPS enforcement concept understood
- [ ] HSTS concept understood
- [ ] Django deployment security checks run and interpreted

### Security Testing Project

- [ ] Deliberate local vulnerability introduced safely
- [ ] Vulnerability reproduced
- [ ] Root cause explained
- [ ] Vulnerability fixed
- [ ] Same attack re-tested and blocked
- [ ] Finding documented
- [ ] Final security pass documented

### Exit

- [ ] Can explain each Phase 4 concept without notes
- [ ] Can explain one real vulnerability and fix end to end
- [ ] Can explain why throttling is useful but incomplete protection
- [ ] Can explain input validation vs authorization
- [ ] Can explain why HTTPS and security headers matter
- [ ] Can audit an endpoint using the security-testing loop
- [ ] Git status clean
- [ ] Meaningful commit created
- [ ] Changes pushed

## Phase 4 Exit Check

Before Phase 4 is complete, I must be able to answer from memory:

1. What is the OWASP API Security Top 10 and why do backend developers use it?
2. What is BOLA and how did our Notes API prevent/fix it?
3. What is the difference between authentication, authorization, throttling, and validation?
4. Why can rate limiting reduce abuse but not be treated as complete DDoS protection?
5. Where should input validation happen in DRF?
6. Why must server-controlled fields not be trusted from client input?
7. What security information can HTTP response headers provide?
8. Why is HTTPS required even when JWT authentication is correct?
9. What did `check --deploy` reveal and what does it not prove?
10. Walk through one vulnerability from reproduction → root cause → fix → verification.

## Completion Requirement

Phase 4 is complete only when:

- the five roadmap areas are understood
- the OWASP audit is documented
- throttling is implemented and manually verified
- validation/output controls are checked
- headers/HTTPS are understood and audited
- the deliberate vulnerability is reproduced and fixed safely
- the final API is in a secure state
- the exit recall check is passed
- the final changes are committed and pushed

After this phase, the Phase 1–4 foundation layer should exist as one API with CRUD, JWT authentication, roles/permissions, and a documented OWASP-style security pass.

## What We Are NOT Studying Yet

Do not expand Phase 4 into later roadmap phases.

- payment-specific security
- VTU/provider-specific security
- production secrets management
- external API/webhook security implementation
- full automated backend test-suite design
- Redis/Celery
- database concurrency/locking
- Docker/deployment implementation

These belong to later phases in the roadmap.

## Primary Reference Sources

Use the current official documentation during lessons:

- OWASP API Security Top 10
- Django REST Framework - Throttling
- Django REST Framework - Serializers / Validation
- Django - Security documentation
- Django - SecurityMiddleware documentation
- Django - system checks / deployment security checks

## Session Log Template

**Date:**  
**Topic:**  
**Official source used:**  
**Concept explained:**  
**Threat / weakness / consequence / control:**  
**Practical request or experiment:**  
**Prediction:**  
**Observed result:**  
**What I explained from memory:**  
**Gap found:**  
**Fix / next step:**  
**Evidence saved:**  
**Git milestone:**  
