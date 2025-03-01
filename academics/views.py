from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import generics

from academics.filters import RegistrationFilter, LectureFilter
from .models import Department, Faculty, Lecture, Registration, Schedule
from rest_framework import viewsets, permissions
from .serializers import (
    LectureSerializer,
    RegistrationSerializer,
    ScheduleSerializer,
    DepartmentSerializer,
    FacultySerializer,
)
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend


class FacultyListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class DepartmentListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = LectureFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # ユーザーの所属学科または学部に関連する講義、または所有者がいない講義
            return Lecture.objects.filter(
                Q(departments=user.department)
                & Q(departments__faculty=user.faculty)
                & (Q(owner__isnull=True) | Q(owner=user))
            ).distinct()
        else:
            # 認証されていないユーザーは所有者がいない講義のみ閲覧可能
            return Lecture.objects.filter(owner__isnull=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class RegistrationViewSet(viewsets.ModelViewSet):
    """
    Registration ViewSet:
    - 認証ユーザー自身の講義登録のみを管理。
    - 認証ユーザーのみがアクセス可能。
    """

    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RegistrationFilter

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ScheduleListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
