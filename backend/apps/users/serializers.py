from rest_framework import serializers
from .models import User, EmployeeProfile


class EmployeeProfileSerializer(serializers.ModelSerializer):
    """Serializer for employee profile data."""

    class Meta:
        model = EmployeeProfile
        fields = (
            "full_name",
            "email",
            "phone",
            "position",
            "salary",
            "join_date",
            "created_at",
        )
        read_only_fields = ("created_at",)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user with profile data."""

    profile = EmployeeProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "date_joined", "profile")
        read_only_fields = ("id", "date_joined")


class LoginSerializer(serializers.Serializer):
    """Serializer for login credentials."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})


class TokenResponseSerializer(serializers.Serializer):
    """Serializer for token response."""

    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()
