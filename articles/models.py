import uuid
import shortuuid
from django.db import models
from config import settings


def generate_short_uuid():
    return shortuuid.ShortUUID().random(length=16)


class Article(models.Model):
    slug = models.CharField(
        default=generate_short_uuid,
        editable=False,
        primary_key=True,
        max_length=16,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="articles",
        on_delete=models.CASCADE,
        verbose_name="著者",
    )
    title = models.CharField(max_length=64)
    content = models.JSONField()  # WYSIWYGエディタのJSON本文を格納

    is_public = models.BooleanField(default=False)  # 公開
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "記事"

    def __str__(self):
        return self.title
