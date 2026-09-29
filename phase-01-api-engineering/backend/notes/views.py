from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Note
from .serializers import NoteSerializer


# Manual APIView version.
#
# This class shows the request/response process explicitly:
#
# Client request
#     ↓
# APIView method
#     ↓
# Query database or read request.data
#     ↓
# Serializer
#     ↓
# Validation / save
#     ↓
# Response
#
# We keep this version for learning purposes because it shows
# what DRF's ModelViewSet later handles for us automatically.
class NoteListView(APIView):

    # GET requests retrieve all notes from the database.
    # many=True tells the serializer that we are serializing
    # multiple Note objects instead of one object.
    def get(self, request):
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    # POST requests create a new Note.
    #
    # request.data contains the incoming parsed request body.
    # The serializer validates the incoming data before anything
    # is saved to the database.
    def post(self, request):
        serializer = NoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # PUT performs a full update of an existing Note.
    #
    # First we retrieve the existing object.
    # Then the serializer receives both:
    # - the existing Note
    # - the new request data
    def put(self, request, pk):
        note = Note.objects.get(pk=pk)

        serializer = NoteSerializer(
            note,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # PATCH performs a partial update.
    #
    # partial=True means the client can send only the field
    # that needs to change instead of sending every required field.
    def patch(self, request, pk):
        note = Note.objects.get(pk=pk)

        serializer = NoteSerializer(
            note,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    # DELETE removes the Note from the database.
    #
    # 204 No Content means the operation succeeded
    # and there is no response body to return.
    def delete(self, request, pk):
        note = Note.objects.get(pk=pk)
        note.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


# ModelViewSet is the shorter DRF version of the CRUD API above.
#
# Instead of manually writing get(), post(), put(), patch(),
# and delete(), ModelViewSet provides standard CRUD actions:
#
# list()
# create()
# retrieve()
# update()
# partial_update()
# destroy()
#
# The router maps HTTP methods and URLs to these actions.
class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer