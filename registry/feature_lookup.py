from collections import defaultdict

from registry.all_features import FEATURE_SPECS


FEATURE_BY_ID = {spec.id: spec for spec in FEATURE_SPECS}


FEATURE_BY_COLUMN = {spec.output_column: spec for spec in FEATURE_SPECS}


DOMAIN_FEATURES = defaultdict(list)

CATEGORY_FEATURES = defaultdict(list)


for spec in FEATURE_SPECS:
    DOMAIN_FEATURES[spec.domain].append(spec)

    CATEGORY_FEATURES[(spec.domain, spec.category)].append(spec)
