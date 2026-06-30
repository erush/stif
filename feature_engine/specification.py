from dataclasses import dataclass
from typing import Literal, Sequence


Aggregation = Literal[
    "count",
    "sum",
    "avg",
    "min",
    "max",
    "distinct_count",
]


@dataclass(frozen=True)
class FeatureSpec:
    id: str

    domain: str

    category: str

    output_column: str

    source_table: str

    group_by: Sequence[str]

    aggregation: Aggregation

    source_column: str | None

    filters: dict[str, object]

    description: str

    interpretation: str

    status: str = "planned"


def validate_feature_spec(spec: FeatureSpec) -> None:
    if not spec.id:
        raise ValueError("FeatureSpec.id is required")

    if not spec.domain:
        raise ValueError(f"{spec.id}: domain is required")

    if not spec.category:
        raise ValueError(f"{spec.id}: category is required")

    if not spec.output_column:
        raise ValueError(f"{spec.id}: output_column is required")

    if not spec.source_table:
        raise ValueError(f"{spec.id}: source_table is required")

    if not spec.group_by:
        raise ValueError(f"{spec.id}: group_by is required")

    if spec.aggregation not in {
        "count",
        "sum",
        "avg",
        "min",
        "max",
        "distinct_count",
    }:
        raise ValueError(f"{spec.id}: unsupported aggregation '{spec.aggregation}'")

    if spec.aggregation != "count" and spec.source_column is None:
        raise ValueError(
            f"{spec.id}: source_column is required for aggregation '{spec.aggregation}'"
        )

    if spec.filters is None:
        raise ValueError(f"{spec.id}: filters cannot be None")
