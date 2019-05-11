from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("start/", views.OAuthFlowStart.as_view(), name="auth_start"),
    path("finish/", views.OAuthFlowFinish.as_view(), name="auth_finish"),
]
