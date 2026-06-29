from pathlib import Path
import json
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_ROOT = PROJECT_ROOT / "data" / "raw" / "skillcorner"
MATCHES_DIR = RAW_ROOT / "data" / "matches"

OUTPUTS_DIR = PROJECT_ROOT / "outputs"
REFERENCES_DIR = PROJECT_ROOT / "references" / "skillcorner"

SUMMARY_JSON = OUTPUTS_DIR / "dataset_summary.json"
PROFILE_MD = OUTPUTS_DIR / "dataset_profile.md"

DATA_DICTIONARY_MD = REFERENCES_DIR / "data_dictionary.md"
EVENT_TYPES_MD = REFERENCES_DIR / "event_types.md"
PHASE_TYPES_MD = REFERENCES_DIR / "phase_types.md"


def ensure_dirs() -> None:
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def discover_matches() -> list[Path]:
    if not MATCHES_DIR.exists():
        raise FileNotFoundError(f"Missing matches directory: {MATCHES_DIR}")

    return sorted(
        [p for p in MATCHES_DIR.iterdir() if p.is_dir()],
        key=lambda p: p.name,
    )


def profile_csv(path: Path) -> dict:
    df = pd.read_csv(path)

    profile = {
        "file": str(path.relative_to(PROJECT_ROOT)),
        "rows": int(len(df)),
        "columns": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
        "missing_values": {
            col: int(df[col].isna().sum()) for col in df.columns
        },
        "unique_values": {},
        "numeric_ranges": {},
    }

    for col in df.columns:
        unique_count = int(df[col].nunique(dropna=True))

        if unique_count <= 50:
            values = df[col].dropna().unique().tolist()
            profile["unique_values"][col] = sorted(map(str, values))

        if pd.api.types.is_numeric_dtype(df[col]):
            profile["numeric_ranges"][col] = {
                "min": None if df[col].dropna().empty else float(df[col].min()),
                "max": None if df[col].dropna().empty else float(df[col].max()),
            }

    return profile


def profile_match_metadata(path: Path) -> dict:
    data = load_json(path)

    return {
        "file": str(path.relative_to(PROJECT_ROOT)),
        "top_level_fields": sorted(data.keys()),
        "raw": data,
    }


def profile_match_folder(match_dir: Path) -> dict:
    match_id = match_dir.name

    expected_files = {
        "match_metadata": match_dir / f"{match_id}_match.json",
        "dynamic_events": match_dir / f"{match_id}_dynamic_events.csv",
        "phases_of_play": match_dir / f"{match_id}_phases_of_play.csv",
        "tracking": match_dir / f"{match_id}_tracking_extrapolated.jsonl",
    }

    files_present = {
        name: path.exists() for name, path in expected_files.items()
    }

    profile = {
        "match_id": match_id,
        "folder": str(match_dir.relative_to(PROJECT_ROOT)),
        "files_present": files_present,
    }

    if expected_files["match_metadata"].exists():
        profile["match_metadata"] = profile_match_metadata(
            expected_files["match_metadata"]
        )

    if expected_files["dynamic_events"].exists():
        profile["dynamic_events"] = profile_csv(
            expected_files["dynamic_events"]
        )

    if expected_files["phases_of_play"].exists():
        profile["phases_of_play"] = profile_csv(
            expected_files["phases_of_play"]
        )

    if expected_files["tracking"].exists():
        tracking_path = expected_files["tracking"]
        profile["tracking"] = {
            "file": str(tracking_path.relative_to(PROJECT_ROOT)),
            "exists": True,
            "size_mb": round(tracking_path.stat().st_size / 1_000_000, 2),
            "status": "inventoried_only_not_loaded",
        }

    return profile


def aggregate_schema(match_profiles: list[dict], section: str) -> dict:
    all_columns = {}
    all_unique_values = {}
    all_numeric_ranges = {}

    for match in match_profiles:
        if section not in match:
            continue

        profile = match[section]

        for col in profile.get("columns", []):
            all_columns.setdefault(col, {
                "dtype_examples": set(),
                "matches_present": 0,
                "total_missing": 0,
            })

            all_columns[col]["matches_present"] += 1
            all_columns[col]["total_missing"] += profile["missing_values"].get(col, 0)

            dtype = profile["dtypes"].get(col)
            if dtype:
                all_columns[col]["dtype_examples"].add(dtype)

        for col, values in profile.get("unique_values", {}).items():
            all_unique_values.setdefault(col, set()).update(values)

        for col, ranges in profile.get("numeric_ranges", {}).items():
            all_numeric_ranges.setdefault(col, {"min": [], "max": []})
            if ranges["min"] is not None:
                all_numeric_ranges[col]["min"].append(ranges["min"])
            if ranges["max"] is not None:
                all_numeric_ranges[col]["max"].append(ranges["max"])

    columns_clean = {
        col: {
            "dtype_examples": sorted(values["dtype_examples"]),
            "matches_present": values["matches_present"],
            "total_missing": values["total_missing"],
        }
        for col, values in sorted(all_columns.items())
    }

    unique_clean = {
        col: sorted(values)
        for col, values in sorted(all_unique_values.items())
    }

    ranges_clean = {}
    for col, values in all_numeric_ranges.items():
        ranges_clean[col] = {
            "min": min(values["min"]) if values["min"] else None,
            "max": max(values["max"]) if values["max"] else None,
        }

    return {
        "columns": columns_clean,
        "unique_values": unique_clean,
        "numeric_ranges": ranges_clean,
    }


def build_summary(match_profiles: list[dict]) -> dict:
    dynamic_rows = sum(
        m.get("dynamic_events", {}).get("rows", 0)
        for m in match_profiles
    )

    phase_rows = sum(
        m.get("phases_of_play", {}).get("rows", 0)
        for m in match_profiles
    )

    return {
        "project": "STIF",
        "provider": "SkillCorner Open Data",
        "raw_root": str(RAW_ROOT.relative_to(PROJECT_ROOT)),
        "matches_dir": str(MATCHES_DIR.relative_to(PROJECT_ROOT)),
        "match_count": len(match_profiles),
        "match_ids": [m["match_id"] for m in match_profiles],
        "total_dynamic_event_rows": int(dynamic_rows),
        "total_phase_rows": int(phase_rows),
        "dynamic_events_schema": aggregate_schema(match_profiles, "dynamic_events"),
        "phases_schema": aggregate_schema(match_profiles, "phases_of_play"),
        "matches": match_profiles,
    }


def write_json(summary: dict) -> None:
    with SUMMARY_JSON.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


def md_table(rows: list[list[str]]) -> str:
    if not rows:
        return ""

    header = rows[0]
    separator = ["---"] * len(header)
    body = rows[1:]

    lines = [
        "| " + " | ".join(header) + " |",
        "| " + " | ".join(separator) + " |",
    ]

    for row in body:
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


def write_profile_markdown(summary: dict) -> None:
    lines = []

    lines.append("# STIF Dataset Profile")
    lines.append("")
    lines.append(f"Provider: {summary['provider']}")
    lines.append(f"Raw root: `{summary['raw_root']}`")
    lines.append(f"Matches: {summary['match_count']}")
    lines.append(f"Dynamic event rows: {summary['total_dynamic_event_rows']}")
    lines.append(f"Phase rows: {summary['total_phase_rows']}")
    lines.append("")

    lines.append("## Match Inventory")
    lines.append("")
    rows = [["match_id", "dynamic_events", "phases", "match_metadata", "tracking"]]

    for match in summary["matches"]:
        files = match["files_present"]
        rows.append([
            match["match_id"],
            str(files.get("dynamic_events", False)),
            str(files.get("phases_of_play", False)),
            str(files.get("match_metadata", False)),
            str(files.get("tracking", False)),
        ])

    lines.append(md_table(rows))
    lines.append("")

    lines.append("## Dynamic Event Columns")
    lines.append("")
    rows = [["column", "dtype_examples", "matches_present", "total_missing"]]

    for col, info in summary["dynamic_events_schema"]["columns"].items():
        rows.append([
            col,
            ", ".join(info["dtype_examples"]),
            str(info["matches_present"]),
            str(info["total_missing"]),
        ])

    lines.append(md_table(rows))
    lines.append("")

    lines.append("## Phase Columns")
    lines.append("")
    rows = [["column", "dtype_examples", "matches_present", "total_missing"]]

    for col, info in summary["phases_schema"]["columns"].items():
        rows.append([
            col,
            ", ".join(info["dtype_examples"]),
            str(info["matches_present"]),
            str(info["total_missing"]),
        ])

    lines.append(md_table(rows))
    lines.append("")

    PROFILE_MD.write_text("\n".join(lines), encoding="utf-8")


def write_data_dictionary(summary: dict) -> None:
    lines = ["# SkillCorner Data Dictionary", ""]

    lines.append("## Dynamic Events")
    lines.append("")
    for col, info in summary["dynamic_events_schema"]["columns"].items():
        lines.append(f"### {col}")
        lines.append(f"- Dtype examples: {', '.join(info['dtype_examples'])}")
        lines.append(f"- Matches present: {info['matches_present']}")
        lines.append(f"- Total missing: {info['total_missing']}")
        lines.append("")

    lines.append("## Phases of Play")
    lines.append("")
    for col, info in summary["phases_schema"]["columns"].items():
        lines.append(f"### {col}")
        lines.append(f"- Dtype examples: {', '.join(info['dtype_examples'])}")
        lines.append(f"- Matches present: {info['matches_present']}")
        lines.append(f"- Total missing: {info['total_missing']}")
        lines.append("")

    DATA_DICTIONARY_MD.write_text("\n".join(lines), encoding="utf-8")


def write_event_types(summary: dict) -> None:
    schema = summary["dynamic_events_schema"]
    unique_values = schema["unique_values"]

    lines = ["# SkillCorner Dynamic Event Types", ""]

    candidate_cols = [
        col for col in unique_values
        if "event" in col.lower() or "type" in col.lower()
    ]

    if not candidate_cols:
        lines.append("No obvious event type columns detected.")
    else:
        for col in candidate_cols:
            lines.append(f"## {col}")
            lines.append("")
            for value in unique_values[col]:
                lines.append(f"- {value}")
            lines.append("")

    EVENT_TYPES_MD.write_text("\n".join(lines), encoding="utf-8")


def write_phase_types(summary: dict) -> None:
    schema = summary["phases_schema"]
    unique_values = schema["unique_values"]

    lines = ["# SkillCorner Phase Types", ""]

    candidate_cols = [
        col for col in unique_values
        if "phase" in col.lower() or "type" in col.lower()
    ]

    if not candidate_cols:
        lines.append("No obvious phase type columns detected.")
    else:
        for col in candidate_cols:
            lines.append(f"## {col}")
            lines.append("")
            for value in unique_values[col]:
                lines.append(f"- {value}")
            lines.append("")

    PHASE_TYPES_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()

    match_dirs = discover_matches()
    match_profiles = [profile_match_folder(match_dir) for match_dir in match_dirs]

    summary = build_summary(match_profiles)

    write_json(summary)
    write_profile_markdown(summary)
    write_data_dictionary(summary)
    write_event_types(summary)
    write_phase_types(summary)

    print("STIF dataset profiling complete.")
    print(f"Matches profiled: {summary['match_count']}")
    print(f"Dynamic event rows: {summary['total_dynamic_event_rows']}")
    print(f"Phase rows: {summary['total_phase_rows']}")
    print(f"Wrote: {SUMMARY_JSON.relative_to(PROJECT_ROOT)}")
    print(f"Wrote: {PROFILE_MD.relative_to(PROJECT_ROOT)}")
    print(f"Wrote: {DATA_DICTIONARY_MD.relative_to(PROJECT_ROOT)}")
    print(f"Wrote: {EVENT_TYPES_MD.relative_to(PROJECT_ROOT)}")
    print(f"Wrote: {PHASE_TYPES_MD.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()