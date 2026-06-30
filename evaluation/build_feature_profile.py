import pandas as pd

from evaluation.utils import (
    load_features,
    feature_columns,
    OUTPUTS_DIR,
    ensure_outputs_dir,
)


def build_feature_profile() -> pd.DataFrame:
    ensure_outputs_dir()

    df = load_features()
    rows = []

    for col in feature_columns(df):
        s = df[col]

        rows.append(
            {
                "feature": col,
                "dtype": str(s.dtype),
                "null_count": int(s.isna().sum()),
                "null_pct": float(s.isna().mean()),
                "zero_count": int((s == 0).sum()),
                "zero_pct": float((s == 0).mean()),
                "distinct_count": int(s.nunique(dropna=True)),
                "min": float(s.min()),
                "max": float(s.max()),
                "mean": float(s.mean()),
                "median": float(s.median()),
                "std": float(s.std()) if pd.notna(s.std()) else 0.0,
                "constant": bool(s.nunique(dropna=True) <= 1),
                "binary": bool(set(s.dropna().unique()).issubset({0, 1})),
            }
        )

    profile = pd.DataFrame(rows)
    profile.to_csv(OUTPUTS_DIR / "feature_profile.csv", index=False)

    markdown = ["# STIF Feature Profile", ""]
    markdown.append(profile.to_markdown(index=False))
    markdown.append("")

    (OUTPUTS_DIR / "feature_profile.md").write_text(
        "\n".join(markdown),
        encoding="utf-8",
    )

    return profile


def main() -> None:
    profile = build_feature_profile()
    print(profile.head())
    print(f"Profiled {len(profile)} features.")


if __name__ == "__main__":
    main()
