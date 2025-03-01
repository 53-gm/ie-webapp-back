import logging
from rest_framework import serializers
from academics.models import Faculty, Department
from academics.serializers import DepartmentSerializer, FacultySerializer
from accounts.constants import GRADE_CHOICES
from .models import CustomUser
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer


class CustomRegisterSerializer(RegisterSerializer):
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), required=False, allow_null=True
    )
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )
    grade = serializers.ChoiceField(choices=GRADE_CHOICES, required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["display_name"] = self.validated_data.get("display_name", "")
        data["faculty"] = self.validated_data.get("faculty", None)
        data["department"] = self.validated_data.get("department", None)
        data["grade"] = self.validated_data.get("grade", None)
        data["picture"] = self.validated_data.get("picture", None)
        data["user_id"] = self.validated_data.get("user_id", None)
        return data

    def save(self, request):
        user = super().save(request)
        user.display_name = self.validated_data.get("display_name", "")
        user.faculty = self.validated_data.get("faculty", None)
        user.department = self.validated_data.get("department", None)
        user.grade = self.validated_data.get("grade", None)
        user.picture = self.validated_data.get("picture", None)
        user.user_id = self.validated_data.get("user_id", None)
        user.is_profile_complete = False
        user.save()
        return user


class CustomUserDetailsSerializer(UserDetailsSerializer):
    faculty = FacultySerializer(read_only=True)
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), write_only=True, source="faculty"
    )
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), write_only=True, source="department"
    )

    class Meta(UserDetailsSerializer.Meta):
        fields = (
            "email",
            "department",
            "department_id",
            "display_name",
            "faculty",
            "faculty_id",
            "grade",
            "is_profile_complete",
            "picture",
            "user_id",
        )

    def validate_user_id(self, value):
        user = self.context.get("request").user if self.context.get("request") else None
        if (
            user
            and CustomUser.objects.filter(user_id=value).exclude(id=user.id).exists()
        ):
            raise serializers.ValidationError("このユーザーIDは既に使用されています")
        return value


class ProfileSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), write_only=True, source="faculty"
    )
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), write_only=True, source="department"
    )

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "display_name",
            "faculty",
            "faculty_id",
            "department",
            "department_id",
            "grade",
            "is_profile_complete",
            "picture",
            "user_id",
        ]
        read_only_fields = ["email", "is_profile_complete"]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.is_profile_complete = True  # プロファイル完了
        instance.save()
        return instance

    def validate_user_id(self, value):
        user = self.context.get("request").user if self.context.get("request") else None
        if (
            user
            and CustomUser.objects.filter(user_id=value).exclude(id=user.id).exists()
        ):
            raise serializers.ValidationError("このユーザーIDは既に使用されています")
        return value
