from collections import defaultdict
from pathlib import Path

from feature_engine.specification import FeatureSpec


def generate_feature_catalog_markdown(specs: list[FeatureSpec]) -> str:

    by_domain = defaultdict(lambda: defaultdict(list))

    for spec in specs:
        by_domain[spec.domain][spec.category].append(spec)

    lines = ["# STIF Tactical Feature Catalog", ""]

    for domain in sorted(by_domain):
        lines.append(f"# {domain.replace('_', ' ').title()}")

        lines.append("")

        for category in sorted(by_domain[domain]):
            lines.append(f"## {category.replace('_', ' ').title()}")

            lines.append("")

            for spec in sorted(
                by_domain[domain][category],
                key=lambda s: s.output_column,
            ):
                lines.append(f"### {spec.output_column}")

                lines.append("")

                lines.append(f"- **ID:** `{spec.id}`")

                lines.append(f"- **Source Table:** `{spec.source_table}`")

                lines.append(f"- **Aggregation:** `{spec.aggregation}`")

                if spec.source_column:
                    lines.append(f"- **Source Column:** `{spec.source_column}`")

                lines.append(f"- **Filters:** `{spec.filters}`")

                lines.append(f"- **Status:** `{spec.status}`")

                lines.append("")

                lines.append("**Description**")

                lines.append("")

                lines.append(spec.description)

                lines.append("")

                lines.append("**Interpretation**")

                lines.append("")

                lines.append(spec.interpretation)

                lines.append("")

    return "\n".join(lines)


def write_feature_catalog(specs: list[FeatureSpec], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        generate_feature_catalog_markdown(specs),
        encoding="utf-8",
    )


def generate_writeup_feature_section(specs: list[FeatureSpec]) -> str:
    lines = ["# Feature Definitions", ""]

    for spec in specs:
        lines.append(f"## {spec.output_column}")
        lines.append("")
        lines.append(spec.description)
        lines.append("")
        lines.append("Interpretation:")
        lines.append("")
        lines.append(spec.interpretation)
        lines.append("")
        lines.append("Computation:")
        lines.append("")
        lines.append(
            f"Grouped by `{', '.join(spec.group_by)}` from `{spec.source_table}` "
            f"using `{spec.aggregation}` with filters `{spec.filters}`."
        )
        lines.append("")

    return "\n".join(lines)
