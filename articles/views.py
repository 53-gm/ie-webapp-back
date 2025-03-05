import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from accounts.models import UserProfile
from .models import Article
from .serializers import ArticleSerializer


from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from django.core.files.storage import default_storage
import uuid


class UploadImageView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("file")  # Tiptap側が"file"キーを送る想定
        if not file_obj:
            return Response({"error": "No file uploaded."}, status=400)

        ext = file_obj.name.split(".")[-1]
        filename = f"{uuid.uuid4()}.{ext}"
        saved_path = default_storage.save(f"articles/{filename}", file_obj)
        url = default_storage.url(saved_path)

        return Response({"url": url}, status=200)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=["GET"], url_path="user/(?P<profile_id>[^/.]+)")
    def by_profile_id(self, request, profile_id=None):
        """プロフィールIDに基づいて記事を取得する"""
        try:
            # プロフィールIDからユーザーを特定
            profile = UserProfile.objects.get(profile_id=profile_id)
            user = profile.user

            # クエリパラメータからフィルタリングオプションを取得
            is_public_only = (
                request.query_params.get("is_public", "false").lower() == "true"
            )

            # ユーザーの記事を取得
            queryset = self.get_queryset().filter(author=user)

            # 公開記事のみをフィルタリング（指定がある場合）
            if is_public_only:
                queryset = queryset.filter(is_public=True)

            # ページネーション適用（オプション）
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            # ページネーションなしの場合
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

        except UserProfile.DoesNotExist:
            return Response(
                {
                    "error": {
                        "code": "not_found",
                        "message": "指定されたプロフィールが見つかりません",
                        "status": 404,
                    }
                },
                status=404,
            )
