from skills.base_profile import BaseProfile


class PossessionProfile(BaseProfile):
    def __init__(self, team_profile):

        super().__init__(
            team_profile,
            "possession",
        )

    def build(self):

        phase = self.category("phase")
        passing = self.category("passing")
        territory = self.category("territory")
        progression = self.category("progression")

        return {
            "build_up_possessions": phase["build_up_possessions"],
            "create_phase_possessions": phase["create_phase_possessions"],
            "finish_phase_possessions": phase["finish_phase_possessions"],
            "set_play_possessions": phase["set_play_possessions"],
            "successful_passes": passing["successful_passes"],
            "forward_passes": passing["forward_passes"],
            "long_passes": passing["long_passes"],
            "build_up_middle_third": territory["build_up_middle_third"],
            "build_up_attacking_third": territory["build_up_attacking_third"],
            "build_up_progressions": progression["build_up_forward_progressions"],
        }


def build_possession_profile(team_profile):

    return PossessionProfile(team_profile).build()
