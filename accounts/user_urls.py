from django.urls import include, path
from .views import (
    DepartmentListView,
    FacultyListView,
    ProfileView,
)

urlpatterns = [
    path("me/profile/", ProfileView.as_view(), name="profile-detail"),
    path("faculties/", FacultyListView.as_view(), name="faculty-list"),
    path("departments/", DepartmentListView.as_view(), name="department-list"),
]
