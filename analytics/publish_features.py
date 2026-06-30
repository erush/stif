from pathlib import Path

import duckdb

from analytics.build_features import build


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE = PROJECT_ROOT / "warehouse" / "soccer.duckdb"


def publish():

    features = build()

    con = duckdb.connect(DATABASE)

    con.register(
        "features_df",
        features,
    )

    con.execute(
        """
        CREATE OR REPLACE TABLE analytics_team_features AS
        SELECT *
        FROM features_df
        """
    )

    con.close()

    print()

    print("Published analytics_team_features")


if __name__ == "__main__":
    publish()
