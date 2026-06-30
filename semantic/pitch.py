ATTACKING_THIRD = "attacking_third"
MIDDLE_THIRD = "middle_third"
DEFENSIVE_THIRD = "defensive_third"

LEFT_CHANNEL = "left"
CENTER_CHANNEL = "center"
RIGHT_CHANNEL = "right"


def pitch_third(x: float) -> str:
    if x < 35:
        return DEFENSIVE_THIRD

    if x < 70:
        return MIDDLE_THIRD

    return ATTACKING_THIRD
