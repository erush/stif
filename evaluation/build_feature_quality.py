import pandas as pd

from evaluation.build_feature_profile import build_feature_profile
from evaluation.build_feature_correlations import build_feature_correlations
from evaluation.utils import OUTPUTS_DIR, ensure_outputs_dir


def build_feature_quality() -> None:
    ensure_outputs_dir()

    profile = build_feature_profile()
    high_corr = build_feature_correlations()

    constant = profile[profile["constant"]]
    sparse = profile[profile["zero_pct"] >= 0.90]
    low_variance = profile[profile["distinct_count"] <= 2]

    lines = ["# STIF Feature Quality Report", ""]

    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total features: {len(profile)}")
    lines.append(f"- Constant features: {len(constant)}")
    lines.append(f"- Sparse features (>=90% zero): {len(sparse)}")
    lines.append(f"- Low-cardinality features (<=2 distinct): {len(low_variance)}")
    lines.append(f"- Highly correlated pairs: {len(high_corr)}")
    lines.append("")

    lines.append("## Constant Features")
    lines.append("")
    lines.append(
        constant[["feature", "distinct_count"]].to_markdown(index=False)
        if len(constant)
        else "None"
    )
    lines.append("")

    lines.append("## Sparse Features")
    lines.append("")
    lines.append(
        sparse[["feature", "zero_pct", "mean", "max"]].to_markdown(index=False)
        if len(sparse)
        else "None"
    )
    lines.append("")

    lines.append("## Highly Correlated Feature Pairs")
    lines.append("")
    lines.append(high_corr.to_markdown(index=False) if len(high_corr) else "None")
    lines.append("")

    (OUTPUTS_DIR / "feature_quality.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )


def main() -> None:
    build_feature_quality()
    print("Wrote outputs/feature_quality.md")


if __name__ == "__main__":
    main()
