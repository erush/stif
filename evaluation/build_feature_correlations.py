import pandas as pd

from evaluation.utils import (
    load_features,
    feature_columns,
    OUTPUTS_DIR,
    ensure_outputs_dir,
)


def build_feature_correlations(threshold: float = 0.95) -> pd.DataFrame:
    ensure_outputs_dir()

    df = load_features()
    cols = feature_columns(df)

    corr = df[cols].corr(numeric_only=True)
    corr.to_csv(OUTPUTS_DIR / "feature_correlations.csv")

    rows = []

    for i, col_a in enumerate(cols):
        for col_b in cols[i + 1 :]:
            value = corr.loc[col_a, col_b]

            if pd.notna(value) and abs(value) >= threshold:
                rows.append(
                    {
                        "feature_a": col_a,
                        "feature_b": col_b,
                        "correlation": float(value),
                    }
                )

    high_corr = (
        pd.DataFrame(rows).sort_values(
            "correlation",
            key=lambda s: s.abs(),
            ascending=False,
        )
        if rows
        else pd.DataFrame(columns=["feature_a", "feature_b", "correlation"])
    )

    high_corr.to_csv(OUTPUTS_DIR / "high_correlations.csv", index=False)

    return high_corr


def main() -> None:
    high_corr = build_feature_correlations()
    print(high_corr.head(20))
    print(f"High-correlation pairs: {len(high_corr)}")


if __name__ == "__main__":
    main()
