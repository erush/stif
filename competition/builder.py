from competition.base import CompetitionBase
from competition.territory import TerritoryBuilder


PROGRESSION_SQL = """
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
"""


TRANSITION_SQL = """
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
"""


POSSESSION_SQL = """
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
"""


PRESSURE_SQL = """
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
"""


CHANCE_CREATION_SQL = """
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
"""


class CompetitionFeatureBuilder(CompetitionBase):
    def build(self):
        self.create_event_base()

        df = self.base_index()

        territory = TerritoryBuilder()
        territory.con = self.con

        queries = territory.queries() + [
            PROGRESSION_SQL,
            TRANSITION_SQL,
            POSSESSION_SQL,
            PRESSURE_SQL,
            CHANCE_CREATION_SQL,
        ]

        for query in queries:
            df = self.merge_feature(df, query)

        df = self.finalize(df)

        self.publish(df)

        return df
