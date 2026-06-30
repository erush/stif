from competition.base import CompetitionBase


class TerritoryBuilder(CompetitionBase):
    def territorial_persistence(self) -> str:
        return """
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
        """

    def territory_switches(self) -> str:
        return """
        WITH ordered AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                channel_end,
                LAG(channel_end) OVER (
                    PARTITION BY match_id, team_id, possession_key
                    ORDER BY event_seconds, event_order
                ) AS previous_channel
            FROM competition_event_base
            WHERE event_type IN ('on_ball_engagement', 'player_possession')
              AND channel_end IS NOT NULL
        )
        SELECT
            match_id,
            team_id,
            COUNT(*) AS territory_switches
        FROM ordered
        WHERE previous_channel IS NOT NULL
          AND channel_end <> previous_channel
        GROUP BY match_id, team_id
        """

    def dual_half_space_possessions(self) -> str:
        return """
        WITH possession_summary AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                MAX(CASE WHEN channel_end = 'half_space_left' THEN 1 ELSE 0 END) AS visited_left_half_space,
                MAX(CASE WHEN channel_end = 'half_space_right' THEN 1 ELSE 0 END) AS visited_right_half_space
            FROM competition_event_base
            WHERE event_type IN ('on_ball_engagement', 'player_possession', 'passing_option')
            GROUP BY match_id, team_id, possession_key
        )
        SELECT
            match_id,
            team_id,
            COUNT(*) AS dual_half_space_possessions
        FROM possession_summary
        WHERE visited_left_half_space = 1
          AND visited_right_half_space = 1
        GROUP BY match_id, team_id
        """

    def territory_recycling(self) -> str:
        return """
        WITH ordered AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                third_end,
                LAG(third_end) OVER (
                    PARTITION BY match_id, team_id, possession_key
                    ORDER BY event_seconds, event_order
                ) AS previous_third
            FROM competition_event_base
            WHERE event_type IN ('on_ball_engagement', 'player_possession')
              AND third_end IS NOT NULL
        )
        SELECT
            match_id,
            team_id,
            COUNT(*) AS territory_recycling_events
        FROM ordered
        WHERE previous_third = 'attacking_third'
          AND third_end IN ('middle_third', 'defensive_third')
        GROUP BY match_id, team_id
        """

    def territory_circulation(self) -> str:
        return """
        WITH ordered AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                channel_end,
                third_end,
                LAG(channel_end) OVER (
                    PARTITION BY match_id, team_id, possession_key
                    ORDER BY event_seconds, event_order
                ) AS previous_channel
            FROM competition_event_base
            WHERE event_type IN ('on_ball_engagement', 'player_possession', 'passing_option')
              AND channel_end IS NOT NULL
        ),
        channel_switches AS (
            SELECT
                match_id,
                team_id,
                possession_key,
                COUNT(*) AS switch_count,
                MAX(CASE WHEN third_end = 'attacking_third' THEN 1 ELSE 0 END) AS reached_attacking_third
            FROM ordered
            WHERE previous_channel IS NOT NULL
              AND channel_end <> previous_channel
            GROUP BY match_id, team_id, possession_key
        )
        SELECT
            match_id,
            team_id,
            SUM(switch_count) AS territory_circulation_before_attack
        FROM channel_switches
        WHERE reached_attacking_third = 1
        GROUP BY match_id, team_id
        """

    def deep_progressions(self) -> str:
        return """
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
        """

    def queries(self) -> list[str]:
        return [
            self.territorial_persistence(),
            self.territory_switches(),
            self.dual_half_space_possessions(),
            self.territory_recycling(),
            self.territory_circulation(),
            self.deep_progressions(),
        ]
