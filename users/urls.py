from django.conf.urls import url

from . import views

app_name = "users"

urlpatterns = [
    url(r"start/$", views.OAuthFlowStart.as_view(), name="auth_start"),
    url(r"finish/$", views.OAuthFlowFinish.as_view(), name="auth_finish"),
]
