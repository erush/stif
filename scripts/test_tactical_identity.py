from pprint import pprint

from services.profile_service import ProfileService
from skills.tactical_identity import build_tactical_identity


profile = ProfileService().build_team_profile(
    1886347,
    1805,
)

identity = build_tactical_identity(profile)

pprint(identity)
