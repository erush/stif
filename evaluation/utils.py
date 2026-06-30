from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURES_PATH = PROJECT_ROOT / "outputs" / "features.csv"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"


def load_features() -> pd.DataFrame:
    if not FEATURES_PATH.exists():
        raise FileNotFoundError(
            f"Missing {FEATURES_PATH}. Run python -m analytics.build_features first."
        )

    return pd.read_csv(FEATURES_PATH)


def feature_columns(df: pd.DataFrame) -> list[str]:
    return [col for col in df.columns if col not in {"match_id", "team_id"}]


def ensure_outputs_dir() -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
