from competition.builder import CompetitionFeatureBuilder


def main():

    builder = CompetitionFeatureBuilder()

    try:
        df = builder.build()

        print()
        print(df.head())
        print()
        print(f"{len(df)} rows exported.")
        print("Wrote analytics_competition_features")
        print("Wrote outputs/competition_features.csv")

    finally:
        builder.close()


if __name__ == "__main__":
    main()
