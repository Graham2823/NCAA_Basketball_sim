from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, generate_recruiting_class, list_players

router = DefaultRouter()
router.register(r'', PlayerViewSet, basename='player')

urlpatterns = [
    # Functional views
    path("recruiting-class/", generate_recruiting_class, name="recruiting-class"),
    path("all/", list_players, name="list-players"),
    path("class/<int:class_id>/", get_recruiting_class, name="get-recruiting-class"),

    # ViewSet routes (includes delete_all automatically)
    path("", include(router.urls)),
]
