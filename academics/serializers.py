from rest_framework import serializers

from academics.constants import TERM_CHOICES
from accounts.models import Department
from accounts.serializers import DepartmentSerializer

from .models import Lecture, Registration, Schedule, Term


class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Term
        fields = ["number"]

    def validate_number(self, value):
        if value not in dict(TERM_CHOICES):
            raise serializers.ValidationError(
                "タームは1から4の間でなければなりません。"
            )
        return value


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ["id", "day", "time"]


class LectureSerializer(serializers.ModelSerializer):
    terms = TermSerializer(many=True, read_only=True)
    departments = DepartmentSerializer(many=True, read_only=True)
    schedules = ScheduleSerializer(many=True, read_only=True)
    term_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Term.objects.all(), write_only=True, source="terms"
    )
    department_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Department.objects.all(),
        write_only=True,
        source="departments",
    )
    schedule_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Schedule.objects.all(), write_only=True, source="schedules"
    )

    class Meta:
        model = Lecture
        fields = [
            "id",
            "syllabus_id",
            "name",
            "terms",
            "departments",
            "schedules",
            "term_ids",
            "department_ids",
            "schedule_ids",
            "grade",
            "room",
            "instructor",
            "units",
            "is_required",
            "is_exam",
            "description",
            "eval_method",
            "biko",
            "created_at",
            "updated_at",
            "owner",
        ]


class RegistrationSerializer(serializers.ModelSerializer):
    lecture = LectureSerializer(read_only=True)
    lecture_id = serializers.PrimaryKeyRelatedField(
        queryset=Lecture.objects.all(),
        write_only=True,
        source="lecture",
    )

    class Meta:
        model = Registration
        fields = ["id", "lecture", "lecture_id", "year", "registered_at"]
        read_only_fields = ["registered_at"]

    def validate(self, data):
        user = self.context["request"].user
        lecture = data.get("lecture")
        year = data.get("year")

        if not user.is_authenticated:
            raise serializers.ValidationError("認証が必要です。")

        # 取得する講義のタームとスケジュール
        new_lecture_terms = lecture.terms.all()
        new_lecture_schedules = lecture.schedules.all()

        # 同じ年に既に登録している講義のタームとスケジュールを取得
        overlapping_registrations = Registration.objects.filter(
            user=user,
            year=year,
            lecture__terms__in=new_lecture_terms,
            lecture__schedules__in=new_lecture_schedules,
        ).distinct()

        if overlapping_registrations.exists():
            # 重複している講義の詳細を取得
            overlapping_lectures = overlapping_registrations.values_list(
                "lecture__name", flat=True
            )
            overlapping_lectures_str = ", ".join(overlapping_lectures)
            raise serializers.ValidationError(
                f"登録しようとしている講義の日程が（{overlapping_lectures_str}）と重複しています。"
            )

        return data
