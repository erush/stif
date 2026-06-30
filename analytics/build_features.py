from pathlib import Path

from feature_engine.engine import FeatureEngine


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE = PROJECT_ROOT / "warehouse" / "soccer.duckdb"


def build():

    with FeatureEngine(DATABASE) as engine:
        print()
        print("=" * 80)
        print("VALIDATING FEATURE SPECS")
        print("=" * 80)

        engine.validate()

        print()
        print("=" * 80)
        print("BUILDING FEATURES")
        print("=" * 80)

        return engine.build()


def main():

    df = build()

    print()
    print(df.head())
    print()
    print(f"{len(df)} rows built.")


if __name__ == "__main__":
    main()
