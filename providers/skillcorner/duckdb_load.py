from pathlib import Path


def sql_path(path: Path) -> str:
    return str(path).replace("'", "''")


def create_fact_table_from_first_csv(con, table_name: str, csv_path: Path) -> list[str]:
    con.execute(f"DROP TABLE IF EXISTS {table_name}")

    con.execute(
        f"""
        CREATE TABLE {table_name} AS
        SELECT *
        FROM read_csv_auto('{sql_path(csv_path)}')
        LIMIT 0
        """
    )

    rows = con.execute(f"DESCRIBE {table_name}").fetchall()
    return [row[0] for row in rows]


def load_csv_files(con, table_name: str, files: list[tuple[int, Path]]) -> None:
    if not files:
        raise FileNotFoundError(f"No CSV files found for {table_name}")

    columns = create_fact_table_from_first_csv(con, table_name, files[0][1])
    has_match_id = "match_id" in columns

    if not has_match_id:
        con.execute(f"ALTER TABLE {table_name} ADD COLUMN match_id BIGINT")

    for match_id, csv_path in files:
        print(f"Loading {table_name}: {match_id}")

        if has_match_id:
            con.execute(
                f"""
                INSERT INTO {table_name}
                SELECT *
                FROM read_csv_auto('{sql_path(csv_path)}')
                """
            )
        else:
            con.execute(
                f"""
                INSERT INTO {table_name}
                SELECT *, {match_id}
                FROM read_csv_auto('{sql_path(csv_path)}')
                """
            )
