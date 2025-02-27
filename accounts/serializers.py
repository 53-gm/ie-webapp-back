import logging
from rest_framework import serializers
from .models import Faculty, Department, CustomUser
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import SocialLoginSerializer

logger = logging.getLogger(__name__)


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ["id", "name"]


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name", "faculty"]


class CustomRegisterSerializer(RegisterSerializer):
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), required=False, allow_null=True
    )
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), required=False, allow_null=True
    )
    grade = serializers.ChoiceField(choices=CustomUser.GRADE_CHOICES, required=False)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data["display_name"] = self.validated_data.get("display_name", "")
        data["faculty"] = self.validated_data.get("faculty", None)
        data["department"] = self.validated_data.get("department", None)
        data["grade"] = self.validated_data.get("grade", None)
        data["picture_url"] = self.validated_data.get("picture_url", None)
        data["user_id"] = self.validated_data.get("user_id", None)
        return data

    def save(self, request):
        user = super().save(request)
        user.display_name = self.validated_data.get("display_name", "")
        user.faculty = self.validated_data.get("faculty", None)
        user.department = self.validated_data.get("department", None)
        user.grade = self.validated_data.get("grade", None)
        user.picture_url = self.validated_data.get("picture_url", None)
        user.user_id = self.validate_data.get("user_id", None)
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
            "picture_url",
            "user_id",
        )


class CustomSocialLoginSerializer(SocialLoginSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "picture_url")


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
            "picture_url",
            "user_id",
        ]
        read_only_fields = ["email"]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.is_profile_complete = True  # プロファイル完了
        instance.save()
        return instance
