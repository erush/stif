from pathlib import Path

import duckdb
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = PROJECT_ROOT / "warehouse" / "soccer.duckdb"


class WarehouseService:
    def __init__(self):

        self.connection = duckdb.connect(DATABASE_PATH)

    def query(
        self,
        sql: str,
        params=None,
    ) -> pd.DataFrame:

        if params is None:
            return self.connection.execute(sql).df()

        return self.connection.execute(sql, params).df()

    def table(
        self,
        table_name: str,
    ) -> pd.DataFrame:

        return self.query(
            f"""
            SELECT *
            FROM {table_name}
            """
        )

    def close(self):

        self.connection.close()
