# from django.urls import path

# from . import views

# urlpatterns = [
#     path("", views.TodoListAndCreate.as_view()),
#     path("<int:pk>/", views.TodoDetailChangeAndDelete.as_view()),
# ]

# Using router

from rest_framework.routers import DefaultRouter

from app.views import TodoViewSet

router = DefaultRouter()
router.register("", TodoViewSet)
urlpatterns = router.urls
