from pathlib import Path

import duckdb
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "warehouse" / "soccer.duckdb"
OUTPUTS = PROJECT_ROOT / "outputs"


class CompetitionBase:
    def __init__(self):
        self.con = duckdb.connect(DATABASE)

    def close(self) -> None:
        self.con.close()

    def create_event_base(self) -> None:
        self.con.execute(
            """
            CREATE OR REPLACE TEMP VIEW competition_event_base AS
            WITH raw AS (
                SELECT
                    *,
                    ROW_NUMBER() OVER () AS event_order,
                    TRY_CAST(SPLIT_PART(time_start, ':', 1) AS DOUBLE) * 60
                        + TRY_CAST(SPLIT_PART(time_start, ':', 2) AS DOUBLE) AS event_seconds
                FROM fact_dynamic_events
            )
            SELECT
                *,
                COALESCE(
                    CAST(associated_player_possession_event_id AS VARCHAR),
                    CAST(event_id AS VARCHAR),
                    CAST(match_id AS VARCHAR) || '_' || CAST(team_id AS VARCHAR) || '_' || CAST(event_order AS VARCHAR)
                ) AS possession_key
            FROM raw
            WHERE match_id IS NOT NULL
              AND team_id IS NOT NULL
            """
        )

    def base_index(self) -> pd.DataFrame:
        return self.con.execute(
            """
            SELECT DISTINCT match_id, team_id
            FROM fact_dynamic_events
            WHERE match_id IS NOT NULL
              AND team_id IS NOT NULL
            ORDER BY match_id, team_id
            """
        ).df()

    def feature(self, sql: str) -> pd.DataFrame:
        return self.con.execute(sql).df()

    def merge_feature(self, df: pd.DataFrame, sql: str) -> pd.DataFrame:
        return df.merge(
            self.feature(sql),
            on=["match_id", "team_id"],
            how="left",
        )

    def finalize(self, df: pd.DataFrame) -> pd.DataFrame:
        feature_cols = [c for c in df.columns if c not in {"match_id", "team_id"}]
        df[feature_cols] = df[feature_cols].fillna(0).astype(int)
        return df

    def publish(self, df: pd.DataFrame) -> None:
        self.con.register("competition_features_df", df)

        self.con.execute(
            """
            CREATE OR REPLACE TABLE analytics_competition_features AS
            SELECT *
            FROM competition_features_df
            """
        )

        OUTPUTS.mkdir(parents=True, exist_ok=True)

        df.to_csv(
            OUTPUTS / "competition_features.csv",
            index=False,
        )
