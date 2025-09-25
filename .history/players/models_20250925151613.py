from django.db import models

class Player(models.Model):
    POSITIONS = [
        ("PG", "Point Guard"),
        ("SG", "Shooting Guard"),
        ("SF", "Small Forward"),
        ("PF", "Power Forward"),
        ("C", "Center"),
    ]

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=2, choices=POSITIONS)
    
    overall = models.IntegerField(null=True, blank=True)
    potential = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)  # in inches
    weight = models.IntegerField(null=True, blank=True)  # in lbs

    # ------------------ Finishing ------------------
    close_shot = models.IntegerField(null=True, blank=True)
    driving_layup = models.IntegerField(null=True, blank=True)
    driving_dunk = models.IntegerField(null=True, blank=True)
    standing_dunk = models.IntegerField(null=True, blank=True)
    post_moves = models.IntegerField(null=True, blank=True)

    # ------------------ Shooting ------------------
    mid_range_shot = models.IntegerField(null=True, blank=True)
    three_point_shot = models.IntegerField(null=True, blank=True)
    free_throw = models.IntegerField(null=True, blank=True)

    # ------------------ Playmaking ------------------
    pass_accuracy = models.IntegerField(null=True, blank=True)
    ball_handle = models.IntegerField(null=True, blank=True)
    speed_with_ball = models.IntegerField(null=True, blank=True)

    # ------------------ Defense ------------------
    interior_defense = models.IntegerField(null=True, blank=True)
    perimeter_defense = models.IntegerField(null=True, blank=True)
    steal = models.IntegerField(null=True, blank=True)
    block = models.IntegerField(null=True, blank=True)

    # ------------------ Rebounding ------------------
    offensive_rebounding = models.IntegerField(null=True, blank=True)
    defensive_rebounding = models.IntegerField(null=True, blank=True)

    # ------------------ Physicals ------------------
    speed = models.IntegerField(null=True, blank=True)
    strength = models.IntegerField(null=True, blank=True)
    vertical = models.IntegerField(null=True, blank=True)

    specialization = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.position}) - OVR {self.overall}"
