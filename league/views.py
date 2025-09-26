from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import League, Conference, Team, Game
from .serializers import LeagueSerializer, ConferenceSerializer, TeamSerializer, GameSerializer
from players.models import Player
from players.utils import generate_player
from players.serializers import PlayerSerializer
import random


class ConferenceViewSet(viewsets.ModelViewSet):
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = League.objects.all()
    serializer_class = LeagueSerializer

    @action(detail=True, methods=["post"])
    def create_teams(self, request, pk=None):
        """
        Create 4 teams with 5 randomly generated players each
        """
        league = self.get_object()

        # create teams
        for i in range(4):
            team = Team.objects.create(name=f"Team {i+1}", league=league)

            # generate 5 players and assign
            for _ in range(5):
                data = generate_player()
                player = Player.objects.create(**data, recruiting_class=None)  # not tied to recruiting class
                team.players.add(player)

        return Response(LeagueSerializer(league).data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=["get"])
    def roster(self, request, pk=None):
        team = self.get_object()
        players = team.players.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer

    @action(detail=False, methods=["post"])
    def simulate(self, request):
        """
        Simulate a game between two teams
        Expects: { "home_team_id": 1, "away_team_id": 2 }
        """
        home_id = request.data.get("home_team_id")
        away_id = request.data.get("away_team_id")

        try:
            home_team = Team.objects.get(id=home_id)
            away_team = Team.objects.get(id=away_id)
        except Team.DoesNotExist:
            return Response({"error": "Invalid team IDs"}, status=status.HTTP_400_BAD_REQUEST)

        # Simple simulation: team overall + random factor
        home_score = home_team.overall + random.randint(-10, 10)
        away_score = away_team.overall + random.randint(-10, 10)

        winner = home_team if home_score >= away_score else away_team

        game = Game.objects.create(
            league=home_team.league,
            home_team=home_team,
            away_team=away_team,
            home_score=home_score,
            away_score=away_score,
            winner=winner,
        )

        return Response(GameSerializer(game).data, status=status.HTTP_201_CREATED)


@api_view(["POST"])
def create_league(request):
    """
    Create a League with 1 Conference
    """
    league_name = request.data.get("name", "Sample League")
    conf_name = request.data.get("conference", "Default Conference")

    conf = Conference.objects.create(name=conf_name, strength=1.0)
    league = League.objects.create(name=league_name)
    league.conferences.add(conf)

    return Response(LeagueSerializer(league).data)
