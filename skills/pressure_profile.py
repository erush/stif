from skills.base_profile import BaseProfile


class PressureProfile(BaseProfile):
    def __init__(self, team_profile):

        super().__init__(
            team_profile,
            "pressure",
        )

    def build(self):

        pressing = self.category("pressing")

        counter = self.category("counter_press")

        recovery = self.category("recovery")

        outcomes = self.category("pressing_outcomes")

        structure = self.category("defensive_structure")

        field = self.category("field_pressure")

        profile = {
            "total_pressure_events": pressing["pressure_events"],
            "pressing_events": pressing["pressing_events"],
            "counter_press_events": counter["counter_press_events"],
            "recovery_press_events": recovery["recovery_press_events"],
            "pressure_regains": outcomes["pressure_regains"],
            "pressure_disruptions": outcomes["pressure_disruptions"],
            "attacking_third_pressing": field["attacking_third_pressing"],
            "high_block": structure["high_block_pressure"],
            "medium_block": structure["medium_block_pressure"],
            "low_block": structure["low_block_pressure"],
        }

        profile["preferred_block"] = max(
            {
                "high": profile["high_block"],
                "medium": profile["medium_block"],
                "low": profile["low_block"],
            },
            key=lambda k: {
                "high": profile["high_block"],
                "medium": profile["medium_block"],
                "low": profile["low_block"],
            }[k],
        )

        return profile


def build_pressure_profile(team_profile):

    return PressureProfile(team_profile).build()
