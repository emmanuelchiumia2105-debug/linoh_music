from django.urls import path
from . import views


urlpatterns = [
    path("", views.home, name="home"),

    path(
        "song/<int:song_id>/play/",
        views.record_play,
        name="record_play"
    ),
]