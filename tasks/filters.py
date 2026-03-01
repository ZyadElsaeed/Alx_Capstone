import django_filters

from .models import Task


class TaskFilter(django_filters.FilterSet):
    """Allows filtering tasks by status and due_date range."""

    due_date_from = django_filters.DateFilter(field_name="due_date", lookup_expr="gte")
    due_date_to = django_filters.DateFilter(field_name="due_date", lookup_expr="lte")

    class Meta:
        model = Task
        fields = ["status"]
