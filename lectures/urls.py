from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LectureViewSet, RegistrationViewSet, ScheduleListView, TaskViewSet


router = DefaultRouter()
router.register(r"lectures", LectureViewSet, basename="lecture")
router.register(r"registrations", RegistrationViewSet, basename="registration")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include(router.urls)),
    path("schedules/", ScheduleListView.as_view(), name="schedule"),
]
