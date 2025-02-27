# accounts/urls.py

from django.urls import include, path
from .views import (
    DepartmentListView,
    FacultyListView,
    GoogleLogin,
    ProfileView,
    PublicHelloAPIView,
    ProtectedAPIView,
)

urlpatterns = [
    path("public/hello/", PublicHelloAPIView.as_view(), name="public-hello-api"),
    path("protected/", ProtectedAPIView.as_view(), name="protected-api"),
    path("google/", GoogleLogin.as_view(), name="google_login"),
    path("faculties/", FacultyListView.as_view(), name="faculty-list"),
    path("departments/", DepartmentListView.as_view(), name="department-list"),
    path("profile/", ProfileView.as_view(), name="profile-complete"),
]
