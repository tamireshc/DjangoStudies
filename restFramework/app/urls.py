from django.urls import path

from . import views

urlpatterns = [
    path("", views.TodoListAndCreate.as_view()),
    path("<int:pk>/", views.TodoDetailChangeAndDelete.as_view()),
]
