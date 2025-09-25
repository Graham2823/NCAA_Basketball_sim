from django.urls import path
from .views import generate_draft_class, list_players

urlpatterns = [
    path("draft/", generate_draft_class),  # POST -> generate players
    path("all/", list_players),            # GET -> list all players
]
