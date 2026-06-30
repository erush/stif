from skills.chance_creation_profile import build_chance_creation_profile
from skills.possession_profile import build_possession_profile
from skills.pressure_profile import build_pressure_profile
from skills.progression_profile import build_progression_profile
from skills.set_piece_profile import build_set_piece_profile
from skills.territory_profile import build_territory_profile
from skills.transition_profile import build_transition_profile


def build_tactical_identity(team_profile):

    territory = build_territory_profile(team_profile)

    progression = build_progression_profile(team_profile)

    transition = build_transition_profile(team_profile)

    possession = build_possession_profile(team_profile)

    pressure = build_pressure_profile(team_profile)

    chance_creation = build_chance_creation_profile(team_profile)

    set_pieces = build_set_piece_profile(team_profile)

    strengths = []

    weaknesses = []

    if pressure["preferred_block"] == "high":
        strengths.append("Aggressive defensive block")

    elif pressure["preferred_block"] == "medium":
        strengths.append("Balanced defensive structure")

    else:
        strengths.append("Deep defensive organization")

    if (
        territory["attacking_third_engagements"]
        > territory["defensive_third_engagements"]
    ):
        strengths.append("Territorial dominance")
    else:
        weaknesses.append("Limited attacking territory")

    if progression["forward_progressions"] > 500:
        strengths.append("Vertical progression")
    else:
        weaknesses.append("Limited forward progression")

    if possession["successful_passes"] > 300:
        strengths.append("Secure possession")
    else:
        weaknesses.append("Inconsistent ball retention")

    if transition["quick_breaks"] > 20:
        strengths.append("Dangerous in transition")
    else:
        weaknesses.append("Limited transition threat")

    if chance_creation["run_ahead_ball"] > 50:
        strengths.append("Strong off-ball penetration")
    else:
        weaknesses.append("Limited attacking movement")

    if set_pieces["goal_for"] > set_pieces["goal_against"]:
        strengths.append("Positive set-piece impact")
    else:
        weaknesses.append("Negative set-piece differential")

    if (
        possession["successful_passes"] > 300
        and progression["forward_progressions"] > 500
    ):
        style = "Possession-Based"

    elif transition["direct_play"] > 100:
        style = "Direct Transition"

    elif pressure["preferred_block"] == "high":
        style = "High Press"

    else:
        style = "Balanced"

    summary = (
        f"{style} team utilizing a "
        f"{pressure['preferred_block']} block with "
        f"{progression['forward_progressions']} forward progressions "
        f"and {territory['attacking_third_engagements']} attacking-third engagements."
    )

    return {
        "style": style,
        "summary": summary,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "territory": territory,
        "progression": progression,
        "transition": transition,
        "possession": possession,
        "pressure": pressure,
        "chance_creation": chance_creation,
        "set_pieces": set_pieces,
    }
