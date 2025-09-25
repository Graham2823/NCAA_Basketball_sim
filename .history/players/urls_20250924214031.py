from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, generate_draft_class, list_players

# -----------------------------
# DRF Router for ViewSet
# -----------------------------
router = DefaultRouter()
router.register(r'players', PlayerViewSet, basename='player')

# -----------------------------
# URL Patterns
# -----------------------------
urlpatterns = [
    # Functional API views
    path("players/draft/", generate_draft_class, name="generate-draft"),
    path("players/all/", list_players, name="list-players"),

    # ViewSet routes (CRUD + delete_all)
    path("", include(router.urls)),
]
