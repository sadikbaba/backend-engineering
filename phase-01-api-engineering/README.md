# Phase 1: API Engineering

This phase focused on understanding how a backend API works from the HTTP request all the way to the database and back to the client.

The project is a small Notes API built with Django and Django REST Framework.

## What I Built

The API supports standard CRUD operations for notes:

```text
GET    /api/notes/
POST   /api/notes/

GET    /api/notes/{id}/
PUT    /api/notes/{id}/
PATCH  /api/notes/{id}/
DELETE /api/notes/{id}/
```

The API also has OpenAPI documentation through Swagger:

```text
/api/schema/
/api/docs/
```

## Project Structure

```text
phase-01-api-engineering/
├── README.md
└── backend/
    ├── config/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── manage.py
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

## REST

REST APIs organize the backend around resources.

For this project, the resource is:

```text
Note
```

The URL identifies the resource:

```text
/api/notes/
```

HTTP methods describe what operation should happen to that resource.

```text
GET     read
POST    create
PUT     full update
PATCH   partial update
DELETE  delete
```

## Resource URLs

Collection:

```text
/api/notes/
```

This represents all notes.

Individual resource:

```text
/api/notes/1/
```

This represents one specific note.

## API Versioning

API versioning allows an API contract to change without immediately breaking clients that depend on an older version.

Example:

```text
/api/v1/notes/
/api/v2/notes/
```

A new version may be needed when a breaking change is introduced.

## Django Model

The `Note` model defines how note data is stored.

```python
class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

The model represents the database structure.

## Migrations

After creating or changing a model:

```bash
python manage.py makemigrations
python manage.py migrate
```

The flow is:

```text
Model change
    ↓
makemigrations
    ↓
Migration file
    ↓
migrate
    ↓
Database schema
```

`makemigrations` creates instructions describing the database change.

`migrate` applies those instructions to the database.

## Serializer

The serializer sits between API data and Django model objects.

For this project:

```python
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = [
            "id",
            "title",
            "content",
            "created_at",
            "updated_at",
        ]
```

The serializer has two major responsibilities.

### Incoming data

```text
Request data
    ↓
Serializer
    ↓
Validation
    ↓
Model
    ↓
Database
```

Example:

```python
serializer = NoteSerializer(data=request.data)

if serializer.is_valid():
    serializer.save()
```

`is_valid()` checks whether the incoming data follows the expected rules.

`save()` creates or updates the model only after validation succeeds.

`serializer.errors` contains validation errors when the data is invalid.

### Outgoing data

The serializer also converts Django model objects into API-friendly data.

```text
Django model
    ↓
Serializer
    ↓
Python representation
    ↓
DRF renderer
    ↓
JSON response
```

The serializer creates the representation.

The renderer produces the final JSON response.

## APIView

`APIView` allows the HTTP methods to be written manually.

Example structure:

```text
GET     get()
POST    post()
PUT     put()
PATCH   patch()
DELETE  delete()
```

This was useful for understanding what happens inside an API request.

Example POST flow:

```text
POST request
    ↓
request.data
    ↓
NoteSerializer
    ↓
is_valid()
    ↓
save()
    ↓
201 Created
```

## ViewSets

After implementing the API manually, the same resource was implemented with a DRF `ModelViewSet`.

```python
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
```

`ModelViewSet` provides standard CRUD actions:

```text
list()
create()
retrieve()
update()
partial_update()
destroy()
```

This reduces repeated CRUD code.

## Routers

A DRF router connects URLs and HTTP methods to ViewSet actions.

```python
router = DefaultRouter()
router.register("notes", NoteViewSet)
```

The router can automatically generate routes such as:

```text
GET    /api/notes/       list()
POST   /api/notes/       create()

GET    /api/notes/1/     retrieve()
PUT    /api/notes/1/     update()
PATCH  /api/notes/1/     partial_update()
DELETE /api/notes/1/     destroy()
```

This means the URLs do not need to be written manually for every CRUD operation.

## DRF Request and Response Cycle

A request moves through several layers before the client receives a response.

```text
Client
    ↓
Django URL routing
    ↓
DRF Router
    ↓
ViewSet action
    ↓
Serializer
    ↓
Model
    ↓
Database
    ↓
Serializer
    ↓
Renderer
    ↓
HTTP Response
    ↓
Client
```

For example:

```text
PATCH /api/notes/1/
```

The router maps the request to:

```text
partial_update()
```

DRF retrieves the existing note, validates the incoming fields, updates the database, serializes the updated object, and returns the response.

## PUT vs PATCH

`PUT` is used for a full update.

```text
PUT /api/notes/1/
```

The client normally provides the full resource representation.

`PATCH` is used for a partial update.

```text
PATCH /api/notes/1/
```

For example:

```json
{
    "title": "Updated title"
}
```

Only the supplied field needs to change.

## HTTP Status Codes

The main status codes practiced in this phase were:

```text
200 OK
Request succeeded.

201 Created
A new resource was created.

204 No Content
The request succeeded and there is no response body.

400 Bad Request
The client sent invalid data.

401 Unauthorized
Authentication is missing or invalid.

403 Forbidden
The client is authenticated but does not have permission.

404 Not Found
The requested resource does not exist.
```

Examples:

```text
GET /api/notes/1/
200 OK

POST /api/notes/
201 Created

PATCH /api/notes/1/
200 OK

DELETE /api/notes/1/
204 No Content
```

## OpenAPI and Swagger

OpenAPI describes the structure of an API.

Swagger provides a visual interface for viewing and testing that API description.

This project uses `drf-spectacular`.

DRF is configured with:

```python
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
```

Schema endpoint:

```text
/api/schema/
```

Swagger documentation:

```text
/api/docs/
```

Swagger makes it possible to inspect the available endpoints, request bodies, parameters, and responses without guessing the API contract.

## Phase 1 Checklist

```text
[x] REST principles
[x] Resource design
[x] API versioning
[x] Django project/app foundation
[x] Note model + database migration
[x] Serializer purpose and validation
[x] Serializer implementation
[x] DRF views
[x] DRF viewsets
[x] DRF routers
[x] Request/response cycle in DRF
[x] Correct HTTP status codes
[x] OpenAPI / Swagger
```

## What I Can Explain After This Phase

I can explain:

- how REST organizes an API around resources
- the difference between collection and individual-resource URLs
- why serializers are needed
- how validation happens before database writes
- how Django models and migrations connect to the database
- how `APIView` handles HTTP methods manually
- how `ModelViewSet` reduces repeated CRUD code
- how routers generate ViewSet routes
- the DRF request and response cycle
- the difference between `PUT` and `PATCH`
- the meaning of common HTTP status codes
- how OpenAPI and Swagger document an API