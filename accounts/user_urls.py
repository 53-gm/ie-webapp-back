from django.urls import include, path
from .views import (
    ProfileView,
)

urlpatterns = [
    # path('me/', UserDetailView.as_view(), name='user-detail'),
    path("me/profile/", ProfileView.as_view(), name="profile-complete"),
]
