from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Faculty, Department

# class CustomUserAdmin(UserAdmin):
#     model = CustomUser
#     list_display = (
#         "email",
#         "display_name",
#         "faculty",
#         "department",
#         "grade",
#         "is_staff",
#         "is_active",
#     )
#     list_filter = ("is_staff", "is_active", "faculty", "department", "grade")
#     search_fields = (
#         "email",
#         "display_name",
#         "faculty__name",
#         "department__name",
#     )
#     ordering = ("email",)

#     readonly_fields = (
#         "date_joined",
#         "last_login",
#     )
#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         (
#             "個人情報",
#             {"fields": ("display_name", "faculty", "department", "grade")},
#         ),
#         (
#             "権限",
#             {
#                 "fields": (
#                     "is_staff",
#                     "is_active",
#                     "is_superuser",
#                     "groups",
#                     "user_permissions",
#                 )
#             },
#         ),
#         ("重要な日付", {"fields": ("last_login", "date_joined")}),
#     )
#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "email",
#                     "password1",
#                     "password2",
#                     "is_staff",
#                     "is_active",
#                     "faculty",
#                     "department",
#                     "grade",
#                 ),
#             },
#         ),
#     )


# admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(CustomUser)
