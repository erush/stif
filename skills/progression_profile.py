from skills.base_profile import BaseProfile


class ProgressionProfile(BaseProfile):
    def __init__(self, team_profile):

        super().__init__(
            team_profile,
            "progression",
        )

    def build(self):

        line_breaks = self.category("line_breaks")
        trajectory = self.category("trajectory")

        return {
            "forward_progressions": trajectory["progression_forward_trajectories"],
            "first_line_breaks": line_breaks["progression_first_line_breaks"],
            "second_line_breaks": line_breaks["progression_second_line_breaks"],
            "last_line_breaks": line_breaks["progression_last_line_breaks"],
            "first_around": line_breaks["progression_first_line_break_around"],
            "first_through": line_breaks["progression_first_line_break_through"],
            "second_around": line_breaks["progression_second_line_break_around"],
            "second_through": line_breaks["progression_second_line_break_through"],
            "last_around": line_breaks["progression_last_line_break_around"],
            "last_through": line_breaks["progression_last_line_break_through"],
        }


def build_progression_profile(team_profile):

    return ProgressionProfile(team_profile).build()
