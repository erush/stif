from typing import Any


class BaseProfile:
    def __init__(
        self,
        team_profile: dict,
        domain: str,
    ):

        self.team_profile = team_profile

        self.domain = domain

        self.categories = team_profile["domains"][domain]["categories"]

    def category(self, name: str) -> dict[str, Any]:

        return self.categories.get(name, {})

    def build(self) -> dict[str, Any]:

        raise NotImplementedError
