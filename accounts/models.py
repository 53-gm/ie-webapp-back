from django.contrib.auth.models import (
    AbstractUser,
)
from django.db import models
import shortuuid


class Faculty(models.Model):
    name = models.CharField(max_length=30)  # 学部名

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=30)  # 学科名
    faculty = models.ForeignKey(
        Faculty, related_name="departments", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"


def generate_short_uuid():
    return shortuuid.ShortUUID().random(length=16)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    user_id = models.CharField(unique=True, max_length=16, default=generate_short_uuid)
    display_name = models.CharField(max_length=16, blank=True)  # 表示名
    faculty = models.ForeignKey(
        Faculty, on_delete=models.SET_NULL, null=True, blank=True
    )
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True
    )
    GRADE_CHOICES = [
        (1, "1年"),
        (2, "2年"),
        (3, "3年"),
        (4, "4年"),
    ]
    grade = models.PositiveSmallIntegerField(
        choices=GRADE_CHOICES, null=True, blank=True
    )  # 学年

    is_profile_complete = models.BooleanField(default=False)
    picture_url = models.URLField(blank=True, null=True)
