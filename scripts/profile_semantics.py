from pathlib import Path
import json
import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DB_PATH = PROJECT_ROOT / "warehouse" / "soccer.duckdb"
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "semantic_profile.json"
REPORT_PATH = PROJECT_ROOT / "outputs" / "semantic_profile.md"


def get_columns(con, table_name: str) -> list[str]:
    rows = con.execute(f"DESCRIBE {table_name}").fetchall()
    return [row[0] for row in rows]


def categorical_columns(con, table_name: str, max_unique: int = 75) -> dict:
    columns = get_columns(con, table_name)
    result = {}

    for col in columns:
        try:
            count = con.execute(
                f"""
                SELECT COUNT(DISTINCT "{col}")
                FROM {table_name}
                """
            ).fetchone()[0]

            if count <= max_unique:
                values = con.execute(
                    f"""
                    SELECT DISTINCT "{col}"
                    FROM {table_name}
                    WHERE "{col}" IS NOT NULL
                    ORDER BY "{col}"
                    """
                ).fetchall()

                result[col] = [str(row[0]) for row in values]

        except Exception:
            continue

    return result


def numeric_ranges(con, table_name: str) -> dict:
    rows = con.execute(f"DESCRIBE {table_name}").fetchall()
    result = {}

    numeric_types = {
        "INTEGER",
        "BIGINT",
        "DOUBLE",
        "FLOAT",
        "REAL",
        "DECIMAL",
        "HUGEINT",
        "UBIGINT",
        "UINTEGER",
    }

    for col, dtype, *_ in rows:
        dtype_upper = str(dtype).upper()

        if not any(t in dtype_upper for t in numeric_types):
            continue

        try:
            min_val, max_val = con.execute(
                f"""
                SELECT MIN("{col}"), MAX("{col}")
                FROM {table_name}
                """
            ).fetchone()

            result[col] = {
                "min": min_val,
                "max": max_val,
            }

        except Exception:
            continue

    return result


def profile_table(con, table_name: str) -> dict:
    return {
        "columns": get_columns(con, table_name),
        "categorical_values": categorical_columns(con, table_name),
        "numeric_ranges": numeric_ranges(con, table_name),
        "row_count": con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0],
    }


def write_markdown(profile: dict) -> None:
    lines = ["# STIF Semantic Profile", ""]

    for table, data in profile.items():
        lines.append(f"## {table}")
        lines.append("")
        lines.append(f"Rows: {data['row_count']:,}")
        lines.append("")

        lines.append("### Columns")
        lines.append("")
        for col in data["columns"]:
            lines.append(f"- `{col}`")
        lines.append("")

        lines.append("### Categorical Values")
        lines.append("")
        for col, values in data["categorical_values"].items():
            lines.append(f"#### {col}")
            for value in values:
                lines.append(f"- {value}")
            lines.append("")

        lines.append("### Numeric Ranges")
        lines.append("")
        for col, values in data["numeric_ranges"].items():
            lines.append(f"- `{col}`: {values['min']} → {values['max']}")
        lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Missing warehouse database: {DB_PATH}. Run python warehouse/build_duckdb.py first."
        )

    con = duckdb.connect(str(DB_PATH))

    profile = {
        "fact_dynamic_events": profile_table(con, "fact_dynamic_events"),
        "fact_phases": profile_table(con, "fact_phases"),
    }

    con.close()

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_PATH.write_text(
        json.dumps(profile, indent=2, default=str),
        encoding="utf-8",
    )

    write_markdown(profile)

    print("Semantic profiling complete.")
    print(f"Wrote: {OUTPUT_PATH.relative_to(PROJECT_ROOT)}")
    print(f"Wrote: {REPORT_PATH.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
