import json

from providers.skillcorner.discovery import match_metadata_files


def load_matches(con) -> None:
    for match_id, json_path in match_metadata_files():
        data = json.loads(json_path.read_text(encoding="utf-8"))

        con.execute(
            """
            INSERT INTO dim_match (match_id, raw_match_json)
            VALUES (?, ?)
            """,
            [match_id, json.dumps(data)],
        )
