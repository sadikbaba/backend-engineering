from rest_framework.throttling import UserRateThrottle


class NoteCreateThrottle(UserRateThrottle):
    scope = "notes_create"
