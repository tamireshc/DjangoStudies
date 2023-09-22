from django.urls import path

from . import views

urlpatterns = [
    path("topics", views.topics, name="topics"),
    path("topics/<int:topic_id>", views.topic, name="topic"),
    path("", views.index, name="index"),
]
