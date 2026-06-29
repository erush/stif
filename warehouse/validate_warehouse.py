def validate_warehouse(con) -> None:
    checks = {
        "dim_match": "SELECT COUNT(*) FROM dim_match",
        "fact_dynamic_events": "SELECT COUNT(*) FROM fact_dynamic_events",
        "fact_phases": "SELECT COUNT(*) FROM fact_phases",
    }

    for table, query in checks.items():
        count = con.execute(query).fetchone()[0]
        if count == 0:
            raise ValueError(f"Validation failed: {table} has 0 rows")
        print(f"{table}: {count:,} rows")

    match_count = con.execute("SELECT COUNT(*) FROM dim_match").fetchone()[0]

    if match_count != 10:
        raise ValueError(f"Expected 10 matches, found {match_count}")

    print("Warehouse validation passed.")
