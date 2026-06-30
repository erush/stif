from collections import Counter

from registry.all_features import FEATURE_SPECS
from evaluation.build_feature_profile import build_feature_profile
from evaluation.build_feature_correlations import build_feature_correlations
from evaluation.build_feature_dictionary import build_feature_dictionary
from evaluation.build_feature_quality import build_feature_quality
from evaluation.utils import OUTPUTS_DIR, ensure_outputs_dir


def build_feature_report() -> None:
    ensure_outputs_dir()

    profile = build_feature_profile()
    high_corr = build_feature_correlations()
    build_feature_dictionary()
    build_feature_quality()

    domain_counts = Counter(spec.domain for spec in FEATURE_SPECS)
    category_counts = Counter((spec.domain, spec.category) for spec in FEATURE_SPECS)

    lines = ["# STIF Feature Evaluation Report", ""]

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total FeatureSpecs: {len(FEATURE_SPECS)}")
    lines.append(f"- Exported features profiled: {len(profile)}")
    lines.append(f"- Highly correlated pairs: {len(high_corr)}")
    lines.append(f"- Constant features: {int(profile['constant'].sum())}")
    lines.append(
        f"- Sparse features >=90% zero: {int((profile['zero_pct'] >= 0.90).sum())}"
    )
    lines.append("")

    lines.append("## Domain Coverage")
    lines.append("")
    for domain, count in sorted(domain_counts.items()):
        lines.append(f"- {domain}: {count}")
    lines.append("")

    lines.append("## Category Coverage")
    lines.append("")
    for (domain, category), count in sorted(category_counts.items()):
        lines.append(f"- {domain} / {category}: {count}")
    lines.append("")

    lines.append("## Generated Artifacts")
    lines.append("")
    lines.append("- `outputs/features.csv`")
    lines.append("- `outputs/feature_profile.csv`")
    lines.append("- `outputs/feature_profile.md`")
    lines.append("- `outputs/feature_correlations.csv`")
    lines.append("- `outputs/high_correlations.csv`")
    lines.append("- `outputs/feature_dictionary.md`")
    lines.append("- `outputs/feature_quality.md`")
    lines.append("")

    (OUTPUTS_DIR / "stif_report.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    build_feature_report()
    print("Wrote outputs/stif_report.md")


if __name__ == "__main__":
    main()
