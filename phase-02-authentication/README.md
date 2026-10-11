# Phase 2: Authentication

## Goal

Learn how authentication works in Django and Django REST Framework, then implement and test multiple authentication approaches before building a complete JWT authentication flow.

This phase focuses on answering one question:

> Who is making this request?

Authorization rules such as roles and object-level permissions are not part of this phase.

---

## Project

Phase 2 extends the API work from Phase 1 and adds a separate frontend for testing authentication flows.

Current structure:

```text
phase-02-authentication/
├── README.md
├── backend/
│   ├── accounts/
│   │   ├── serializers.py
│   │   ├── session_views.py
│   │   ├── token_views.py
│   │   ├── jwt_views.py
│   │   └── urls.py
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── notes/
│   ├── manage.py
│   └── db.sqlite3
└── frontend/
    ├── src/
    │   ├── auth/
    │   │   ├── session.js
    │   │   ├── token.js
    │   │   └── jwt.js
    │   ├── main.js
    │   └── style.css
    ├── index.html
    └── package.json
```

The Phase 1 API code was carried forward so authentication could be added without changing the completed Phase 1 project.

---

# Concepts

## Authentication

Authentication means proving who a user is.

Example:

```text
username + password
        ↓
credentials checked
        ↓
user identified
```

Authentication is not the same as authorization.

Authentication asks:

```text
Who are you?
```

Authorization asks:

```text
What are you allowed to do?
```

Authorization will be studied in Phase 3.

---

# Django Authentication System

Django provides a built-in user and authentication system.

Important concepts studied:

```text
User model
password hashing
create_user()
set_password()
check_password()
authenticate()
login()
logout()
request.user
is_authenticated
authentication backends
```

## Password Handling

Passwords must never be stored as plain text.

Instead of:

```python
user.password = "mypassword"
```

Django provides safe password handling:

```python
user.set_password("mypassword")
```

or:

```python
User.objects.create_user(
    username="sadik",
    password="mypassword",
)
```

The password is hashed before being stored.

## authenticate()

```python
user = authenticate(
    username="sadik",
    password="mypassword",
)
```

`authenticate()` checks the supplied credentials using Django's configured authentication backend.

If the credentials are valid, it returns a user object.

If they are invalid, it returns:

```python
None
```

`authenticate()` checks credentials.

It does not automatically create a session or token.

## login()

```python
login(request, user)
```

`login()` starts or attaches a Django session for an authenticated user.

## logout()

```python
logout(request)
```

`logout()` ends the current Django session.

It does not delete the user account.

## request.user

After authentication, Django or DRF can expose the identified user through:

```python
request.user
```

For example:

```python
request.user.username
```

refers to the authenticated user making the request.

It is not data taken from:

```python
request.data
```

## is_authenticated

```python
request.user.is_authenticated
```

indicates whether Django currently recognizes the request as belonging to an authenticated user.

---

# Session Authentication

Session authentication keeps login state on the server.

Simplified flow:

```text
User logs in
    ↓
Server verifies credentials
    ↓
Server creates a session
    ↓
Browser receives a session identifier
    ↓
Browser stores it in a cookie
    ↓
Later requests send the cookie
    ↓
Server finds the session
    ↓
User is recognized
```

Important distinction:

```text
Session
= server-side login state

Session ID
= identifier used to locate the session

Cookie
= browser storage that can carry the session ID
```

The password is not sent with every request.

## Session Authentication Implemented

The project includes:

```text
POST /api/accounts/session/login/
POST /api/accounts/session/logout/
GET  /api/accounts/session/me/
GET  /api/accounts/session/csrf/
```

The session flow was tested through the Vite frontend.

The frontend also handles CSRF correctly when sending requests that require it.

A one-hour session expiry was tested during the learning experiment.

---

# DRF Token Authentication

Token authentication uses a token as the credential for later API requests.

Simplified flow:

```text
User logs in
    ↓
Credentials verified
    ↓
Client receives token
    ↓
Client sends token on later requests
    ↓
Server checks token
    ↓
User is identified
```

The token is sent using:

```text
Authorization: Token <token>
```

Token authentication is not automatically JWT.

JWT is a different token format and authentication approach.

## DRF Token Authentication Implemented

The project includes:

```text
POST /api/accounts/token/login/
GET  /api/accounts/token/me/
POST /api/accounts/token/logout/
```

The token frontend can:

```text
Login
Store token
Access protected endpoint
Display authenticated user
Logout
Delete token
Remove browser token
```

Reusing a deleted token was tested and correctly rejected.

---

# JWT Authentication

JWT means:

```text
JSON Web Token
```

A JWT has three major parts:

```text
header.payload.signature
```

---

## Header

The header contains information about the token itself, including the signing algorithm.

Example:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

---

## Payload

The payload contains claims or information carried by the token.

Example:

```json
{
  "user_id": 5
}
```

A normal signed JWT payload is not automatically encrypted or hidden.

---

## Signature

The signature allows the server to detect whether the JWT has been modified.

Simplified idea:

```text
header + payload + secret
        ↓
signing algorithm
        ↓
signature
```

When the token is received again, the server verifies the signature.

If the payload changes:

```text
payload changes
    ↓
expected signature changes
    ↓
original signature no longer matches
    ↓
verification fails
    ↓
token is rejected
```

---

# Signing vs Encryption

Signing and encryption are not the same thing.

```text
Signing
= protects integrity
= helps detect modification

Encryption
= hides information
= encrypted information can be decrypted with the correct key
```

Signing does not automatically hide the JWT payload.

---

# HS256

HS256 means:

```text
HMAC using SHA-256
```

In the JWT flow, HS256 is used to create and verify the token signature using a shared secret.

Simplified:

```text
header + payload + secret
        ↓
HS256
        ↓
signature
```

The same secret is used when verifying the signature.

---

# Access Token

The access token is used to access protected API endpoints.

Example:

```text
GET /api/accounts/jwt/me/

Authorization: Bearer <access_token>
```

Access tokens are short-lived.

Their purpose is:

```text
access protected resource
```

---

# Refresh Token

The refresh token has a different job.

It is used to obtain a new access token.

```text
access token expires
        ↓
client sends refresh token
        ↓
refresh token verified
        ↓
new access token issued
```

The refresh token is not used as the Bearer token for the normal protected `/jwt/me/` request.

In this project it is sent inside the request body:

```json
{
  "refresh": "<refresh_token>"
}
```

---

# Access Token vs Refresh Token

```text
Access token
= sent to protected API endpoints
= shorter lifetime

Refresh token
= used to obtain a new access token
= longer lifetime
```

For the current project:

```text
/jwt/me/
→ access token

/jwt/refresh/
→ refresh token

/jwt/logout/
→ refresh token
```

---

# JWT Registration

Registration creates a new user account.

```text
username + password
        ↓
validate data
        ↓
create_user()
        ↓
password hashed
        ↓
user saved
```

Registration is different from login.

```text
Registration
= create an account

Login
= authenticate an existing account
```

The registration endpoint returns the created username and a success message.

It does not automatically store JWT tokens in the frontend.

The user logs in afterward to obtain access and refresh tokens.

---

# JWT Login

Login verifies an existing user's credentials.

Successful login returns:

```text
access token
refresh token
```

The frontend stores them separately:

```text
jwt_access
jwt_refresh
```

For this learning project, they are stored in:

```javascript
sessionStorage
```

This is used for the learning experiment and should not automatically be treated as the best production token-storage strategy.

---

# Protected JWT Request

The protected user endpoint is:

```text
GET /api/accounts/jwt/me/
```

The frontend sends:

```text
Authorization: Bearer <access_token>
```

If the access token is valid, the backend identifies the user.

Example response:

```json
{
  "authenticated": true,
  "username": "sadiktest"
}
```

---

# Token Expiration

JWT access tokens have a limited lifetime.

```text
Access token created
        ↓
valid for a period
        ↓
expires
        ↓
protected endpoint returns 401
```

Expiration was deliberately tested using a one-minute access-token lifetime.

The expired token was correctly rejected.

After testing, the learning configuration can use a longer lifetime such as five minutes.

---

# Manual Token Refresh

The frontend contains a `refreshJWT()` function.

Its flow is:

```text
Read jwt_refresh
        ↓
POST /jwt/refresh/
        ↓
send refresh token
        ↓
receive new access token
        ↓
replace jwt_access
```

The refresh token itself remains available for future refresh operations until it expires or is blacklisted.

---

# Automatic Access-Token Refresh

The frontend also handles expired access tokens automatically.

The verified flow is:

```text
GET /jwt/me/
        ↓
401 because access token expired
        ↓
refreshJWT()
        ↓
POST /jwt/refresh/
        ↓
new access token received
        ↓
retry /jwt/me/ once
        ↓
200 success
```

Actual backend test result:

```text
GET  /api/accounts/jwt/me/       → 401
POST /api/accounts/jwt/refresh/  → 200
GET  /api/accounts/jwt/me/       → 200
```

The protected request is retried only once to avoid an infinite retry loop.

---

# JWT Logout

JWT logout works differently from Django session logout.

The frontend sends the refresh token:

```json
{
  "refresh": "<refresh_token>"
}
```

The backend creates a `RefreshToken` object and blacklists it.

Simplified flow:

```text
Logout request
        ↓
send refresh token
        ↓
backend blacklists refresh token
        ↓
refresh token can no longer issue new access tokens
        ↓
frontend removes jwt_access
        ↓
frontend removes jwt_refresh
```

The access token is not required by the current logout endpoint.

This means logout can still invalidate the refresh token even if the access token has already expired.

An already-issued access token is not automatically destroyed by blacklisting the refresh token.

It remains valid until its own expiration time.

---

# JWT Backend Endpoints

Implemented endpoints:

```text
POST /api/accounts/jwt/register/
POST /api/accounts/jwt/login/
GET  /api/accounts/jwt/me/
POST /api/accounts/jwt/refresh/
POST /api/accounts/jwt/logout/
```

---

# JWT Frontend Functions

The frontend currently contains:

```javascript
registerJWT()
loginJWT()
getJWTUser()
refreshJWT()
logoutJWT()
```

Their responsibilities are:

```text
registerJWT()
→ create user

loginJWT()
→ authenticate user
→ store access + refresh tokens

getJWTUser()
→ access protected endpoint
→ automatically refresh expired access token
→ retry once

refreshJWT()
→ exchange refresh token for new access token

logoutJWT()
→ blacklist refresh token
→ remove JWT tokens from sessionStorage
```

---

# Complete JWT Flow

The completed flow is:

```text
Register
    ↓
Login
    ↓
Receive access + refresh tokens
    ↓
Store both tokens
    ↓
Use access token for protected endpoint
    ↓
Access token expires
    ↓
Protected request returns 401
    ↓
Use refresh token
    ↓
Receive new access token
    ↓
Retry protected request once
    ↓
Authenticated request succeeds
    ↓
Logout
    ↓
Blacklist refresh token
    ↓
Remove browser tokens
```

---

# Security Notes

## Passwords

Passwords are handled through Django's authentication system.

They are stored as password hashes rather than plain-text passwords.

## JWT Payload

A signed JWT payload is readable.

Signing protects integrity.

It does not automatically provide confidentiality.

## Browser Token Storage

This learning frontend uses:

```javascript
sessionStorage
```

for JWT access and refresh tokens.

JavaScript running on the page can access `sessionStorage`, so this should not automatically be treated as the best production design.

The purpose here is to understand the JWT authentication flow clearly.

## Refresh Token Logout

Blacklisting the refresh token prevents it from being used to create future access tokens.

It does not instantly invalidate an access token that has already been issued.

---

# Progress

- [x] Authentication fundamentals
- [x] Authentication vs authorization
- [x] Django User model basics
- [x] Password hashing
- [x] `create_user()`
- [x] `set_password()`
- [x] `check_password()`
- [x] `authenticate()`
- [x] Authentication backend
- [x] `login()`
- [x] `logout()`
- [x] `request.user`
- [x] `is_authenticated`
- [x] Session authentication
- [x] Cookie, session and session-ID distinction
- [x] Session expiration
- [x] CSRF handling
- [x] DRF TokenAuthentication
- [x] Token login
- [x] Protected token request
- [x] Token logout and invalidation
- [x] JWT structure
- [x] JWT header
- [x] JWT payload
- [x] JWT signature
- [x] Signing vs encryption
- [x] JWT verification
- [x] HS256
- [x] Access token
- [x] Refresh token
- [x] Token expiration
- [x] Registration
- [x] JWT login
- [x] Protected JWT request
- [x] Refresh-token exchange
- [x] Refresh-token blacklisting
- [x] JWT logout
- [x] JWT frontend integration
- [x] Manual token refresh
- [x] Automatic access-token refresh
- [x] One-time request retry after refresh
- [x] JWT expiration and recovery testing
- [x] Final JWT signing / verification recall check

---

# Implementation Status

## Backend Implemented and Tested

- [x] Session authentication
- [x] Session expiry
- [x] CSRF endpoint
- [x] DRF TokenAuthentication
- [x] Token invalidation
- [x] JWT registration
- [x] JWT login
- [x] Protected JWT endpoint
- [x] Access-token refresh
- [x] JWT logout
- [x] Refresh-token blacklisting
- [x] Access-token expiration testing
- [x] Refresh recovery testing

## Frontend Implemented and Tested

- [x] Session authentication frontend
- [x] DRF token authentication frontend
- [x] JWT registration
- [x] JWT login
- [x] JWT authenticated-user check
- [x] Manual JWT refresh
- [x] Automatic JWT refresh
- [x] Retry after access-token expiration
- [x] JWT logout
- [x] Browser token cleanup

---

# Phase Completion Requirement

Phase 2 is complete only when the authentication project works, is tested, and the authentication flow can be explained from memory.

The final required skill is:

> Implement a complete JWT authentication flow and explain the difference between access and refresh tokens.

The implementation portion is complete and tested.

The final Phase 2 exit check is still required before the phase is marked complete.

---

# Not Studying Yet

The following belong to later phases:

```text
Authorization rules
Role-based permissions
Object-level permissions
Rate limiting
```