from rest_framework import serializers
from django.contrib.auth import get_user_model

from users.models import Stats

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "bio", "avatar")
        extra_kwargs = {
            "email": {"required": False},
            "bio": {"required": False},
            "avatar": {"required": False},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
            bio=validated_data.get("bio", ""),
            avatar=validated_data.get("avatar", None),
        )
        return user


class StatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stats
        fields = ('total_sessions', 'streak_days', 'avg_duration', 'total_minutes')


class UserSerializer(serializers.ModelSerializer):

    stats = StatsSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "email", "bio", "avatar", "stats")
