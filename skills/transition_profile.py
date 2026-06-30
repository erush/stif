from skills.base_profile import BaseProfile


class TransitionProfile(BaseProfile):
    def __init__(self, team_profile):

        super().__init__(
            team_profile,
            "transition",
        )

    def build(self):

        attack = self.category("attacking_transition")
        defend = self.category("defensive_transition")
        disruption = self.category("disruption")
        progression = self.category("progression")

        return {
            "attacking_transitions": attack["transition_attacking_transitions"],
            "direct_play": attack["transition_direct_play"],
            "quick_breaks": attack["transition_quick_breaks"],
            "defending_direct": defend["transition_defending_direct"],
            "defending_transition": defend["transition_defending_transition"],
            "defending_quick_break": defend["transition_defending_quick_break"],
            "chaotic": disruption["transition_chaotic"],
            "disruptions": disruption["transition_disruption"],
            "forward_progressions": progression["transition_forward_progressions"],
            "line_breaks": progression["transition_line_breaks"],
        }


def build_transition_profile(team_profile):

    return TransitionProfile(team_profile).build()
