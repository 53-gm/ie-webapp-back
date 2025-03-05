from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from .models import Department, Faculty, UserProfile
from rest_framework.response import Response
from .serializers import (
    DepartmentSerializer,
    FacultySerializer,
    UserProfileSerializer,
    UserWithProfileSerializer,
)
from rest_framework.permissions import AllowAny


class FacultyListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class DepartmentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    """ユーザープロフィールの取得・更新ビュー"""

    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """現在のユーザーのプロフィールを取得"""
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

    def update(self, request, *args, **kwargs):
        """プロフィール更新処理をカスタマイズ"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # 更新後のプロフィール完了状態をレスポンスに含める
        result = serializer.data
        return Response(result)


class ProfileDetailView(generics.RetrieveAPIView):
    """プロフィールIDによるユーザープロフィール取得ビュー"""

    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = "profile_id"
    lookup_url_kwarg = "profile_id"

    def get_queryset(self):
        return UserProfile.objects.all()


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/api/auth/callback/google"
    client_class = OAuth2Client

    def get_response(self):
        """ログイン成功時のレスポンスをカスタマイズ"""
        # オリジナルのレスポンスを取得（トークン情報など）
        original_response = super().get_response()
        original_data = original_response.data

        # ユーザー情報をUserWithProfileSerializerでシリアライズ
        user_data = UserWithProfileSerializer(self.user).data

        # 両方のデータを結合
        response_data = {**original_data, "user": user_data}

        return Response(response_data)
