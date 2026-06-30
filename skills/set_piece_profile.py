from skills.base_profile import BaseProfile


class SetPieceProfile(BaseProfile):
    def __init__(self, team_profile):

        super().__init__(
            team_profile,
            "set_pieces",
        )

    def build(self):

        corners = self.category("corners")
        free_kicks = self.category("free_kicks")
        goal_kicks = self.category("goal_kicks")
        throw_ins = self.category("throw_ins")
        goals = self.category("goals")

        return {
            "corner_for": corners["corner_for"],
            "corner_against": corners["corner_against"],
            "free_kick_for": free_kicks["free_kick_for"],
            "free_kick_against": free_kicks["free_kick_against"],
            "goal_kick_for": goal_kicks["goal_kick_for"],
            "goal_kick_against": goal_kicks["goal_kick_against"],
            "throw_in_for": throw_ins["throw_in_for"],
            "throw_in_against": throw_ins["throw_in_against"],
            "goal_for": goals["goal_for"],
            "goal_against": goals["goal_against"],
        }


def build_set_piece_profile(team_profile):

    return SetPieceProfile(team_profile).build()
