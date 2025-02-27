from rest_framework import serializers

from accounts.models import CustomUser
from accounts.serializers import CustomUserDetailsSerializer
from .models import Article


class ArticleSerializer(serializers.ModelSerializer):
    author = CustomUserDetailsSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        write_only=True,
        source="author",
        required=False,
    )

    class Meta:
        model = Article
        fields = (
            "slug",
            "title",
            "content",
            "author",
            "author_id",
            "is_public",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("author", "created_at", "updated_at")
