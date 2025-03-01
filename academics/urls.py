from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    FacultyListView,
    DepartmentListView,
    LectureViewSet,
    RegistrationViewSet,
    ScheduleListView,
)

router = DefaultRouter()
router.register(r"lectures", LectureViewSet, basename="lecture")
router.register(r"registrations", RegistrationViewSet, basename="registration")

urlpatterns = [
    path("faculties/", FacultyListView.as_view(), name="faculty-list"),
    path("departments/", DepartmentListView.as_view(), name="department-list"),
    path("schedules/", ScheduleListView.as_view(), name="schedule"),
    path("", include(router.urls)),
]
