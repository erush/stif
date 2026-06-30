from pprint import pprint

from services.profile_service import ProfileService


profiles = ProfileService()

team = profiles.build_team_profile(
    match_id=1886347,
    team_id=1805,
)

pprint(team)
