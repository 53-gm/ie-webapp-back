import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    lecture_id = django_filters.CharFilter(field_name="lecture", lookup_expr="exact")

    class Meta:
        model = Task
        fields = ["lecture_id"]
