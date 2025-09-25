import random

# ------------------ Position-specific stat ranges ------------------
STAT_RANGES = {
    "PG": {
        # Finishing
        "close_shot": (30, 85),
        "driving_layup": (40, 95),
        "driving_dunk": (30, 75),
        "standing_dunk": (25, 60),
        "post_moves": (25, 60),

        # Shooting
        "mid_range_shot": (35, 95),
        "three_point_shot": (35, 99),
        "free_throw": (50, 99),

        # Playmaking
        "pass_accuracy": (45, 99),
        "ball_handle": (45, 99),
        "speed_with_ball": (75, 99),

        # Defense
        "interior_defense": (30, 60),
        "perimeter_defense": (30, 95),
        "steal": (35, 95),
        "block": (25, 55),

        # Rebounding
        "offensive_rebounding": (25, 55),
        "defensive_rebounding": (35, 65),

        # Physicals
        "speed": (70, 99),
        "strength": (20, 65),
        "vertical": (30, 95),
        "potential":(60,99),
    },
    "SG": {
        "close_shot": (30, 85),
        "driving_layup": (30, 95),
        "driving_dunk": (30, 95),
        "standing_dunk": (30, 70),
        "post_moves": (30, 65),

        "mid_range_shot": (35, 95),
        "three_point_shot": (30, 99),
        "free_throw": (50, 99),

        "pass_accuracy": (30, 85),
        "ball_handle": (70, 95),
        "speed_with_ball": (70, 95),

        "interior_defense": (40, 70),
        "perimeter_defense": (65, 90),
        "steal": (60, 90),
        "block": (30, 65),

        "offensive_rebounding": (30, 60),
        "defensive_rebounding": (40, 70),

        "speed": (75, 95),
        "strength": (50, 70),
        "vertical": (70, 95),
        "potential":(60,99),
    },
    "SF": {
        "close_shot": (70, 90),
        "driving_layup": (65, 90),
        "driving_dunk": (60, 99),
        "standing_dunk": (50, 85),
        "post_moves": (50, 85),

        "mid_range_shot": (60, 90),
        "three_point_shot": (60, 90),
        "free_throw": (65, 95),

        "pass_accuracy": (55, 80),
        "ball_handle": (60, 85),
        "speed_with_ball": (60, 85),

        "interior_defense": (55, 85),
        "perimeter_defense": (55, 85),
        "steal": (50, 80),
        "block": (40, 75),

        "offensive_rebounding": (50, 75),
        "defensive_rebounding": (55, 85),

        "speed": (65, 85),
        "strength": (55, 80),
        "vertical": (65, 90),
        "potential":(60,99),
    },
    "PF": {
        "close_shot": (75, 95),
        "driving_layup": (55, 85),
        "driving_dunk": (70, 99),
        "standing_dunk": (70, 99),
        "post_moves": (70, 95),

        "mid_range_shot": (55, 85),
        "three_point_shot": (40, 80),
        "free_throw": (60, 85),

        "pass_accuracy": (45, 75),
        "ball_handle": (45, 75),
        "speed_with_ball": (45, 70),

        "interior_defense": (70, 95),
        "perimeter_defense": (50, 75),
        "steal": (40, 70),
        "block": (55, 90),

        "offensive_rebounding": (70, 95),
        "defensive_rebounding": (70, 95),

        "speed": (55, 75),
        "strength": (70, 95),
        "vertical": (60, 85),
        "potential":(60,99),
    },
    "C": {
        "close_shot": (80, 99),
        "driving_layup": (45, 75),
        "driving_dunk": (75, 99),
        "standing_dunk": (80, 99),
        "post_moves": (75, 99),

        "mid_range_shot": (40, 75),
        "three_point_shot": (25, 65),
        "free_throw": (50, 75),

        "pass_accuracy": (35, 65),
        "ball_handle": (30, 60),
        "speed_with_ball": (30, 60),

        "interior_defense": (75, 99),
        "perimeter_defense": (40, 65),
        "steal": (35, 65),
        "block": (70, 99),

        "offensive_rebounding": (80, 99),
        "defensive_rebounding": (80, 99),

        "speed": (40, 70),
        "strength": (80, 99),
        "vertical": (55, 85),
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
    overall = int(sum(stats.values()) / len(stats))  # avg rating
    height = random.randint(*HEIGHT_RANGES[position])
    weight = random.randint(*WEIGHT_RANGES[position])

    # ---- NEW: Specialization ----
    # Find top 3 stats
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
