from providers.skillcorner.discovery import dynamic_event_files
from providers.skillcorner.duckdb_load import load_csv_files


def load_dynamic_events(con) -> None:
    load_csv_files(
        con=con,
        table_name="fact_dynamic_events",
        files=dynamic_event_files(),
    )
