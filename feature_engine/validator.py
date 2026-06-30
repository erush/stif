from feature_engine.specification import FeatureSpec, validate_feature_spec
from feature_engine.sql_generator import generate_feature_sql


def validate_specs(specs: list[FeatureSpec]) -> None:
    seen_ids = set()
    seen_columns = set()

    for spec in specs:
        validate_feature_spec(spec)

        if spec.id in seen_ids:
            raise ValueError(f"Duplicate feature id: {spec.id}")

        if spec.output_column in seen_columns:
            raise ValueError(f"Duplicate output column: {spec.output_column}")

        seen_ids.add(spec.id)
        seen_columns.add(spec.output_column)


def validate_source_columns(con, spec: FeatureSpec) -> None:
    rows = con.execute(f'DESCRIBE "{spec.source_table}"').fetchall()
    columns = {row[0] for row in rows}

    missing = []

    for column in spec.group_by:
        if column not in columns:
            missing.append(column)

    if spec.source_column is not None and spec.source_column not in columns:
        missing.append(spec.source_column)

    for column in spec.filters:
        if column not in columns:
            missing.append(column)

    if missing:
        raise ValueError(
            f"{spec.id}: missing source columns in {spec.source_table}: {missing}"
        )


def validate_specs_against_warehouse(con, specs: list[FeatureSpec]) -> None:
    validate_specs(specs)

    for spec in specs:
        validate_source_columns(con, spec)


def validate_generated_sql(con, specs: list[FeatureSpec]) -> None:
    for spec in specs:
        sql = generate_feature_sql(spec)
        con.execute(f"SELECT * FROM ({sql}) LIMIT 1")


def validate_feature_output(df, required_rows: int = 20) -> None:
    if len(df) != required_rows:
        raise ValueError(f"Expected {required_rows} rows, found {len(df)}")

    required = {"match_id", "team_id"}

    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing required output columns: {missing}")

    if df[["match_id", "team_id"]].duplicated().any():
        raise ValueError("Duplicate match_id/team_id rows detected")
