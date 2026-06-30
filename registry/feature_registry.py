from dataclasses import dataclass


@dataclass(frozen=True)
class Feature:
    id: str
    column: str
    domain: str
    name: str
    description: str
    interpretation: str
    source_table: str
    status: str = "planned"


FEATURE_REGISTRY = (
    Feature(
        id="territory_attacking_third_engagements",
        column="territory_attacking_third_engagements",
        domain="territory",
        name="Attacking Third Engagements",
        description="Counts team on-ball engagements ending in the attacking third.",
        interpretation="Higher values indicate greater territorial presence in advanced areas.",
        source_table="analytics_territory",
    ),
    Feature(
        id="territory_middle_third_engagements",
        column="territory_middle_third_engagements",
        domain="territory",
        name="Middle Third Engagements",
        description="Counts team on-ball engagements ending in the middle third.",
        interpretation="Higher values indicate more sustained midfield involvement and buildup activity.",
        source_table="analytics_territory",
    ),
    Feature(
        id="territory_defensive_third_engagements",
        column="territory_defensive_third_engagements",
        domain="territory",
        name="Defensive Third Engagements",
        description="Counts team on-ball engagements ending in the defensive third.",
        interpretation="Higher values indicate more activity close to a team's own goal.",
        source_table="analytics_territory",
    ),
)


def features_by_domain(domain: str) -> list[Feature]:
    return [feature for feature in FEATURE_REGISTRY if feature.domain == domain]


def feature_columns() -> list[str]:
    return [feature.column for feature in FEATURE_REGISTRY]


def feature_by_id(feature_id: str) -> Feature:
    for feature in FEATURE_REGISTRY:
        if feature.id == feature_id:
            return feature

    raise KeyError(f"Unknown feature: {feature_id}")
