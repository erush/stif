from skills.base_profile import BaseProfile


class TerritoryProfile(BaseProfile):
    def __init__(self, team_profile):

        super().__init__(
            team_profile,
            "territory",
        )

    def build(self):

        territory = self.category("territorial_control")
        channels = self.category("channels")
        possession = self.category("possession")

        return {
            "attacking_third_engagements": territory[
                "territory_attacking_third_engagements"
            ],
            "middle_third_engagements": territory["territory_middle_third_engagements"],
            "defensive_third_engagements": territory[
                "territory_defensive_third_engagements"
            ],
            "center_channel": channels["territory_center_channel_engagements"],
            "left_half_space": channels["territory_left_half_space_engagements"],
            "right_half_space": channels["territory_right_half_space_engagements"],
            "left_wide": channels["territory_left_wide_engagements"],
            "right_wide": channels["territory_right_wide_engagements"],
            "attacking_possessions": possession[
                "territory_attacking_third_possessions"
            ],
            "middle_possessions": possession["territory_middle_third_possessions"],
        }


def build_territory_profile(team_profile):

    return TerritoryProfile(team_profile).build()
