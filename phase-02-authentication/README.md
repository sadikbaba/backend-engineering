# Phase 2: Authentication

## Goal

Learn how authentication works in Django and Django REST Framework, then add a complete JWT authentication flow to the Notes API built in Phase 1.

This phase focuses on answering one question:

> Who is making this request?

Authorization rules such as roles and object-level permissions are not part of this phase.

## Project

Phase 2 extends the Notes API from Phase 1.

Current structure:

```text
phase-02-authentication/
├── README.md
└── backend/
    ├── config/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── manage.py
    ├── db.sqlite3
    └── notes/
        ├── migrations/
        │   └── 0001_initial.py
        ├── models.py
        ├── serializers.py
        ├── urls.py
        ├── views.py
        ├── admin.py
        ├── apps.py
        └── tests.py
```

The Phase 1 API code was carried forward so authentication can be added without changing the completed Phase 1 project.

## Concepts

### Authentication

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

## Django Authentication System

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

### Password Handling

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
User.objects.create_user(username="sadik", password="mypassword")
```

The password is hashed before being stored.

### authenticate()

```python
user = authenticate(username="sadik", password="mypassword")
```

`authenticate()` checks the supplied credentials using Django's configured authentication backend.

If the credentials are valid, it returns a user.

If they are invalid, it returns:

```python
None
```

### login()

`login()` starts or attaches a Django session for an authenticated user.

```python
login(request, user)
```

### logout()

`logout()` ends the current Django session.

```python
logout(request)
```

It does not delete the user account.

### request.user

After authentication, Django/DRF can expose the identified user through:

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

### is_authenticated

```python
request.user.is_authenticated
```

indicates whether Django currently recognizes the request as belonging to an authenticated user.

## Session Authentication

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
Browser usually stores it in a cookie
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
= identifier used to locate that session

Cookie
= browser storage that can carry the session ID
```

The password is not sent with every request.

## Token Authentication

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

Token authentication is not automatically JWT.

JWT is one token format that can be used for authentication.

## JWT

JWT means:

```text
JSON Web Token
```

A JWT has three major parts:

```text
header.payload.signature
```

### Header

The header contains information about the token itself, including the signing algorithm.

Example:

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

### Payload

The payload contains claims or information carried by the token.

Example:

```json
{
    "user_id": 5
}
```

A JWT payload is not automatically encrypted or hidden.

### Signature

The signature helps the server detect whether the token was modified.

Simplified idea:

```text
header + payload + secret
        ↓
signing algorithm
        ↓
signature
```

When the token is received again, the server can verify the signature.

Signing is not encryption.

```text
Signing
= helps detect modification

Encryption
= hides information
```

## Access Token

The access token is used when making authenticated API requests.

Example:

```text
GET /api/notes/

Authorization: Bearer <access_token>
```

Access tokens are normally short-lived.

## Refresh Token

The refresh token is used to obtain another access token after the current access token expires.

```text
access token expires
        ↓
client sends refresh token
        ↓
refresh token verified
        ↓
new access token issued
```

The refresh token is not normally used directly to access regular API resources.

## Token Expiration

Tokens have limited lifetimes.

```text
Access token created
        ↓
valid for a period of time
        ↓
expires
        ↓
server rejects expired token
```

When the access token expires, the client can normally use the refresh token instead of asking the user to enter their password again.

## Registration

Registration creates a new user account.

```text
username/email/password
        ↓
validate data
        ↓
create user
        ↓
hash password
        ↓
save user
```

Registration is different from login.

```text
Registration
= create an account

Login
= prove ownership of an existing account
```

## Phase 2 Practical Project

The practical goal is to add JWT authentication to the Phase 1 Notes API.

The finished flow should include:

```text
Registration
Login
Access token
Refresh token
Token expiration
Token refresh
Logout
```

The final flow should look approximately like:

```text
Register account
      ↓
Login
      ↓
Receive access + refresh tokens
      ↓
Use access token with API requests
      ↓
Access token expires
      ↓
Use refresh token
      ↓
Receive new access token
      ↓
Logout
```

## Progress

```text
[x] Authentication fundamentals
[x] Django User model basics
[x] Password hashing concept
[x] create_user()
[x] set_password()
[x] check_password()
[x] authenticate()
[x] Authentication backend
[x] login()
[x] logout()
[x] request.user
[x] is_authenticated
[x] Session authentication
[x] Cookie, session and session ID distinction
[x] Token authentication concept
[x] JWT basic structure
[x] Access token concept
[x] Refresh token concept
[x] Token expiration concept
[x] Registration concept
[x] Login concept
[x] Password handling concept

[ ] Implement registration endpoint
[ ] Implement JWT login
[ ] Generate access and refresh tokens
[ ] Authenticate API requests with access tokens
[ ] Implement refresh-token endpoint
[ ] Implement logout flow
[ ] Test valid credentials
[ ] Test invalid credentials
[ ] Test expired access token
[ ] Test token refresh
[ ] Complete Phase 2 review from memory
```

## Phase Completion Requirement

Phase 2 is complete only when the authentication project works, is tested, and the JWT flow can be explained from memory.

The final skill is:

> Implement a complete JWT authentication flow and explain the difference between access and refresh tokens.

## Not Studying Yet

The following belong to later phases:

```text
Authorization rules
Role-based permissions
Object-level permissions
Rate limiting
```