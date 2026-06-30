from pathlib import Path

from analytics.build_features import build


PROJECT_ROOT = Path(__file__).resolve().parents[1]

OUTPUTS = PROJECT_ROOT / "outputs"


def export():

    OUTPUTS.mkdir(
        parents=True,
        exist_ok=True,
    )

    features = build()

    path = OUTPUTS / "features.csv"

    features.to_csv(
        path,
        index=False,
    )

    print()

    print(f"Exported {path}")


if __name__ == "__main__":
    export()
