from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note

        fields = ["id", "title", "content", "created_at", "updated_at"]  # noqa: RUF012

    def validate_title(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(
                "Title must be less than 100 characters"
            )

        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters")

        return value
