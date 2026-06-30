from feature_engine.specification import FeatureSpec, validate_feature_spec


def quote_identifier(value: str) -> str:
    return '"' + value.replace('"', '""') + '"'


def quote_literal(value: object) -> str:
    if value is None:
        return "NULL"

    if isinstance(value, bool):
        return "TRUE" if value else "FALSE"

    if isinstance(value, (int, float)):
        return str(value)

    return "'" + str(value).replace("'", "''") + "'"


def build_filter_clause(filters: dict[str, object]) -> str:
    if not filters:
        return ""

    clauses = []

    for column, value in filters.items():
        column_sql = quote_identifier(column)

        if isinstance(value, (list, tuple, set)):
            values = ", ".join(quote_literal(v) for v in value)
            clauses.append(f"{column_sql} IN ({values})")
        elif value is None:
            clauses.append(f"{column_sql} IS NULL")
        else:
            clauses.append(f"{column_sql} = {quote_literal(value)}")

    return "WHERE " + " AND ".join(clauses)


def aggregation_sql(spec: FeatureSpec) -> str:
    if spec.aggregation == "count":
        return f"COUNT(*) AS {quote_identifier(spec.output_column)}"

    if spec.aggregation == "distinct_count":
        return (
            f"COUNT(DISTINCT {quote_identifier(spec.source_column)}) "
            f"AS {quote_identifier(spec.output_column)}"
        )

    if spec.aggregation == "sum":
        return (
            f"SUM({quote_identifier(spec.source_column)}) "
            f"AS {quote_identifier(spec.output_column)}"
        )

    if spec.aggregation == "avg":
        return (
            f"AVG({quote_identifier(spec.source_column)}) "
            f"AS {quote_identifier(spec.output_column)}"
        )

    if spec.aggregation == "min":
        return (
            f"MIN({quote_identifier(spec.source_column)}) "
            f"AS {quote_identifier(spec.output_column)}"
        )

    if spec.aggregation == "max":
        return (
            f"MAX({quote_identifier(spec.source_column)}) "
            f"AS {quote_identifier(spec.output_column)}"
        )

    raise ValueError(f"Unsupported aggregation: {spec.aggregation}")


def generate_feature_sql(spec: FeatureSpec) -> str:
    validate_feature_spec(spec)

    group_cols = ", ".join(quote_identifier(col) for col in spec.group_by)
    filter_clause = build_filter_clause(spec.filters)
    metric_sql = aggregation_sql(spec)

    return f"""
SELECT
    {group_cols},
    {metric_sql}
FROM {quote_identifier(spec.source_table)}
{filter_clause}
GROUP BY
    {group_cols}
""".strip()


def generate_feature_view_sql(spec: FeatureSpec) -> str:
    return f"""
CREATE OR REPLACE VIEW {quote_identifier(spec.output_column)} AS
{generate_feature_sql(spec)}
""".strip()
