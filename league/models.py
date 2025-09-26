from django.db import models
from players.models import Player


class Conference(models.Model):
    name = models.CharField(max_length=100)
    strength = models.FloatField(default=1.0)

    def __str__(self):
        return self.name


class League(models.Model):
    name = models.CharField(max_length=100)
    conferences = models.ManyToManyField(Conference, related_name="leagues")

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="teams")
    conference = models.ForeignKey(
        Conference, on_delete=models.CASCADE, related_name="teams", null=True, blank=True
    )
    players = models.ManyToManyField(Player, related_name="teams", blank=True)

    @property
    def overall(self):
        if self.players.exists():
            return int(sum(p.overall for p in self.players.all()) / self.players.count())
        return 60  # default baseline

    def __str__(self):
        return self.name


class Game(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name="games")
    home_team = models.ForeignKey(Team, related_name="home_games", on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name="away_games", on_delete=models.CASCADE)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    winner = models.ForeignKey(Team, related_name="wins", on_delete=models.CASCADE, null=True, blank=True)
    week = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} (Week {self.week})"
