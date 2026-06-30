from registry.feature_lookup import DOMAIN_FEATURES
from services.feature_service import FeatureService


class ProfileService:
    def __init__(self):
        self.features = FeatureService()

    def build_team_profile(self, match_id: int, team_id: int) -> dict:
        row = self.features.team(match_id, team_id)

        profile = {
            "match_id": match_id,
            "team_id": team_id,
            "domains": {},
        }

        for domain, specs in DOMAIN_FEATURES.items():
            profile["domains"][domain] = {"categories": {}}

            for spec in specs:
                category = spec.category

                if category not in profile["domains"][domain]["categories"]:
                    profile["domains"][domain]["categories"][category] = {}

                profile["domains"][domain]["categories"][category][
                    spec.output_column
                ] = row[spec.output_column]

        return profile

    def build_match_profiles(self, match_id: int) -> list[dict]:
        rows = self.features.match(match_id)

        return [
            self.build_team_profile(
                int(row.match_id),
                int(row.team_id),
            )
            for _, row in rows.iterrows()
        ]

    def compare_profiles(self, profile_a: dict, profile_b: dict) -> dict:
        comparison = {}

        for domain in DOMAIN_FEATURES:
            comparison[domain] = {}

            categories_a = profile_a["domains"][domain]["categories"]
            categories_b = profile_b["domains"][domain]["categories"]

            for category in categories_a:
                comparison[domain][category] = {}

                for feature in categories_a[category]:
                    a_value = categories_a[category][feature]
                    b_value = categories_b[category][feature]

                    comparison[domain][category][feature] = {
                        "team_a": a_value,
                        "team_b": b_value,
                        "difference": a_value - b_value,
                    }

        return comparison
