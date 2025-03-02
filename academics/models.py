import uuid
from django.db import models
from django.forms import ValidationError
from django.contrib.auth.models import User

from academics.constants import DAY_CHOICES, TERM_CHOICES, TIME_CHOICES
from accounts.models import Department


class Term(models.Model):
    number = models.PositiveSmallIntegerField(
        choices=TERM_CHOICES, verbose_name="ターム", primary_key=True
    )

    class Meta:
        verbose_name = "ターム"
        verbose_name_plural = "学期"

    def __str__(self):
        return f"第{self.number}ターム"

    def clean(self):
        if self.number not in dict(TERM_CHOICES):
            raise ValidationError(
                {"number": "タームは1から4の間でなければなりません。"}
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Schedule(models.Model):
    day = models.PositiveSmallIntegerField(choices=DAY_CHOICES, verbose_name="曜日")
    time = models.PositiveSmallIntegerField(choices=TIME_CHOICES, verbose_name="時限")

    class Meta:
        unique_together = ("day", "time")
        verbose_name = "スケジュール"
        verbose_name_plural = "スケジュール"

    def __str__(self):
        return f"{dict(DAY_CHOICES).get(self.day)} {dict(TIME_CHOICES).get(self.time)}"


class Lecture(models.Model):
    id = models.CharField(
        max_length=36,
        primary_key=True,
        default=uuid.uuid4,
        verbose_name="講義コード",
    )
    syllabus_id = models.CharField(
        max_length=30, blank=True, null=True, verbose_name="シラバスコード"
    )
    name = models.CharField(max_length=200, verbose_name="講義名")
    departments = models.ManyToManyField(
        Department, related_name="lectures", verbose_name="履修可能学科"
    )
    terms = models.ManyToManyField(Term, related_name="lectures", verbose_name="ターム")
    grade = models.IntegerField(verbose_name="対象学年", default=1)
    schedules = models.ManyToManyField(
        Schedule, related_name="lectures", verbose_name="スケジュール"
    )

    # 詳細情報
    room = models.CharField(max_length=50, blank=True, verbose_name="講義室")
    instructor = models.CharField(max_length=200, verbose_name="担当教員")
    units = models.FloatField(verbose_name="単位数", default=0)
    is_required = models.BooleanField(verbose_name="必修", default=False)
    is_exam = models.BooleanField(verbose_name="期末テスト", default=False)
    description = models.CharField(max_length=5000, blank=True, verbose_name="概要")
    eval_method = models.CharField(max_length=1000, blank=True, verbose_name="評価方法")
    biko = models.CharField(max_length=300, blank=True, verbose_name="備考")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")
    owner = models.ForeignKey(
        User,
        related_name="lectures",
        on_delete=models.CASCADE,
        verbose_name="所有者",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = "講義"

    def __str__(self):
        return f"{self.id} - {self.name}"


class Registration(models.Model):
    user = models.ForeignKey(
        User,
        related_name="registrations",
        on_delete=models.CASCADE,
        verbose_name="ユーザー",
    )
    lecture = models.ForeignKey(
        Lecture,
        related_name="registrations",
        on_delete=models.CASCADE,
        verbose_name="講義",
    )
    year = models.PositiveIntegerField(verbose_name="年度")
    registered_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")

    class Meta:
        unique_together = ("user", "lecture", "year")
        verbose_name_plural = "登録状況"

    def __str__(self):
        return f"{self.user.profile.display_name} が {self.lecture.name} を {self.year}年  に登録"
