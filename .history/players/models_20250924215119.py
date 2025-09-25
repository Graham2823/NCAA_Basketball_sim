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
    overall = models.IntegerField(null=True, blank=True)
    dunking = models.IntegerField(null=True, blank=True)
    layup = models.IntegerField(null=True, blank=True)
    Midshooting = models.IntegerField(null=True, blank=True)
    threeptshooting = models.IntegerField(null=True, blank=True)
    passing = models.IntegerField(null=True, blank=True)
    rebounding = models.IntegerField(null=True, blank=True)
    defense = models.IntegerField(null=True, blank=True)
    speed = models.IntegerField(null=True, blank=True)
    potential = models.IntegerField(null=True, blank=True)
    height=models.integerField(null=True, blank=True)
    weight=models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.position}) - OVR {self.overall}"
