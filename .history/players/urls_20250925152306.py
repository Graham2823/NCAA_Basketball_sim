from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, generate_recruting_class, list_players

router = DefaultRouter()
router.register(r'', PlayerViewSet, basename='player')

urlpatterns = [
    # Functional views
    path("recruiting-class/", generate_recruiting_class, name="generate-draft"),
    path("all/", list_players, name="list-players"),

    # ViewSet routes (includes delete_all automatically)
    path("", include(router.urls)),
]
