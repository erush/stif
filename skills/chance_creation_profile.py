from skills.base_profile import BaseProfile


class ChanceCreationProfile(BaseProfile):
    def __init__(self, team_profile):

        super().__init__(
            team_profile,
            "chance_creation",
        )

    def build(self):

        runs = self.category("off_ball_runs")
        penetration = self.category("penetration")
        receiving = self.category("receiving")

        return {
            "support_runs": runs["support_runs"],
            "overlap_runs": runs["overlap_runs"],
            "underlap_runs": runs["underlap_runs"],
            "behind_runs": penetration["behind_runs"],
            "wide_runs": penetration["wide_runs"],
            "half_space_runs": penetration["half_space_runs"],
            "run_ahead_ball": penetration["run_ahead_ball"],
            "coming_short_runs": receiving["coming_short_runs"],
            "cross_receivers": receiving["cross_receivers"],
            "dropping_off_runs": receiving["dropping_off_runs"],
        }


def build_chance_creation_profile(team_profile):

    return ChanceCreationProfile(team_profile).build()
