from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from .models import Player, RecruitingClass
from .serializers import PlayerSerializer, RecruitingClassSerializer
from .utils import generate_player
from datetime import datetime

# -----------------------------
# Existing functional API views
# -----------------------------

@api_view(["POST"])
def generate_recruiting_class(request):
    """Generate a recruiting class with N random players"""
    count = int(request.data.get("count", 10))  # default 10 players
    year = int(request.data.get("year", datetime.now().year))

    # Create recruiting class
    recruiting_class = RecruitingClass.objects.create(year=year)

    players = []
    for _ in range(count):
        data = generate_player()
        player = Player.objects.create(
            recruiting_class=recruiting_class,
            **data
        )
        players.append(player)

    serializer = RecruitingClassSerializer(recruiting_class)
    return Response(serializer.data)


@api_view(['GET'])
def list_players(request):
    """List all players in DB"""
    players = Player.objects.all().order_by('-potential')
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)

# -----------------------------
# ViewSet for RESTful endpoints
# -----------------------------

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

    @action(detail=False, methods=["delete"])
    def delete_all(self, request):
        """Delete all players"""
        count = Player.objects.count()
        Player.objects.all().delete()
        return Response(
            {"message": f"Deleted {count} players."},
            status=status.HTTP_200_OK
        )
