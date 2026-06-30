from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Domain:
    id: str
    name: str
    description: str
    sql_files: tuple[str, ...]


DOMAIN_REGISTRY = (
    Domain(
        id="territory",
        name="Territory Control",
        description="Measures where teams operate, recover, and sustain activity on the pitch.",
        sql_files=("100_territory.sql", "101_territory_views.sql"),
    ),
    Domain(
        id="progression",
        name="Ball Progression",
        description="Measures how teams move the ball through space and advance into dangerous areas.",
        sql_files=("110_progression.sql", "111_progression_views.sql"),
    ),
    Domain(
        id="transition",
        name="Transition Play",
        description="Measures attacking and defensive behavior immediately after possession changes.",
        sql_files=("120_transition.sql", "121_transition_views.sql"),
    ),
    Domain(
        id="possession",
        name="Possession Structure",
        description="Measures buildup, circulation, resets, and sustained possession behavior.",
        sql_files=("130_possession.sql", "131_possession_views.sql"),
    ),
    Domain(
        id="pressure",
        name="Defensive Pressure",
        description="Measures pressing, disruption, recoveries, and defensive engagement.",
        sql_files=("140_pressure.sql", "141_pressure_views.sql"),
    ),
    Domain(
        id="chance_creation",
        name="Chance Creation",
        description="Measures final-third entries, box activity, and attacking construction.",
        sql_files=("150_chance_creation.sql", "151_chance_creation_views.sql"),
    ),
    Domain(
        id="set_pieces",
        name="Set Piece Organization",
        description="Measures corners, free kicks, throw-ins, and restart-based attacking behavior.",
        sql_files=("160_set_pieces.sql", "161_set_pieces_views.sql"),
    ),
)


def domain_ids() -> list[str]:
    return [domain.id for domain in DOMAIN_REGISTRY]


def domain_by_id(domain_id: str) -> Domain:
    for domain in DOMAIN_REGISTRY:
        if domain.id == domain_id:
            return domain

    raise KeyError(f"Unknown domain: {domain_id}")


def sql_paths(sql_root: Path, domain_id: str) -> list[Path]:
    domain = domain_by_id(domain_id)
    return [sql_root / sql_file for sql_file in domain.sql_files]
