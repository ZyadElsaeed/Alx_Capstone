from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from .filters import TaskFilter
from .models import Task
from .permissions import IsOwner
from .serializers import TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for tasks.

    - Queryset is scoped to the authenticated user.
    - Supports filtering by status, searching by title, and ordering.
    - Uses IsOwner permission for object-level access control.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_class = TaskFilter
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["title"]
    ordering_fields = ["created_at", "due_date", "status"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Return only tasks belonging to the current user."""
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Assign the task to the current user on creation."""
        serializer.save(user=self.request.user)
