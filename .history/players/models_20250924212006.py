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

    # Basic stats
    overall = models.IntegerField()
    shooting = models.IntegerField()
    passing = models.IntegerField()
    rebounding = models.IntegerField()
    defense = models.IntegerField()
    speed = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.position}) - OVR {self.overall}"
