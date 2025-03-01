from django.contrib.auth.models import (
    AbstractUser,
)
from django.db import models
import shortuuid

from academics.models import Department, Faculty
from accounts.constants import GRADE_CHOICES


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
    grade = models.PositiveSmallIntegerField(
        choices=GRADE_CHOICES, null=True, blank=True
    )  # 学年

    is_profile_complete = models.BooleanField(default=False)
    picture = models.ImageField(null=True, blank=True)
