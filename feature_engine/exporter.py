from functools import reduce
from pathlib import Path

import pandas as pd

from feature_engine.specification import FeatureSpec
from feature_engine.sql_generator import generate_feature_sql
from feature_engine.validator import validate_feature_output


def base_match_team_index(con) -> pd.DataFrame:
    dynamic_pairs = con.execute(
        """
        SELECT DISTINCT match_id, team_id
        FROM fact_dynamic_events
        WHERE match_id IS NOT NULL
          AND team_id IS NOT NULL
        """
    ).fetchdf()

    return dynamic_pairs.sort_values(["match_id", "team_id"]).reset_index(drop=True)


def compute_feature(con, spec: FeatureSpec) -> pd.DataFrame:
    sql = generate_feature_sql(spec)
    return con.execute(sql).fetchdf()


def build_feature_frame(con, specs: list[FeatureSpec]) -> pd.DataFrame:
    base = base_match_team_index(con)

    frames = [base]

    for spec in specs:
        feature_df = compute_feature(con, spec)
        frames.append(feature_df)

    df = reduce(
        lambda left, right: left.merge(
            right,
            on=["match_id", "team_id"],
            how="left",
        ),
        frames,
    )

    feature_columns = [spec.output_column for spec in specs]

    for column in feature_columns:
        if column in df.columns:
            df[column] = df[column].fillna(0).astype(int)

    return df


def export_features(
    con,
    specs: list[FeatureSpec],
    output_path: Path,
    validate: bool = True,
) -> pd.DataFrame:
    df = build_feature_frame(con, specs)

    if validate:
        validate_feature_output(df)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    return df
