from rest_framework import serializers
from .models import Player, RecruitingClass

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = "__all__"


class RecruitingClassSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)

    class Meta:
        model = RecruitingClass
        fields = ["id", "year", "created_at", "players"]
