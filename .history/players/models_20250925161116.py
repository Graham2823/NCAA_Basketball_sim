from django.db import models

class RecruitingClass(models.Model):
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Recruiting Class {self.year} (ID: {self.id})"


class Player(models.Model):
    # Basic info
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=2)
    overall = models.IntegerField()
    height = models.IntegerField()
    weight = models.IntegerField()
    specialization = models.JSONField(default=list)
    state = models.CharField(max_length=50) 

    # Link to recruiting class
    recruiting_class = models.ForeignKey(
        RecruitingClass,
        related_name="players",
        on_delete=models.CASCADE,
    )

    # Stats
    close_shot = models.IntegerField()
    driving_layup = models.IntegerField()
    driving_dunk = models.IntegerField()
    standing_dunk = models.IntegerField()
    post_moves = models.IntegerField()
    mid_range_shot = models.IntegerField()
    three_point_shot = models.IntegerField()
    free_throw = models.IntegerField()
    pass_accuracy = models.IntegerField()
    ball_handle = models.IntegerField()
    speed_with_ball = models.IntegerField()
    interior_defense = models.IntegerField()
    perimeter_defense = models.IntegerField()
    steal = models.IntegerField()
    block = models.IntegerField()
    offensive_rebounding = models.IntegerField()
    defensive_rebounding = models.IntegerField()
    speed = models.IntegerField()
    strength = models.IntegerField()
    vertical = models.IntegerField()
    potential = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.position})"
    
    @property
    def ranking(self):
        """Compute star ranking based on overall"""
        if self.overall >= 74:
            return 5
        elif self.overall >= 70:
            return 4
        elif self.overall >= 65:
            return 3
        elif self.overall >= 60:
            return 2
        else:
            return 1
