from django.contrib.auth.models import User
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CurrentUserSerializer(serializers.Serializer):
    authenticated = serializers.BooleanField(read_only=True)
    username = serializers.CharField(source="get_username")


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class RoleRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    role = serializers.ChoiceField(choices=["viewer", "editor", "admin"])


class RoleResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class RegisterResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    username = serializers.CharField()
