from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_ROOT = PROJECT_ROOT / "data" / "raw" / "skillcorner"
MATCHES_DIR = RAW_ROOT / "data" / "matches"
WAREHOUSE_DIR = PROJECT_ROOT / "warehouse"
DB_PATH = WAREHOUSE_DIR / "soccer.duckdb"
SCHEMA_SQL = PROJECT_ROOT / "sql" / "000_schema.sql"
