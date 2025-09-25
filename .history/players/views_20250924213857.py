from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Player
from .serializers import PlayerSerializer
from .utils import generate_player

@api_view(['POST'])
def generate_draft_class(request):
    """Generate N random players and save them"""
    count = int(request.data.get("count", 10))  # default 10 players
    players = []

    for _ in range(count):
        data = generate_player()
        player = Player.objects.create(**data)
        players.append(player)

    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def list_players(request):
    """List all players in DB"""
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)

@action(detail=False, methods=["delete"])
    def delete_all(self, request):
        count = Player.objects.count()
        Player.objects.all().delete()
        return Response(
            {"message": f"Deleted {count} players."},
            status=status.HTTP_200_OK
        )
