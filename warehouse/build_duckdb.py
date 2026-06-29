from pathlib import Path
import duckdb
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "warehouse" / "soccer.duckdb"
SCHEMA_SQL = PROJECT_ROOT / "sql" / "000_schema.sql"

sys.path.append(str(PROJECT_ROOT))

from warehouse.load_matches import load_matches
from warehouse.load_dynamic_events import load_dynamic_events
from warehouse.load_phases import load_phases
from warehouse.validate_warehouse import validate_warehouse


def execute_sql_file(con, path: Path) -> None:
    sql = path.read_text(encoding="utf-8")

    try:
        con.execute(sql)
    except Exception as e:
        print("\n===== SQL THAT FAILED =====\n")
        print(sql)
        print("\n==========================\n")
        raise


def build_database() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()

    con = duckdb.connect(str(DB_PATH))

    print("Creating schema...")
    execute_sql_file(con, SCHEMA_SQL)

    print("Loading matches...")
    load_matches(con)

    print("Loading dynamic events...")
    load_dynamic_events(con)

    print("Loading phases...")
    load_phases(con)

    print("Validating warehouse...")
    validate_warehouse(con)

    con.close()

    print(f"Warehouse built: {DB_PATH}")


if __name__ == "__main__":
    build_database()
