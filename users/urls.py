from django.urls import path

from . import views

app_name = "auth"

urlpatterns = [
    path("start/", views.OAuthFlowStart.as_view(), name="start"),
    path("finish/", views.OAuthFlowFinish.as_view(), name="finish"),
    path(
        "token/refresh/",
        views.SpotifyAuthTokenRefresh.as_view(),
        name="auth_token_refresh",
    ),
]
