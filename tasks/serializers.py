from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.

    The `user` field is read-only and automatically set to the requesting user
    via the view's perform_create method.
    """

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "created_at",
            "updated_at",
            "user",
        )
        read_only_fields = ("id", "created_at", "updated_at", "user")
