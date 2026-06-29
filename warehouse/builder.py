from pathlib import Path

import duckdb


class WarehouseBuilder:
    """
    Generic warehouse builder for DuckDB projects.
    """

    def __init__(self, database_path: Path):

        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = None

    def connect(self):

        if self.database_path.exists():
            self.database_path.unlink()

        self.connection = duckdb.connect(str(self.database_path))

        print(f"Connected: {self.database_path.name}")

    def close(self):

        if self.connection is not None:
            self.connection.close()

            print("Connection closed.")

    def execute_sql_file(self, sql_file: Path):

        sql = Path(sql_file).read_text(encoding="utf-8")

        print(f"Executing {sql_file.name}")

        self.connection.execute(sql)

    def execute(self, sql: str, params=None):

        if params is None:
            return self.connection.execute(sql)

        return self.connection.execute(sql, params)

    def query(self, sql: str):

        return self.connection.execute(sql).fetchdf()

    def scalar(self, sql: str):

        return self.connection.execute(sql).fetchone()[0]

    def table_exists(self, table_name: str):

        count = self.scalar(
            f"""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{table_name}'
            """
        )

        return count > 0

    def row_count(self, table_name: str):

        return self.scalar(
            f"""
            SELECT COUNT(*)
            FROM {table_name}
            """
        )

    def describe(self, table_name: str):

        return self.query(
            f"""
            DESCRIBE {table_name}
            """
        )

    def summarize(self):

        tables = self.query(
            """
            SELECT table_name

            FROM information_schema.tables

            WHERE table_schema='main'

            ORDER BY table_name
            """
        )

        print()

        print("=" * 70)
        print("WAREHOUSE SUMMARY")
        print("=" * 70)

        for table in tables.table_name:
            rows = self.row_count(table)

            print(f"{table:<30} {rows:>12,}")

        print("=" * 70)

    def checkpoint(self, message):

        print()

        print("-" * 70)
        print(message)
        print("-" * 70)
