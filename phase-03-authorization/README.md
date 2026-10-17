# Phase 3: Authorization

## Goal

Control what an authenticated user is allowed to do.

Authentication answers:

```text
Who are you?
```

Authorization answers:

```text
What are you allowed to do?
```

## Concepts

We will study these in roadmap order:

1. DRF permission classes
2. Object-level permissions
3. Role-based access
4. Server-side authorization enforcement

## Practical Project

Extend the Phase 2 API with roles such as:

```text
owner
admin
viewer
```

Add permission checks so users can only perform actions they are allowed to perform, including object-level checks such as allowing users to edit only their own resources.

## Progress

- [ ] DRF permission classes
- [ ] Object-level permissions
- [ ] Role-based access
- [ ] Server-side enforcement rule
- [ ] Add roles to the API
- [ ] Add object-level checks
- [ ] Test allowed and denied requests
- [ ] Document the implementation
- [ ] Phase 3 exit check

## Completion Requirement

Phase 3 is complete when the permission model works, is tested, and can be explained from memory at both endpoint and object level.

## Not Studying Yet

```text
OWASP-level API security hardening
Rate limiting
Throttling
```

Those belong to Phase 4.

#### Permissions I have done so far

### DRF built-in permissions
1. AllowAny
2. IsAuthenticated
3. IsAuthenticatedOrReadOnly
4. IsAdminUser
5. DjangoModelPermissions
6. DjangoModelPermissionsOrAnonReadOnly
7. DjangoObjectPermissions

### Custom permissions
8. IsOwnerOrReadOnly
