from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, generate_draft_class, list_players

router = DefaultRouter()
router.register(r'players', PlayerViewSet, basename='player')

urlpatterns = [
    # Functional views
    path("players/draft/", generate_draft_class, name="generate-draft"),
    path("players/all/", list_players, name="list-players"),

    # ViewSet routes (includes delete_all automatically)
    path("", include(router.urls)),
]
