from django.urls import path, include

urlpatterns = [
    path("lectures/", include("lectures.urls")),
    path("auth/", include("accounts.urls")),
    path("articles/", include("articles.urls")),
]
