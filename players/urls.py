from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, generate_recruiting_class, list_players, get_recruiting_class, list_recruiting_classes

router = DefaultRouter()
router.register(r'', PlayerViewSet, basename='player')

urlpatterns = [
    # Functional views
    path("recruiting-class/", generate_recruiting_class, name="recruiting-class"),
    path("all/", list_players, name="list-players"),
    path("class/<int:class_id>/", get_recruiting_class, name="get-recruiting-class"),
     path("recruiting-classes/", list_recruiting_classes, name="list-recruiting-classes"),

    # ViewSet routes (includes delete_all automatically)
    path("", include(router.urls)),
]
