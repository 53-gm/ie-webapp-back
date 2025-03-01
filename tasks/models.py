from django.conf import settings
from django.db import models
from academics.models import Lecture
from tasks.constants import (
    TASK_PRIORITY_CHOICES,
    TASK_PRIORITY_MEDIUM,
    TASK_STATUS_CHOICES,
    TASK_STATUS_TODO,
)


class Task(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        on_delete=models.CASCADE,
        verbose_name="ユーザー",
    )
    lecture = models.ForeignKey(
        Lecture,
        related_name="tasks",
        on_delete=models.CASCADE,
        verbose_name="講義",
    )
    title = models.CharField(max_length=30, verbose_name="タイトル")
    description = models.CharField(max_length=300, verbose_name="詳細")
    due_date = models.DateTimeField(
        verbose_name="締め切り",
        blank=True,
        null=True,
    )
    priority = models.SmallIntegerField(
        verbose_name="優先度",
        default=TASK_PRIORITY_MEDIUM,
        choices=TASK_PRIORITY_CHOICES,
    )
    status = models.SmallIntegerField(
        verbose_name="状態", default=TASK_STATUS_TODO, choices=TASK_STATUS_CHOICES
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="登録日時")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    class Meta:
        verbose_name_plural = "タスク"
