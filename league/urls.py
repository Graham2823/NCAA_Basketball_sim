from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConferenceViewSet, LeagueViewSet, TeamViewSet, GameViewSet

router = DefaultRouter()
router.register(r'conferences', ConferenceViewSet, basename='conference')
router.register(r'leagues', LeagueViewSet, basename='league')
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'games', GameViewSet, basename='game')

urlpatterns = [
    path("", include(router.urls)),
]
