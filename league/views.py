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
        Create 4 teams with 15 randomly generated players each,
        ensuring positional balance: 2 of each position + 5 random.
        """
        league = self.get_object()
        positions = ["PG", "SG", "SF", "PF", "C"]

        for i in range(4):  # make *exactly* 4 teams
            team = Team.objects.create(name=f"Team {i+1}", league=league)

            # --- Generate 2 players for each position ---
            for pos in positions:
                for _ in range(2):
                    data = generate_player(position=pos)  # force position
                    player = Player.objects.create(**data, recruiting_class=None)
                    team.players.add(player)

            # --- Generate 5 random players ---
            for _ in range(5):
                data = generate_player()  # random position
                player = Player.objects.create(**data, recruiting_class=None)
                team.players.add(player)

        # Return the updated league with its teams + players
        return Response(LeagueSerializer(league).data)
    
    @action(detail=False, methods=["post"])
    def create_league(self, request):
        """
        Create a League with 2 Conferences and 5 Teams in each conference (10 teams total)
        Conference 1 teams are stronger on average than Conference 2 teams
        Each team has some randomness in player skill distribution with capped elite/good players
        """
        league_name = request.data.get("name", "Sample League")
        league = League.objects.create(name=league_name)

        # Create two conferences
        conf1 = Conference.objects.create(name="Conference 1", strength=1.0)
        conf2 = Conference.objects.create(name="Conference 2", strength=0.8)
        league.conferences.add(conf1, conf2)

        positions = ["PG", "SG", "SF", "PF", "C"]

        # Base skill pools for each conference (before randomization)
        conference_skill_pools = {
            conf1: {"elite": 3, "good": 5, "mid": 5, "bad": 2},  # stronger conference
            conf2: {"elite": 1, "good": 4, "mid": 6, "bad": 6},  # weaker conference
        }

        for conf, base_pool in conference_skill_pools.items():
            for i in range(5):  # 5 teams per conference
                team = Team.objects.create(name=f"{conf.name} Team {i+1}", league=league)

                # Copy and shuffle the pool for randomness
                team_skill_pool = []
                for skill, count in base_pool.items():
                    team_skill_pool.extend([skill] * count)
                random.shuffle(team_skill_pool)

                # Track how many elite/good players have been assigned to enforce caps
                skill_count = {"elite": 0, "good": 0}

                # --- Generate 2 players per position first ---
                for pos in positions:
                    for _ in range(2):
                        if team_skill_pool:
                            # Pop a random skill, respecting caps
                            while True:
                                skill_level = team_skill_pool.pop(random.randint(0, len(team_skill_pool) - 1))
                                if skill_level == "elite" and skill_count["elite"] >= 3:
                                    continue
                                if skill_level == "good" and skill_count["good"] >= 5:
                                    continue
                                break
                        else:
                            skill_level = "mid"

                        if skill_level in skill_count:
                            skill_count[skill_level] += 1

                        data = generate_player(position=pos, skillLvl=skill_level)
                        player = Player.objects.create(**data, recruiting_class=None)
                        team.players.add(player)

                # --- Fill remaining 5 spots randomly ---
                while len(team.players.all()) < 15:
                    if team_skill_pool:
                        while True:
                            skill_level = team_skill_pool.pop(random.randint(0, len(team_skill_pool) - 1))
                            if skill_level == "elite" and skill_count["elite"] >= 3:
                                continue
                            if skill_level == "good" and skill_count["good"] >= 5:
                                continue
                            break
                    else:
                        skill_level = "mid"

                    if skill_level in skill_count:
                        skill_count[skill_level] += 1

                    data = generate_player(skillLvl=skill_level)
                    player = Player.objects.create(**data, recruiting_class=None)
                    team.players.add(player)

        return Response(LeagueSerializer(league).data)
    @action(detail=True, methods=["get"])
    def get_league_teams(self, request, pk=None):
        league = self.get_object()
        teams = league.teams.all()  # use the related_name here
        serialized_teams = TeamSerializer(teams, many=True, context={"include_players": True})
        return Response(serialized_teams.data)


    @action(detail=True, methods=["get"])
    def get_league_players(self, request, pk=None):
        league = self.get_object()
        players = Player.objects.filter(teams__league=league).distinct().order_by("-overall")
        serialized_players = PlayerSerializer(players, many=True)
        return Response(serialized_players.data)





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

            rebounds = (player.offensive_rebounding*0.4 + player.defensive_rebounding*0.6) * performance / 10 * (minutes / 40)
            assists = (player.pass_accuracy*0.3 + player.ball_handle*0.2) * performance / 6.5 * (minutes / 40)
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
            positions = ["PG", "SG", "SF", "PF", "C"]

            # --- Force starters: best at each position ---
            starters = []
            for pos in positions:
                best_at_pos = next((p for p in players if p.position == pos), None)
                if best_at_pos:
                    starters.append(best_at_pos)

            # Fill any missing positions (if roster is weird) with best remaining
            used_ids = {p.id for p in starters}
            while len(starters) < 5 and players:
                extra = next((p for p in players if p.id not in used_ids), None)
                if extra:
                    starters.append(extra)
                    used_ids.add(extra.id)

            # --- Prepare backups by position ---
            backups_by_pos = {pos: [] for pos in positions}
            for p in players:
                if p.id not in used_ids:
                    backups_by_pos[p.position].append(p)
                    used_ids.add(p.id)

            total_minutes = 200.0
            starter_minutes = {}
            backup_minutes = {}

            # --- Assign starter minutes (weighted by overall) ---
            starter_overall_sum = sum(p.overall for p in starters)
            for p in starters:
                starter_minutes[p.id] = total_minutes * (p.overall / starter_overall_sum) * 0.85

            # Remaining minutes to distribute to backups
            remaining_minutes = total_minutes - sum(starter_minutes.values())

            # --- Assign backup minutes per position ---
            bench_minutes = {}
            for pos in positions:
                starter = next((p for p in starters if p.position == pos), None)
                if starter:
                    starter_min = starter_minutes[starter.id]
                else:
                    starter_min = 0
                pos_backups = backups_by_pos[pos]
                if not pos_backups:
                    continue
                # Total minutes for this position's backups: assume starter gets 32 max
                target_pos_minutes = max(0, 40 - starter_min)
                # Randomly decide how many backups play
                n_playing = random.randint(1, len(pos_backups))
                playing_backups = random.sample(pos_backups, k=n_playing)
                # Randomly split minutes among playing backups
                weights = [random.random() for _ in range(n_playing)]
                weight_sum = sum(weights)
                for b, w in zip(playing_backups, weights):
                    bench_minutes[b.id] = target_pos_minutes * (w / weight_sum)

            # Combine all players and minutes
            all_players = starters + [p for lst in backups_by_pos.values() for p in lst if p.id in bench_minutes]
            all_minutes = [starter_minutes[p.id] for p in starters] + [bench_minutes[p.id] for p in all_players if p.id in bench_minutes]

            # Scale to exactly 200
            scale = total_minutes / sum(all_minutes)
            all_minutes = [m * scale for m in all_minutes]

            # Fix rounding drift
            rounded_minutes = [round(m) for m in all_minutes]
            diff = 200 - sum(rounded_minutes)
            if diff != 0:
                rounded_minutes[-1] += diff

            # Simulate stats
            box = [
                simulate_player_stats(p, mins, team_factor * 20, opp_def_factor / 100)
                for p, mins in zip(all_players, rounded_minutes)
            ]

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




