import django_filters
from .models import Lecture, Registration, Schedule


class LectureFilter(django_filters.FilterSet):

    schedules = django_filters.ModelMultipleChoiceFilter(
        field_name="schedules__id",
        queryset=Schedule.objects.all(),
        label="スケジュール",
    )
    day = django_filters.NumberFilter(
        field_name="schedules__day", lookup_expr="exact", label="曜日"
    )
    time = django_filters.NumberFilter(
        field_name="schedules__time", lookup_expr="exact", label="時限"
    )

    class Meta:
        model = Lecture
        fields = ["schedules", "day", "time"]


class RegistrationFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name="year", lookup_expr="exact")
    number = django_filters.NumberFilter(method="filter_by_term")

    class Meta:
        model = Registration
        fields = ["year", "number"]

    def filter_by_term(self, queryset, name, value):
        """
        Registration の関連先 Lecture の terms の中で、
        number が指定された値に一致するものだけフィルタします。
        """
        return queryset.filter(lecture__terms__number=value).distinct()
