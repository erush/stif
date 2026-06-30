from pathlib import Path

import duckdb
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATABASE = PROJECT_ROOT / "warehouse" / "soccer.duckdb"
OUTPUTS = PROJECT_ROOT / "outputs"


def base_index(con) -> pd.DataFrame:
    return con.execute(
        """
        SELECT DISTINCT match_id, team_id
        FROM fact_dynamic_events
        WHERE match_id IS NOT NULL
          AND team_id IS NOT NULL
        ORDER BY match_id, team_id
        """
    ).df()


def create_event_base(con) -> None:
    con.execute(
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


def feature(con, sql: str) -> pd.DataFrame:
    return con.execute(sql).df()


def build_competition_features() -> pd.DataFrame:
    con = duckdb.connect(DATABASE)

    create_event_base(con)

    df = base_index(con)

    feature_queries = [
        """
        WITH ordered AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                third_end,
                CASE
                    WHEN third_end = 'attacking_third'
                     AND LAG(third_end) OVER (
                        PARTITION BY match_id, team_id, possession_key
                        ORDER BY event_seconds, event_order
                     ) = 'attacking_third'
                    THEN 1 ELSE 0
                END AS persistent_event
            FROM competition_event_base
            WHERE event_type IN ('on_ball_engagement', 'player_possession')
        )
        SELECT
            match_id,
            team_id,
            SUM(persistent_event) AS territorial_persistence_events
        FROM ordered
        GROUP BY match_id, team_id
        """,
        """
        WITH possession_summary AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                MAX(CASE WHEN third_start = 'defensive_third' OR third_end = 'defensive_third' THEN 1 ELSE 0 END) AS touched_defensive_third,
                MAX(CASE WHEN third_start = 'attacking_third' OR third_end = 'attacking_third' THEN 1 ELSE 0 END) AS touched_attacking_third
            FROM competition_event_base
            GROUP BY match_id, team_id, possession_key
        )
        SELECT
            match_id,
            team_id,
            COUNT(*) AS deep_territory_progressions
        FROM possession_summary
        WHERE touched_defensive_third = 1
          AND touched_attacking_third = 1
        GROUP BY match_id, team_id
        """,
        """
        WITH possession_summary AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                MAX(CASE WHEN first_line_break_type IN ('through', 'around') THEN 1 ELSE 0 END) AS broke_first_line,
                MAX(CASE WHEN second_last_line_break_type IN ('through', 'around') THEN 1 ELSE 0 END) AS broke_second_line,
                MAX(CASE WHEN last_line_break_type IN ('through', 'around') THEN 1 ELSE 0 END) AS broke_last_line
            FROM competition_event_base
            GROUP BY match_id, team_id, possession_key
        )
        SELECT
            match_id,
            team_id,
            COUNT(*) AS multi_line_progressions
        FROM possession_summary
        WHERE broke_first_line = 1
          AND broke_second_line = 1
          AND broke_last_line = 1
        GROUP BY match_id, team_id
        """,
        """
        WITH possession_summary AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                MAX(CASE WHEN team_in_possession_phase_type IN ('transition', 'quick_break', 'direct') THEN 1 ELSE 0 END) AS transition_phase,
                MAX(CASE WHEN third_start = 'defensive_third' OR third_end = 'defensive_third' THEN 1 ELSE 0 END) AS touched_defensive_third,
                MAX(CASE WHEN third_start = 'attacking_third' OR third_end = 'attacking_third' THEN 1 ELSE 0 END) AS touched_attacking_third
            FROM competition_event_base
            GROUP BY match_id, team_id, possession_key
        )
        SELECT
            match_id,
            team_id,
            COUNT(*) AS transition_burst_possessions
        FROM possession_summary
        WHERE transition_phase = 1
          AND touched_defensive_third = 1
          AND touched_attacking_third = 1
        GROUP BY match_id, team_id
        """,
        """
        WITH possession_summary AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                MAX(CASE WHEN team_in_possession_phase_type = 'build_up' THEN 1 ELSE 0 END) AS has_build_up,
                MAX(CASE WHEN team_in_possession_phase_type = 'create' THEN 1 ELSE 0 END) AS has_create,
                MAX(CASE WHEN team_in_possession_phase_type IN ('chaotic', 'disruption') THEN 1 ELSE 0 END) AS has_instability
            FROM competition_event_base
            GROUP BY match_id, team_id, possession_key
        )
        SELECT
            match_id,
            team_id,
            COUNT(*) AS stable_build_up_sequences
        FROM possession_summary
        WHERE has_build_up = 1
          AND has_create = 1
          AND has_instability = 0
        GROUP BY match_id, team_id
        """,
        """
        WITH flagged AS (
            SELECT
                match_id,
                team_id,
                event_seconds,
                event_order,
                CASE
                    WHEN event_subtype IN ('pressure', 'pressing', 'counter_press', 'recovery_press')
                    THEN 1 ELSE 0
                END AS pressure_flag
            FROM competition_event_base
        ),
        waves AS (
            SELECT
                *,
                SUM(CASE WHEN pressure_flag = 0 THEN 1 ELSE 0 END)
                    OVER (
                        PARTITION BY match_id, team_id
                        ORDER BY event_seconds, event_order
                    ) AS wave_id
            FROM flagged
        ),
        wave_lengths AS (
            SELECT
                match_id,
                team_id,
                wave_id,
                COUNT(*) AS wave_events
            FROM waves
            WHERE pressure_flag = 1
            GROUP BY match_id, team_id, wave_id
        )
        SELECT
            match_id,
            team_id,
            SUM(wave_events) AS pressing_wave_events
        FROM wave_lengths
        WHERE wave_events >= 2
        GROUP BY match_id, team_id
        """,
        """
        WITH possession_summary AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                COUNT(DISTINCT associated_off_ball_run_subtype) AS run_type_count
            FROM competition_event_base
            WHERE associated_off_ball_run_subtype IS NOT NULL
            GROUP BY match_id, team_id, possession_key
        )
        SELECT
            match_id,
            team_id,
            COUNT(*) AS penetration_diversity_possessions
        FROM possession_summary
        WHERE run_type_count >= 3
        GROUP BY match_id, team_id
        """,
    ]

    for query in feature_queries:
        df = df.merge(
            feature(con, query),
            on=["match_id", "team_id"],
            how="left",
        )

    feature_cols = [c for c in df.columns if c not in {"match_id", "team_id"}]
    df[feature_cols] = df[feature_cols].fillna(0).astype(int)

    con.register("competition_features_df", df)

    con.execute(
        """
        CREATE OR REPLACE TABLE analytics_competition_features AS
        SELECT *
        FROM competition_features_df
        """
    )

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUTS / "competition_features.csv", index=False)

    con.close()

    return df


def main() -> None:
    df = build_competition_features()
    print(df.head())
    print(f"{len(df)} rows exported.")
    print("Wrote analytics_competition_features")
    print("Wrote outputs/competition_features.csv")


if __name__ == "__main__":
    main()
