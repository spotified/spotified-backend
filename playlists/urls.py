from django.conf.urls import url

from . import views

app_name = "playlists"

urlpatterns = [url(r"/", views.PlayList.as_view(), name="playlist")]
