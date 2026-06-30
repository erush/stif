from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FEATURES_PATH = PROJECT_ROOT / "outputs" / "features.csv"


class FeatureService:
    def __init__(self):

        self._features = None

    @property
    def features(self) -> pd.DataFrame:

        if self._features is None:
            self._features = pd.read_csv(FEATURES_PATH)

        return self._features

    def refresh(self):

        self._features = pd.read_csv(FEATURES_PATH)

    def all(self) -> pd.DataFrame:

        return self.features.copy()

    def match(self, match_id: int) -> pd.DataFrame:

        return self.features.loc[self.features.match_id == match_id].copy()

    def team(
        self,
        match_id: int,
        team_id: int,
    ) -> pd.Series:

        df = self.features

        row = df.loc[(df.match_id == match_id) & (df.team_id == team_id)]

        if row.empty:
            raise ValueError(f"No features for match={match_id}, team={team_id}")

        return row.iloc[0]
