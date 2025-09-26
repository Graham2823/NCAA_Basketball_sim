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

            # generate 15 players and assign
            for _ in range(15):
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
        Simulate a realistic college basketball game between two teams with bench rotation.
        Expects JSON: { "home_team_id": 1, "away_team_id": 2 }
        """
        home_id = request.data.get("home_team_id")
        away_id = request.data.get("away_team_id")

        try:
            home_team = Team.objects.prefetch_related('players').get(id=home_id)
            away_team = Team.objects.prefetch_related('players').get(id=away_id)
        except Team.DoesNotExist:
            return Response({"error": "Invalid team IDs"}, status=status.HTTP_400_BAD_REQUEST)

        # -------------------------
        # Player stat simulation
        # -------------------------
        def simulate_player_stats(player, minutes, team_off_factor, opp_def_factor):
            performance = random.uniform(0.95, 1.05)

            productivity = (
                player.close_shot * 0.25 +
                player.driving_layup * 0.15 +
                player.driving_dunk * 0.10 +
                player.mid_range_shot * 0.20 +
                player.three_point_shot * 0.20 +
                player.free_throw * 0.10
            ) * performance * team_off_factor / (opp_def_factor + 1)

            points = productivity * (minutes / 40)

            if random.random() < 0.05:
                points *= random.uniform(1.4, 1.8)

            rebounds = (player.offensive_rebounding*0.4 + player.defensive_rebounding*0.6) * performance / 8 * (minutes / 40)
            assists = (player.pass_accuracy*0.3 + player.ball_handle*0.2) * performance / 5 * (minutes / 40)
            steals = player.steal * performance / 25 * (minutes / 40)
            blocks = player.block * performance / 20 * (minutes / 40)
            turnovers = max(0, (minutes / 40) * (5 - (player.ball_handle + player.pass_accuracy)/50) * performance)

            return {
                "player_id": player.id,
                "name": player.name,
                "position": player.position,
                "minutes": round(minutes),
                "points": round(points),
                "rebounds": round(rebounds),
                "assists": round(assists),
                "steals": round(steals),
                "blocks": round(blocks),
                "turnovers": round(turnovers),
            }

        # -------------------------
        # Team strengths
        # -------------------------
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

        home_factor = home_off / (home_off + away_def + 50)
        away_factor = away_off / (away_off + home_def + 50)

        # -------------------------
        # Simulate team with 200 minutes
        # -------------------------
        def simulate_team(team, team_factor, opp_def_factor):
            players = sorted(team.players.all(), key=lambda p: p.overall, reverse=True)
            starters = players[:5]
            bench = players[5:10]

            total_minutes = 200.0
            box = []

            # Starters: 85% of total minutes, weighted by overall
            starter_overall_sum = sum(p.overall for p in starters)
            starter_minutes = [total_minutes * (p.overall / starter_overall_sum) * 0.85 for p in starters]
            total_starter = sum(starter_minutes)
            remaining_minutes = total_minutes - total_starter

            # Bench: top 3–5 players, remaining minutes weighted by overall
            bench_players = bench[:random.randint(3, 5)]
            bench_overall_sum = sum(p.overall for p in bench_players) if bench_players else 1
            bench_minutes = [remaining_minutes * (p.overall / bench_overall_sum) for p in bench_players]

            # Combine players
            all_players = starters + bench_players
            all_minutes = starter_minutes + bench_minutes

            # Scale slightly to hit exactly 200
            scale = total_minutes / sum(all_minutes)
            all_minutes = [m * scale for m in all_minutes]

            # Simulate stats
            for p, mins in zip(all_players, all_minutes):
                box.append(simulate_player_stats(p, mins, team_factor*20, opp_def_factor/100))

            return box

        home_box = simulate_team(home_team, home_factor, away_def)
        away_box = simulate_team(away_team, away_factor, home_def)

        # -------------------------
        # Team totals
        # -------------------------
        home_score = sum(p['points'] for p in home_box)
        away_score = sum(p['points'] for p in away_box)

        winner = home_team if home_score >= away_score else away_team

        game = Game.objects.create(
            league=home_team.league,
            home_team=home_team,
            away_team=away_team,
            home_score=home_score,
            away_score=away_score,
            winner=winner,
        )

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
