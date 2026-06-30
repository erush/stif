from services.warehouse_service import WarehouseService


WAREHOUSE = WarehouseService()


class FeatureService:
    TABLE = "analytics_team_features"

    def all(self):

        return WAREHOUSE.table(self.TABLE)

    def match(
        self,
        match_id: int,
    ):

        return WAREHOUSE.query(
            """
            SELECT *
            FROM analytics_team_features
            WHERE match_id = ?
            """,
            [match_id],
        )

    def team(
        self,
        match_id: int,
        team_id: int,
    ):

        df = WAREHOUSE.query(
            """
            SELECT *
            FROM analytics_team_features
            WHERE match_id = ?
              AND team_id = ?
            """,
            [match_id, team_id],
        )

        if df.empty:
            raise ValueError(f"No team found ({match_id}, {team_id})")

        return df.iloc[0]
