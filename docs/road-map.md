# Universal Backend Engineering Roadmap

A production-capable Python/Django backend curriculum. Not built around VTU or any single app. VTU is one optional capstone at the end, not the foundation.

---

## Baseline Audit

**Already solid, review only:** core Django, core Python, basic Django ORM.

**New, core focus:** DRF, API design, JWT auth, permissions, API security, PostgreSQL at depth, transactions, concurrency, idempotency, external API integration, webhooks, Redis, Celery, testing, logging/monitoring, secrets management, caching, deployment, Docker, architecture.

**Prerequisite chains:**
- Auth requires API Engineering.
- Authorization requires Auth.
- Concurrency and Reliability require Databases.
- Webhooks require External APIs.
- Background Jobs benefit from Caching (Redis) being understood first.
- Deployment and Docker require Configuration/Secrets.
- Architecture is best learned after you have felt the pain of a messy codebase, so it sits mid-late, not first.

**Independent, can be learned in any order once prerequisites are met:** Testing, Observability, Caching.

**Advanced, delayed on purpose:** Performance tuning, multi-service architecture, advanced Celery patterns.

**Domain-specific, kept out of the core:** payment-system concepts, provider/API architecture (VTU-style), reconciliation. These appear only in the final Domain Applications phase.

---

## Phase 1: API Engineering

**Goal:** Build correct, well-designed REST APIs with Django REST Framework instead of ad hoc views.

**Concepts:**
- REST principles, resource design, versioning
- DRF serializers, views, viewsets, routers
- Request/response cycle in DRF
- Status codes used correctly
- API documentation (OpenAPI/Swagger via drf-spectacular or similar)

**Prerequisites:** Core Django, core Python.

**Practical project:** A REST API for a simple resource (e.g. a notes or tasks API) with full CRUD, proper status codes, and generated API docs.

**Skills gained:** Can design and document a clean REST API from scratch.

**What NOT to study yet:** JWT, permissions, Redis, Celery, deployment.

---

## Phase 2: Authentication

**Goal:** Implement real authentication, not just Django's default session login.

**Concepts:**
- Django auth system internals
- Token vs session auth
- JWT structure, access and refresh tokens, expiration
- Login, logout, registration, password handling

**Prerequisites:** Phase 1.

**Practical project:** Add JWT authentication to the Phase 1 API, with registration, login, logout, and refresh token flow.

**Skills gained:** Can implement a full JWT auth flow and explain access vs refresh tokens.

**What NOT to study yet:** Authorization rules, rate limiting.

---

## Phase 3: Authorization

**Goal:** Control who can do what, beyond "logged in or not."

**Concepts:**
- DRF permission classes
- Object-level permissions
- Role-based access
- The rule that authorization must always be enforced server-side, never trusted from the client

**Prerequisites:** Phase 2.

**Practical project:** Add roles (e.g. owner, admin, viewer) to the Phase 2 API, with object-level checks so users can only edit their own resources.

**Skills gained:** Can design and enforce a permission model at both endpoint and object level.

**What NOT to study yet:** OWASP-level security hardening, rate limiting.

---

## Phase 4: API Security

**Goal:** Harden the API against real attack classes, using OWASP as the reference.

**Concepts:**
- OWASP API Security Top 10, applied to your own API
- Rate limiting and throttling
- Input validation and output sanitization
- Secure headers, HTTPS enforcement
- Basic security testing of your own endpoints

**Prerequisites:** Phase 3.

**Practical project:** Run a security pass on the Phase 3 API: add throttling, fix at least one deliberately introduced vulnerability (e.g. broken object-level auth), and document the fix.

**Skills gained:** Can audit an API against a known checklist and explain each fix.

**What NOT to study yet:** Payment-specific security, production secrets management (comes in Phase 11).

---

## Phase 5: Databases

**Goal:** Go beyond basic ORM use into real relational database engineering.

**Concepts:**
- PostgreSQL fundamentals for backend engineers
- Advanced Django ORM: select_related, prefetch_related, annotations, query optimization
- Indexes and query plans at a conceptual level
- Transactions, atomicity, isolation levels

**Prerequisites:** Phase 1.

**Practical project:** Refactor the API's data layer for correctness and speed: fix N+1 queries, wrap a multi-step write in a transaction, add indexes where they matter.

**Skills gained:** Can read a slow query and fix it, and can reason about transaction boundaries.

**What NOT to study yet:** Concurrency/locking, that is the next phase.

---

## Phase 6: Concurrency

**Goal:** Handle simultaneous requests correctly.

**Concepts:**
- Race conditions, with a concrete example (two requests decrementing stock at once)
- Database locking: select_for_update, optimistic vs pessimistic locking
- Why "it worked in testing" does not mean it is safe under load

**Prerequisites:** Phase 5.

**Practical project:** Build an endpoint that is deliberately vulnerable to a race condition (e.g. limited-stock purchase), reproduce the bug under concurrent requests, then fix it with proper locking.

**Skills gained:** Can identify and fix a race condition, and can explain locking tradeoffs.

**What NOT to study yet:** Idempotency, next phase.

---

## Phase 7: Reliability

**Goal:** Make operations safe to retry and consistent even when things fail halfway.

**Concepts:**
- Idempotency keys and idempotent endpoint design
- Retry-safe operations
- Data consistency patterns for financial or state-changing operations
- Failure handling: partial failure, compensating actions

**Prerequisites:** Phase 6.

**Practical project:** Make a "create order" or "process payment" endpoint idempotent using an idempotency key, and prove it by sending the same request twice and confirming only one effect occurs.

**Skills gained:** Can design an idempotent endpoint and explain why it matters for money or state-changing actions.

**What NOT to study yet:** Full payment provider integration, that is domain-specific.

---

## Phase 8: External APIs and Webhooks

**Goal:** Integrate with third-party services reliably in both directions.

**Concepts:**
- Calling external APIs: timeouts, retries, error handling
- API keys and secrets for outbound calls
- Webhooks: receiving, verifying signatures, handling out-of-order or duplicate events
- Idempotency applied to webhook processing (ties back to Phase 7)

**Prerequisites:** Phase 7.

**Practical project:** Integrate one real external API (e.g. a public weather or payments sandbox API) and build a webhook receiver that verifies signatures and handles duplicate delivery safely.

**Skills gained:** Can integrate an external API defensively and build a secure webhook handler.

**What NOT to study yet:** Provider-specific architecture like VTU, that is domain-specific.

---

## Phase 9: Caching and Background Jobs

**Goal:** Offload slow or repeated work using Redis and Celery.

**Concepts:**
- Redis as a cache: what to cache, cache invalidation
- Caching strategy (cache-aside, TTLs)
- Celery: workers, queues, tasks
- When background jobs are the right tool versus a synchronous request

**Prerequisites:** Phase 5, 8.

**Practical project:** Cache an expensive query with Redis, then move a slow operation (e.g. sending an email or processing a webhook) into a Celery background task.

**Skills gained:** Can decide what to cache and when to defer work to a background job.

**What NOT to study yet:** Advanced Celery patterns (chains, chords, scheduled beat jobs) unless a real need appears.

---

## Phase 10: Testing

**Goal:** Test backend behavior that actually matters: correctness under normal and adversarial conditions.

**Concepts:**
- Unit tests for business logic
- Integration tests for API endpoints
- Testing authentication and permission checks
- Testing concurrency and idempotency (simulate duplicate/parallel requests)
- Mocking external API calls

**Prerequisites:** Phases 1 to 9 (there is now real logic worth testing).

**Practical project:** Write a test suite covering the auth flow, one permission rule, the idempotent endpoint from Phase 7, and the webhook handler from Phase 8, with external calls mocked.

**Skills gained:** Can write tests that catch real regressions, not just happy-path checks.

**What NOT to study yet:** Chasing 100% coverage as a goal.

---

## Phase 11: Observability, Configuration and Secrets

**Goal:** Know what is happening in the system and keep sensitive data out of the codebase.

**Concepts:**
- Structured logging
- Monitoring and error tracking concepts
- Environment variables and settings management
- Secrets management: what never goes in Git, what belongs in environment config
- File and data storage: local vs object storage, when each is appropriate

**Prerequisites:** Phase 1 to 10.

**Practical project:** Add structured logging and basic error tracking to the project, move all secrets to environment variables, and add file upload with storage handled correctly (not hardcoded local paths in production config).

**Skills gained:** Can debug a production issue from logs alone, and can explain why a secret should never be committed.

**What NOT to study yet:** Full production deployment, next phase.

---

## Phase 12: Architecture and Code Organization

**Goal:** Structure a Django project so it stays maintainable as it grows.

**Concepts:**
- App boundaries in Django (what belongs in its own app)
- Separating business logic from views (services/selectors pattern)
- Serializer and permission organization at scale
- Git and backend engineering practices: branching, commit discipline, code review basics

**Prerequisites:** Phase 1 to 11 (you now have enough real code to reorganize meaningfully).

**Practical project:** Refactor the accumulated project into clear app boundaries with business logic pulled out of views into service functions, and clean up commit history going forward.

**Skills gained:** Can justify a Django app boundary and explain why logic does not belong in a view.

**What NOT to study yet:** Multi-service or microservice architecture, that is advanced and situational.

---

## Phase 13: Deployment and Docker

**Goal:** Ship the backend to production correctly and repeatably.

**Concepts:**
- Docker basics: images, containers, Dockerfile for a Django app
- docker-compose for local multi-service setup (app, Postgres, Redis)
- Production deployment: Gunicorn, Nginx, environment separation
- CI basics: run tests before deploy

**Prerequisites:** Phase 11, 12.

**Practical project:** Dockerize the full project (Django, Postgres, Redis, Celery worker) with docker-compose, then deploy it to a real server with a basic CI check that runs tests before deploy.

**Skills gained:** Can containerize and deploy a real Django backend end to end.

**What NOT to study yet:** Kubernetes or orchestration beyond docker-compose, unless a real need appears.

---

## Phase 14: Domain Applications (Optional Capstone Layer)

**Goal:** Apply the universal backend skills to a specific domain. This is where VTU or payments becomes the outcome, not the foundation.

**Concepts (domain-specific, only introduced here):**
- Payment-system concepts: settlement, reconciliation, ledger thinking
- Provider/API architecture (e.g. VTU providers): abstracting multiple providers behind one interface, failover between providers
- Practical security testing specific to payment-like flows

**Prerequisites:** All prior phases.

**Practical project:** Build the VTU application (or a payments-style app) as a capstone: real provider integration behind an abstraction layer, idempotent transaction processing, webhook handling for provider callbacks, full test suite, dockerized deployment.

**Skills gained:** Everything above, applied to one coherent production system.

---

## Final Roadmap Requirements

### Learning Timeline
- Phases 1 to 4 (API, auth, authorization, security): foundation layer
- Phases 5 to 7 (databases, concurrency, reliability): the core engineering weight
- Phases 8 to 9 (external APIs, webhooks, caching, jobs): integration layer
- Phases 10 to 12 (testing, observability, architecture): production-readiness layer
- Phase 13 (deployment, Docker): shipping layer
- Phase 14: domain capstone

### Portfolio Checklist
- [ ] Phase 1 to 4 API with JWT auth, roles, and a documented OWASP-style security pass
- [ ] Phase 5 to 7 API with optimized queries, transactions, and a fixed race condition
- [ ] Phase 8 external API integration plus a signed webhook receiver
- [ ] Phase 9 Redis caching plus a Celery background job
- [ ] Phase 10 test suite covering auth, permissions, idempotency, and webhooks
- [ ] Phase 11 logging, error tracking, and secrets properly externalized
- [ ] Phase 13 dockerized, deployed project with CI running tests
- [ ] Phase 14 domain capstone (VTU or similar)

### GitHub Project Checklist (per repo)
- [ ] README with problem statement, architecture summary, and why each tool was chosen
- [ ] Setup instructions that work from a fresh clone
- [ ] .gitignore correctly excluding secrets and build artifacts
- [ ] Meaningful commit history
- [ ] Passing tests, ideally with a CI badge
- [ ] API docs (OpenAPI/Swagger link or screenshot)

### Interview Preparation Checklist
- [ ] Can explain JWT access vs refresh tokens
- [ ] Can explain a real race condition you fixed and how locking solved it
- [ ] Can explain idempotency and why it matters for money-moving endpoints
- [ ] Can explain how you would design and verify a webhook receiver
- [ ] Can explain when to use caching vs a background job
- [ ] Can explain a Django app boundary decision you made
- [ ] Can walk through your Docker/deployment setup end to end

### Common Interview Questions
- How do you prevent a race condition when two users buy the last item in stock at the same time?
- What is an idempotency key and where would you use one?
- How do you verify a webhook actually came from the provider it claims to be from?
- Walk through the difference between select_related and prefetch_related.
- How would you design rate limiting for a public API?
- What secrets should never be committed to Git, and where should they live instead?
- Describe your Docker setup for a Django project with Postgres, Redis, and Celery.
- How do you decide what to cache and for how long?

### Free Learning Resources
- Django docs (docs.djangoproject.com)
- Django REST Framework docs (django-rest-framework.org)
- PostgreSQL official docs (postgresql.org/docs)
- OWASP API Security Top 10 (owasp.org)
- Redis docs (redis.io/docs)
- Celery docs (docs.celeryq.dev)
- Docker docs (docs.docker.com)

### Books (optional deep dives)
- Two Scoops of Django (Daniel and Audrey Feldroy), for Django architecture patterns
- Designing Data-Intensive Applications (Martin Kleppmann), for concurrency and consistency depth
- Web Application Security (Andrew Hoffman), for the security phase

### Practice Websites
- Postman or Insomnia for manual API testing and security probing
- SQLBolt or PGExercises for practicing PostgreSQL queries
- OWASP Juice Shop, for hands-on security testing practice (against a deliberately vulnerable app, not your own production API)

### Advanced Topics for After This Roadmap
- Multi-service and microservice architecture
- Advanced Celery patterns: chains, chords, scheduled beat tasks
- Database read replicas and sharding
- Event-driven architecture with message queues beyond Celery
- Advanced observability: distributed tracing

---

## Non-Negotiables

- Never skip the practical project for a phase.
- Never move to the next phase until the current project works, is tested, and you can rebuild its core piece from memory.
- Keep domain-specific work (payments, VTU, provider architecture) out of the core phases. It belongs only in Phase 14.