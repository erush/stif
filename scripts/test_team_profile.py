from pprint import pprint

from skills.team_profile import build_team_profile


profile = build_team_profile(
    match_id=1886347,
    team_id=1805,
)

pprint(profile)
