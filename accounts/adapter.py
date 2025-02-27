from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.core.exceptions import ImproperlyConfigured

import logging

logger = logging.getLogger(__name__)


class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        data = form.cleaned_data
        user.faculty = data.get("faculty")
        user.department = data.get("department")
        user.grade = data.get("grade")
        user.picture_url = data.get("picture_url")
        user.is_profile_complete = data.get("is_profile_complete")
        user.save()
        return user


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)

        if sociallogin.account.provider == "google":
            extra_data = sociallogin.account.extra_data
            picture_url = extra_data.get("picture")
            username = extra_data.get("name")

            if picture_url:
                user.picture_url = picture_url
                user.display_name = username
                user.save()

        return user
