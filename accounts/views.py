# accounts/views.py

import logging
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from accounts.models import Department, Faculty
from accounts.serializers import (
    CustomSocialLoginSerializer,
    DepartmentSerializer,
    FacultySerializer,
    ProfileSerializer,
)


logger = logging.getLogger(__name__)


class PublicHelloAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logger.error(f"Request Cookies: {request.COOKIES}")
        return Response({"message": "こんにちは、これは公開エンドポイントです！"})

    def post(self, request):
        logger.error(request.body)
        return Response({"message": "こんにちは、これは公開エンドポイントです！"})


class ProtectedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "message": f"こんにちは、{request.user.email}さん！これは保護されたエンドポイントです。"
            }
        )


class FacultyListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class DepartmentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000/api/auth/callback/google"
    client_class = OAuth2Client
    serializer_class = CustomSocialLoginSerializer
