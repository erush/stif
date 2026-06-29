from providers.skillcorner.discovery import phase_files
from providers.skillcorner.duckdb_load import load_csv_files


def load_phases(con) -> None:
    load_csv_files(
        con=con,
        table_name="fact_phases",
        files=phase_files(),
    )
