import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.files.storage import default_storage
from rest_framework import viewsets, permissions
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
