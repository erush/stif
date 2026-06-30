from pprint import pprint

from services.profile_service import ProfileService
from skills.pressure_profile import build_pressure_profile


profile = ProfileService().build_team_profile(
    1886347,
    1805,
)

pprint(build_pressure_profile(profile))
