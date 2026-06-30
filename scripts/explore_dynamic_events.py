from pathlib import Path
import duckdb
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "warehouse" / "soccer.duckdb"


def show_table(title, df):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    print(df.to_string(index=False))


def main():

    con = duckdb.connect(str(DB_PATH))

    print("\n")
    print("=" * 80)
    print("FACT_DYNAMIC_EVENTS")
    print("=" * 80)

    print(
        con.execute("""
        SELECT COUNT(*)
        FROM fact_dynamic_events
    """).fetchone()[0]
    )

    print("\nColumns\n")

    describe = con.execute("""
        DESCRIBE fact_dynamic_events
    """).fetchdf()

    print(describe.to_string(index=False))

    object_columns = []

    for row in describe.itertuples():
        dtype = row.column_type.upper()

        if "VARCHAR" in dtype:
            object_columns.append(row.column_name)

    print("\n")

    for column in object_columns:
        try:
            values = con.execute(f"""
                SELECT "{column}", COUNT(*) cnt
                FROM fact_dynamic_events
                GROUP BY 1
                ORDER BY cnt DESC
                LIMIT 25
            """).fetchdf()

            show_table(column, values)

        except Exception:
            pass

    con.close()


if __name__ == "__main__":
    main()
