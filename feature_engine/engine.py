from pathlib import Path

import duckdb
import pandas as pd

from registry.all_features import FEATURE_SPECS

from feature_engine.validator import (
    validate_specs_against_warehouse,
    validate_generated_sql,
)

from feature_engine.exporter import export_features


class FeatureEngine:
    def __init__(self, database_path: Path):

        self.database_path = Path(database_path)

        self.connection = duckdb.connect(str(self.database_path))

    def validate(self):

        validate_specs_against_warehouse(
            self.connection,
            FEATURE_SPECS,
        )

        validate_generated_sql(
            self.connection,
            FEATURE_SPECS,
        )

    def build(self) -> pd.DataFrame:

        return export_features(
            con=self.connection,
            specs=FEATURE_SPECS,
            output_path=Path("outputs/features.csv"),
            validate=True,
        )

    def close(self):

        self.connection.close()

    def __enter__(self):

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):

        self.close()
