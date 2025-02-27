from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, UploadImageView

router = DefaultRouter()
router.register(r"articles", ArticleViewSet, basename="article")

urlpatterns = [
    path("", include(router.urls)),
    path("upload_image/", UploadImageView.as_view(), name="upload_image"),
]
