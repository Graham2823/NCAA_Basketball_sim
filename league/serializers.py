from rest_framework import serializers
from .models import League, Conference, Team, Game
from players.serializers import PlayerSerializer


class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = "__all__"

class TeamSerializer(serializers.ModelSerializer):
    # Keep players as a nested serializer
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "overall", "players", "conference", "league"]

    def to_representation(self, instance):
        """
        Conditionally include players based on context.
        """
        rep = super().to_representation(instance)
        if self.context.get("include_players"):
            rep["players"] = PlayerSerializer(instance.players.all(), many=True).data
        else:
            # If you want, you could also return only player IDs
            rep["players"] = list(instance.players.values_list("id", flat=True))
        return rep



class LeagueSerializer(serializers.ModelSerializer):
    teams = TeamSerializer(many=True, read_only=True)

    class Meta:
        model = League
        fields = ["id", "name", "conferences", "teams"]


class GameSerializer(serializers.ModelSerializer):
    home_team = TeamSerializer(read_only=True)
    away_team = TeamSerializer(read_only=True)
    winner = TeamSerializer(read_only=True)

    class Meta:
        model = Game
        fields = "__all__"