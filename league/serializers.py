from rest_framework import serializers
from .models import League, Conference, Team, Game
from players.serializers import PlayerSerializer


class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "overall", "players", "conference", "league"]


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