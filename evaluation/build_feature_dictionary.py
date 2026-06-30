from collections import defaultdict

from registry.all_features import FEATURE_SPECS
from evaluation.utils import OUTPUTS_DIR, ensure_outputs_dir


def build_feature_dictionary() -> None:
    ensure_outputs_dir()

    by_domain = defaultdict(lambda: defaultdict(list))

    for spec in FEATURE_SPECS:
        by_domain[spec.domain][spec.category].append(spec)

    lines = ["# STIF Feature Dictionary", ""]

    for domain in sorted(by_domain):
        lines.append(f"# {domain.replace('_', ' ').title()}")
        lines.append("")

        for category in sorted(by_domain[domain]):
            lines.append(f"## {category.replace('_', ' ').title()}")
            lines.append("")

            for spec in sorted(
                by_domain[domain][category], key=lambda s: s.output_column
            ):
                lines.append(f"### `{spec.output_column}`")
                lines.append("")
                lines.append(f"- ID: `{spec.id}`")
                lines.append(f"- Domain: `{spec.domain}`")
                lines.append(f"- Category: `{spec.category}`")
                lines.append(f"- Source table: `{spec.source_table}`")
                lines.append(f"- Aggregation: `{spec.aggregation}`")
                lines.append(f"- Filters: `{spec.filters}`")
                lines.append("")
                lines.append(spec.description)
                lines.append("")
                lines.append(f"Interpretation: {spec.interpretation}")
                lines.append("")

    (OUTPUTS_DIR / "feature_dictionary.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    build_feature_dictionary()
    print("Wrote outputs/feature_dictionary.md")


if __name__ == "__main__":
    main()
