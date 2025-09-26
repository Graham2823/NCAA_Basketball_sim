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
        Simulate a realistic college basketball game between two teams with box scores.
        Expects JSON: { "home_team_id": 1, "away_team_id": 2 }
        """
        home_id = request.data.get("home_team_id")
        away_id = request.data.get("away_team_id")

        try:
            home_team = Team.objects.prefetch_related('players').get(id=home_id)
            away_team = Team.objects.prefetch_related('players').get(id=away_id)
        except Team.DoesNotExist:
            return Response({"error": "Invalid team IDs"}, status=status.HTTP_400_BAD_REQUEST)

        def simulate_player_stats(player, team_off_factor, opp_def_factor):
            """Simulate individual stats including boom games."""
            performance = random.uniform(0.85, 1.15)

            # Base points calculation
            base_points = (
                player.close_shot * 0.25 +
                player.driving_layup * 0.15 +
                player.driving_dunk * 0.10 +
                player.mid_range_shot * 0.20 +
                player.three_point_shot * 0.20 +
                player.free_throw * 0.10
            ) * performance * team_off_factor / (opp_def_factor + 1)

            # Boom game chance: 5% chance to score 1.5–2x more
            if random.random() < 0.05:
                boom_multiplier = random.uniform(1.5, 2.0)
                points = int(base_points * boom_multiplier)
            else:
                points = int(base_points)

            # Scale rebounds, assists, steals, blocks realistically
            rebounds = int((player.offensive_rebounding*0.4 + player.defensive_rebounding*0.6) * performance / 10)
            assists = int((player.pass_accuracy*0.3 + player.ball_handle*0.2) * performance / 20)
            steals = int(player.steal * performance / 30)
            blocks = int(player.block * performance / 25)
            turnovers = max(0, int(5 - ((player.ball_handle + player.pass_accuracy)/40) * performance))

            return {
                "player_id": player.id,
                "name": player.name,
                "position": player.position,
                "points": points,
                "rebounds": rebounds,
                "assists": assists,
                "steals": steals,
                "blocks": blocks,
                "turnovers": turnovers,
            }

        # -------------------------------
        # Compute team offensive/defensive strength
        # -------------------------------
        def team_off_def(team):
            offense = sum(
                p.three_point_shot + p.mid_range_shot + p.close_shot + p.driving_layup + p.driving_dunk
                for p in team.players.all()
            )
            defense = sum(
                p.perimeter_defense + p.interior_defense + p.steal + p.block + p.defensive_rebounding
                for p in team.players.all()
            )
            return offense, defense

        home_off, home_def = team_off_def(home_team)
        away_off, away_def = team_off_def(away_team)

        # Normalize team factors to target realistic scores
        # Average points per player ~10-20, team ~60-110
        home_factor = home_off / (home_off + away_def + 50)  # +50 prevents explosion
        away_factor = away_off / (away_off + home_def + 50)

        # -------------------------------
        # Simulate player box scores
        # -------------------------------
        home_box = [simulate_player_stats(p, team_off_factor=home_factor*15, opp_def_factor=away_def/100)
                    for p in home_team.players.all()]
        away_box = [simulate_player_stats(p, team_off_factor=away_factor*15, opp_def_factor=home_def/100)
                    for p in away_team.players.all()]

        # -------------------------------
        # Compute team total scores
        # -------------------------------
        home_score = sum(p['points'] for p in home_box)
        away_score = sum(p['points'] for p in away_box)

        winner = home_team if home_score >= away_score else away_team

        # -------------------------------
        # Save game to DB
        # -------------------------------
        game = Game.objects.create(
            league=home_team.league,
            home_team=home_team,
            away_team=away_team,
            home_score=home_score,
            away_score=away_score,
            winner=winner,
        )

        # -------------------------------
        # Return response with box scores
        # -------------------------------
        return Response({
            "game_id": game.id,
            "home_team": home_team.name,
            "away_team": away_team.name,
            "home_score": home_score,
            "away_score": away_score,
            "winner": winner.name,
            "home_box": home_box,
            "away_box": away_box,
        }, status=status.HTTP_201_CREATED)

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
