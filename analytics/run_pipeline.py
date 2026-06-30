from analytics.publish_features import publish
from analytics.export_features import export


def main():

    print()

    print("=" * 80)
    print("STIF ANALYTICS PIPELINE")
    print("=" * 80)

    publish()

    export()

    print()

    print("Pipeline complete.")


if __name__ == "__main__":
    main()
