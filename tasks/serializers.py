from rest_framework import serializers

from academics.models import Lecture
from academics.serializers import LectureSerializer
from .models import Task


class TaskSerializer(serializers.ModelSerializer):

    lecture = LectureSerializer(read_only=True)
    lecture_id = serializers.PrimaryKeyRelatedField(
        queryset=Lecture.objects.all(),
        write_only=True,
        source="lecture",
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "lecture",
            "lecture_id",
            "title",
            "description",
            "status",
            "due_date",
            "priority",
            "created_at",
            "updated_at",
        ]
