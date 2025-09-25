import random

POSITIONS = {
    "PG": {"dunking":(20,99),"layup":(50,90), "Midshooting":(50,90),"3ptshooting": (50, 90), "passing": (70, 99), "rebounding": (30, 60), "defense": (60, 85), "speed": (75, 99)},
    "SG": {"dunking":(40,99),"layup":(50,90), "Midshooting":(50,90), "3ptshooting": (50, 90), "passing": (50, 85), "rebounding": (40, 70), "defense": (60, 85), "speed": (70, 90)},
    "SF": {"dunking":(50,99),"layup":(50,90), "Midshooting":(50,90), "3ptshooting": (50, 90), "passing": (50, 80), "rebounding": (50, 80), "defense": (65, 90), "speed": (65, 85)},
    "PF": {"layup":(50,90), "Midshooting":(50,90), "3ptshooting": (50, 90), "passing": (40, 75), "rebounding": (70, 95), "defense": (70, 95), "speed": (55, 75)},
    "C":  {"layup":(50,90), "Midshooting":(50,90), "3ptshooting": (50, 90), "passing": (30, 70), "rebounding": (80, 99), "defense": (75, 99), "speed": (40, 75)},
}

FIRST_NAMES = ["John", "Mike", "Chris", "Kevin", "James", "Alex", "David", "Marcus"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

def generate_player():
    position = random.choice(list(POSITIONS.keys()))
    stats = {stat: random.randint(rng[0], rng[1]) for stat, rng in POSITIONS[position].items()}
    overall = int(sum(stats.values()) / len(stats))

    return {
        "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "position": position,
        "overall": overall,
        **stats,
    }
