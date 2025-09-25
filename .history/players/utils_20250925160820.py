import random

# ------------------ Position-specific stat ranges ------------------
STAT_RANGES = {
    "PG": {
        # Finishing
        "close_shot": (35, 95),
        "driving_layup": (45, 95),
        "driving_dunk": (35, 95),
        "standing_dunk": (30, 60),
        "post_moves": (30, 60),

        # Shooting
        "mid_range_shot": (40, 95),
        "three_point_shot": (40, 99),
        "free_throw": (55, 99),

        # Playmaking
        "pass_accuracy": (50, 99),
        "ball_handle": (50, 99),
        "speed_with_ball": (75, 99),

        # Defense
        "interior_defense": (35, 60),
        "perimeter_defense": (35, 95),
        "steal": (40, 95),
        "block": (30, 65),

        # Rebounding
        "offensive_rebounding": (30, 65),
        "defensive_rebounding": (40, 85),

        # Physicals
        "speed": (75, 99),
        "strength": (20, 75),
        "vertical": (30, 95),
        "potential":(60,99),
    },
    "SG": {
        "close_shot": (35, 95),
        "driving_layup": (35, 95),
        "driving_dunk": (35, 95),
        "standing_dunk": (35, 75),
        "post_moves": (35, 85),

        "mid_range_shot": (40, 95),
        "three_point_shot": (35, 99),
        "free_throw": (50, 99),

        "pass_accuracy": (35, 95),
        "ball_handle": (45, 95),
        "speed_with_ball": (65, 95),

        "interior_defense": (35, 70),
        "perimeter_defense": (40, 99),
        "steal": (35, 90),
        "block": (35, 75),

        "offensive_rebounding": (35, 75),
        "defensive_rebounding": (45, 90),

        "speed": (70, 95),
        "strength": (30, 80),
        "vertical": (30, 95),
        "potential":(60,99),
    },
    "SF": {
        "close_shot": (35, 95),
        "driving_layup": (40, 95),
        "driving_dunk": (35, 99),
        "standing_dunk": (35, 95),
        "post_moves": (35, 95),

        "mid_range_shot": (35, 95),
        "three_point_shot": (35, 95),
        "free_throw": (45, 95),

        "pass_accuracy": (40, 90),
        "ball_handle": (40, 85),
        "speed_with_ball": (50, 85),

        "interior_defense": (40, 85),
        "perimeter_defense": (40, 85),
        "steal": (35, 90),
        "block": (35, 85),

        "offensive_rebounding": (35, 85),
        "defensive_rebounding": (35, 95),

        "speed": (55, 90),
        "strength": (35, 90),
        "vertical": (35, 90),
        "potential":(60,99),
    },
    "PF": {
        "close_shot": (50, 95),
        "driving_layup": (40, 85),
        "driving_dunk": (35, 99),
        "standing_dunk": (55, 99),
        "post_moves": (45, 95),

        "mid_range_shot": (40, 90),
        "three_point_shot": (35, 90),
        "free_throw": (45, 85),

        "pass_accuracy": (40, 80),
        "ball_handle": (40, 75),
        "speed_with_ball": (40, 70),

        "interior_defense": (45, 95),
        "perimeter_defense": (35, 75),
        "steal": (35, 80),
        "block": (45, 99),

        "offensive_rebounding": (45, 95),
        "defensive_rebounding": (45, 95),

        "speed": (45, 75),
        "strength": (45, 95),
        "vertical": (30, 85),
        "potential":(60,99),
    },
    "C": {
        "close_shot": (50, 99),
        "driving_layup": (40, 75),
        "driving_dunk": (40, 99),
        "standing_dunk": (55, 99),
        "post_moves": (50, 99),

        "mid_range_shot": (35, 85),
        "three_point_shot": (30, 90),
        "free_throw": (40, 90),

        "pass_accuracy": (35, 85),
        "ball_handle": (30, 60),
        "speed_with_ball": (30, 60),

        "interior_defense": (55, 99),
        "perimeter_defense": (35, 65),
        "steal": (40, 75),
        "block": (45, 99),

        "offensive_rebounding": (55, 99),
        "defensive_rebounding": (55, 99),

        "speed": (30, 70),
        "strength": (55, 99),
        "vertical": (35, 85),
        "potential":(60,99),
    },
}

# Height and weight ranges
HEIGHT_RANGES = {
    "PG": (68, 78),
    "SG": (72, 80),
    "SF": (75, 82),
    "PF": (78, 84),
    "C": (80, 88),
}

WEIGHT_RANGES = {
    "PG": (160, 210),
    "SG": (170, 220),
    "SF": (180, 230),
    "PF": (190, 250),
    "C": (200, 300),
}

FIRST_NAMES = ["John", "Mike", "Chris", "Kevin", "James", "Alex", "David", "Marcus"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]

# ------------------ Player Generator ------------------
def generate_player():
    position = random.choice(list(STAT_RANGES.keys()))
    stats = {stat: random.randint(rng[0], rng[1]) for stat, rng in STAT_RANGES[position].items()}

    # ------------------ Correlated Stats ------------------

    # Physicals affecting finishing
    if stats["vertical"] > 85:
        stats["driving_dunk"] = max(stats["driving_dunk"], stats["vertical"] - 10)
        stats["standing_dunk"] = max(stats["standing_dunk"], stats["vertical"] - 15)

    # Finishing correlations
    if stats["driving_layup"] > 85 or stats["driving_dunk"] > 85:
        stats["close_shot"] = max(stats["close_shot"], max(stats["driving_layup"], stats["driving_dunk"]) - 5)
    if stats["post_moves"] > 85:
        stats["close_shot"] = max(stats["close_shot"], stats["post_moves"] - 5)

    # Shooting correlations
    if stats["mid_range_shot"] > 85:
        stats["free_throw"] = max(stats["free_throw"], stats["mid_range_shot"] - 5)
    if stats["three_point_shot"] > 85:
        stats["free_throw"] = max(stats["free_throw"], stats["three_point_shot"] - 10)

    # Playmaking correlations
    if stats["pass_accuracy"] > 85:
        stats["ball_handle"] = max(stats["ball_handle"], stats["pass_accuracy"] - 10)
    if stats["speed_with_ball"] > 85:
        stats["speed"] = max(stats["speed"], stats["speed_with_ball"] - 5)
        stats["pass_accuracy"] = max(stats["pass_accuracy"], stats["speed_with_ball"] - 10)

    # Defense correlations
    if stats["perimeter_defense"] > 85:
        stats["steal"] = max(stats["steal"], stats["perimeter_defense"] - 10)
    if stats["interior_defense"] > 85:
        stats["block"] = max(stats["block"], stats["interior_defense"] - 10)

    # Rebounding correlations
    if stats["strength"] > 80:
        stats["offensive_rebounding"] = max(stats["offensive_rebounding"], stats["strength"] - 10)
        stats["defensive_rebounding"] = max(stats["defensive_rebounding"], stats["strength"] - 5)
    if stats["offensive_rebounding"] > 80 or stats["defensive_rebounding"] > 80:
        stats["strength"] = max(stats["strength"], stats["offensive_rebounding"] - 10)

    # Speed correlations
    if stats["speed"] > 85:
        stats["speed_with_ball"] = max(stats["speed_with_ball"], stats["speed"] - 5)

    # ------------------ Overall, Height & Weight ------------------
    overall = int(sum(stats.values()) / len(stats))  # avg rating
    height = random.randint(*HEIGHT_RANGES[position])
    weight = random.randint(*WEIGHT_RANGES[position])

    # ------------------ Specialization (Top 3 skill stats) ------------------
    excluded_fields = {"speed", "strength", "vertical", "potential"}
    skill_stats = {k: v for k, v in stats.items() if k not in excluded_fields}
    sorted_stats = sorted(skill_stats.items(), key=lambda x: x[1], reverse=True)
    top_three = [stat for stat, value in sorted_stats[:3]]

    return {
        "name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
        "position": position,
        "overall": overall,
        "height": height,
        "weight": weight,
        "specialization": top_three,
        **stats,
    }
