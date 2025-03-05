# lectures/admin.py

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from import_export import resources, fields
from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Department
from .models import Lecture, Registration, Schedule, Term
from import_export.widgets import ManyToManyWidget


class ScheduleWidget(ManyToManyWidget):
    """
    カスタムウィジェット: "曜日-時限" の形式で指定された文字列を解析し、
    対応する Schedule オブジェクトを取得する。
    例: "月曜日-1限"
    """

    def clean(self, value, row=None, *args, **kwargs):
        if not value:
            return self.model.objects.none()
        schedules = []
        for item in value.split(self.separator):
            item = item.strip()
            if not item:
                continue
            try:
                # "曜日-時限" の形式を分割
                day_part, time_part = item.split("-", 1)
                day_part = day_part.strip()
                time_part = time_part.strip()

                # 対応する Schedule を取得
                schedule = Schedule.objects.get(day=day_part, time=time_part)
                schedules.append(schedule)
            except ValueError:
                raise ValidationError(
                    f"'{item}' は '曜日(int)-時限(int)' の形式で指定してください。"
                )
            except ObjectDoesNotExist:
                raise ValidationError(f"スケジュール '{item}' が存在しません。")

        return schedules


class LectureResource(resources.ModelResource):
    terms = fields.Field(
        column_name="terms",
        attribute="terms",
        widget=ManyToManyWidget(Term, field="number", separator=";"),
    )
    departments = fields.Field(
        column_name="departments",
        attribute="departments",
        widget=ManyToManyWidget(Department, field="name", separator=";"),
    )
    schedules = fields.Field(
        column_name="schedules",
        attribute="schedules",
        widget=ScheduleWidget(Schedule, separator=";"),
    )

    class Meta:
        model = Lecture
        fields = (
            "id",
            "syllabus_id",
            "name",
            "terms",
            "departments",
            "schedules",
            "grade",
            "room",
            "instructor",
            "units",
            "is_required",
            "is_exam",
            "description",
            "eval_method",
            "biko",
            "owner",
        )
        import_id_fields = ("id",)
        skip_unchanged = True
        report_skipped = True


@admin.register(Lecture)
class LectureAdmin(ImportExportModelAdmin):
    resource_class = LectureResource
    filter_horizontal = ("terms", "departments", "schedules")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "lecture", "registered_at")
    date_hierarchy = "registered_at"
