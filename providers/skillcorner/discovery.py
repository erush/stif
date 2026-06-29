from pathlib import Path

from providers.skillcorner.paths import MATCHES_DIR


def discover_match_dirs() -> list[Path]:
    if not MATCHES_DIR.exists():
        raise FileNotFoundError(f"Missing SkillCorner matches directory: {MATCHES_DIR}")

    return sorted(
        [path for path in MATCHES_DIR.iterdir() if path.is_dir()],
        key=lambda path: int(path.name),
    )


def dynamic_event_files() -> list[tuple[int, Path]]:
    files = []

    for match_dir in discover_match_dirs():
        match_id = int(match_dir.name)
        csv_path = match_dir / f"{match_id}_dynamic_events.csv"

        if csv_path.exists():
            files.append((match_id, csv_path))

    return files


def phase_files() -> list[tuple[int, Path]]:
    files = []

    for match_dir in discover_match_dirs():
        match_id = int(match_dir.name)
        csv_path = match_dir / f"{match_id}_phases_of_play.csv"

        if csv_path.exists():
            files.append((match_id, csv_path))

    return files


def match_metadata_files() -> list[tuple[int, Path]]:
    files = []

    for match_dir in discover_match_dirs():
        match_id = int(match_dir.name)
        json_path = match_dir / f"{match_id}_match.json"

        if json_path.exists():
            files.append((match_id, json_path))

    return files
