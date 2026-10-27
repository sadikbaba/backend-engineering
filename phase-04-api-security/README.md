# Phase 4: API Security

**Status:** Final review, Git milestone pending  
**Started:** 19 October 2026  
**Latest practical:** 27 October 2026  
**Base project:** Django REST Framework Notes API with JWT and role-based permissions

## Goal

Make the existing API harder to misuse. Use the OWASP API Security Top 10 to check real risks, test the protections, and explain why each one matters.

## Work completed

- Studied the OWASP API Security Top 10 and mapped the risks to the Notes API.
- Added user throttling and a tighter limit for note creation. Repeated requests produced `429 Too Many Requests`.
- Validated note titles and restricted client control of sensitive fields. Note ownership is set from `request.user` on creation.
- Inspected security response headers, HTTPS and HSTS behavior, and Django deployment warnings.
- Removed legacy session and token login routes. The Notes API uses JWT authentication.
- Cleaned up duplicate middleware and corrected OpenAPI request and response schemas. Registration is documented as `201 Created`; role changes return a `RoleResponse` schema.
- Passed the Phase 4 knowledge exit quiz: **7.5/10 (75%)**, above the **70%** pass mark.

## OWASP API Security Top 10 audit

| Risk | Finding for this project | Follow-up |
| --- | --- | --- |
| API1: Broken Object Level Authorization | Reproduced BOLA locally and restored `IsOwnerOrAdmin`. Cross-owner PATCH returned `403` after the fix. | Final Git diff review |
| API2: Broken Authentication | JWT login works; invalid credentials returned `401`. | Review login abuse protection before deployment |
| API3: Broken Object Property Level Authorization | `owner` is assigned on the server; serializer output fields reviewed. | Retest unwanted client fields when features change |
| API4: Unrestricted Resource Consumption | User and note-creation throttles tested with `429`. | Throttling alone is not DDoS protection |
| API5: Broken Function Level Authorization | Role-management endpoints use JWT and `IsAppAdmin`. Non-admin denial was tested in Phase 3. | Retest after role changes |
| API6: Sensitive Business Flows | Registration, login, and role changes are sensitive actions. | Review endpoint-specific abuse controls later |
| API7: Server-Side Request Forgery | No current endpoint fetches client-supplied URLs. | Reassess if URL-fetching is added |
| API8: Security Misconfiguration | Response headers inspected; `check --deploy` identified production settings still needed. | Configure and verify HTTPS settings on deployment |
| API9: Improper Inventory Management | Old login routes removed; current endpoints appear in OpenAPI. | Keep API inventory current |
| API10: Unsafe Consumption of APIs | No external provider integration in this phase. | Revisit in the external API phase |

## Practical finding: BOLA

**Endpoint:** `PATCH /api/notes/4/`  
**Setup:** `musa` had the `editor` role; Note 4 belonged to `sadiktest`.

**Problem and risk:** Temporarily removing `IsOwnerOrAdmin` left authentication and model-level permission checks, but no ownership check. An editor could edit somebody else's note.

**Reproduction:** Musa's PATCH changed Note 4's title to `BOLA local experiment` and returned **`200 OK`**.

**Fix:** Restored `IsOwnerOrAdmin` to `NoteViewSet.permission_classes`.

**Verification:** The same PATCH returned **`403 Forbidden`**, with `You do not have permission to perform this action.` A later source check confirmed that `IsOwnerOrAdmin` was present and Note 4 still belonged to `sadiktest`.

**Lesson:** Model permission answers whether a user can edit notes in general. Object permission checks whether they can edit *this* note. The deliberately vulnerable version must never be committed.

## Deployment notes

Local development uses HTTP, so production-only HTTPS settings were not blindly enabled. Before deployment, review `DEBUG`, `ALLOWED_HOSTS`, HTTPS redirect, HSTS, secure session and CSRF cookies, and the development-only email backend. Re-run `check --deploy` for the real deployment environment. A passing system check does not test application authorization rules.

## Final checklist

- [x] OWASP risks mapped to the current API
- [x] Throttling tested with `429`
- [x] Validation and output controls reviewed
- [x] Security headers and deployment warnings inspected
- [x] BOLA introduced locally, reproduced, fixed, and re-tested
- [x] Exit quiz passed at 75%
- [ ] Restore Note 4's original title, `Learning DRF validation`, if not already done
- [ ] Confirm `python manage.py check` output
- [ ] Confirm `git diff --check` and inspect final Git diff
- [ ] Commit and push only the secure final version

## Study rules and next phase

Use official OWASP, Django, and DRF documentation for new topics. Explain the threat before the fix, test only local or authorized systems, and use evidence before declaring a control effective. Do not commit passwords, JWTs, secrets, or a deliberately vulnerable version.

Once final Git verification is complete, continue to **Phase 5: Databases**. Payment security, production secrets management, external APIs, and full automated testing belong to later phases.

**References:** [OWASP API Security Top 10](https://owasp.org/API-Security/) · [DRF permissions](https://www.django-rest-framework.org/api-guide/permissions/) · [DRF throttling](https://www.django-rest-framework.org/api-guide/throttling/) · [Django deployment checklist](https://docs.djangoproject.com/en/6.1/howto/deployment/checklist/)
