STIF Project Layers

Purpose

STIF is organized into architectural layers.

Each layer has a single responsibility.

Keeping responsibilities separate makes the system easier to extend, test, and maintain as additional tactical domains and feature engineering pipelines are added.

⸻

Layer 1 — Provider

Location

data/raw/

Purpose

Stores the original SkillCorner datasets.

Responsibilities

* Match metadata
* Dynamic event files
* Phases of play
* Tracking data
* Aggregate datasets

Rules

* Never modify raw provider files.
* Treat the provider as read-only.

⸻

Layer 2 — Warehouse

Location

warehouse/
sql/

Purpose

Transforms provider files into a normalized DuckDB warehouse.

Responsibilities

* Data loading
* Schema creation
* Table validation
* ETL pipeline
* Warehouse integrity

Outputs

soccer.duckdb

Rules

* No tactical logic.
* No feature engineering.
* Only data storage and normalization.

⸻

Layer 3 — Semantic Layer

Location

semantic/

Purpose

Defines the meaning of the provider.

Responsibilities

* Event catalog
* Phase catalog
* Pitch definitions
* Shared constants
* Enumerations

Examples

ATTACKING_THIRD
BUILD_UP
COUNTER_PRESS
HALF_SPACE_LEFT

Rules

* Contains vocabulary.
* Never performs calculations.

⸻

Layer 4 — Feature Specification Layer

Location

registry/

Purpose

Defines every tactical feature declaratively.

Responsibilities

* FeatureSpec definitions
* Tactical metadata
* Feature descriptions
* Interpretations

Example

territory_attacking_third_engagements

Rules

* Defines WHAT should be computed.
* Never contains SQL execution.

⸻

Layer 5 — Domain Layer

Location

domains/

Purpose

Implements tactical domains.

Responsibilities

* Territory
* Progression
* Transition
* Possession
* Pressure
* Chance Creation
* Set Pieces

Each domain contains

builder.py
queries.py
validator.py

Rules

* Contains domain-specific tactical logic.
* May combine multiple FeatureSpecs.
* Responsible for advanced calculations.

⸻

Layer 6 — Feature Engine

Location

feature_engine/

Purpose

Generic framework for executing FeatureSpecs.

Responsibilities

* SQL generation
* Validation
* Documentation generation
* Feature export
* Execution engine

Rules

* Domain agnostic.
* Never contains soccer-specific logic.

⸻

Layer 7 — Analytics

Location

analytics/

Purpose

User-facing entry points.

Responsibilities

* Build features
* Export submissions
* Validation
* Reporting

Rules

* Orchestrates workflows.
* Does not implement business logic.

⸻

Layer 8 — Outputs

Location

outputs/

Purpose

Stores generated artifacts.

Examples

* features.csv
* validation reports
* submission files

Rules

* Generated only.
* Never edited manually.

⸻

Architectural Flow

SkillCorner Provider
        │
        ▼
Warehouse
        │
        ▼
Semantic Layer
        │
        ▼
Feature Specifications
        │
        ▼
Domain Builders
        │
        ▼
Feature Engine
        │
        ▼
Analytics
        │
        ▼
Competition Outputs

⸻

Design Principles

* Every directory has a single responsibility.
* Tactical concepts belong in domains.
* Generic execution belongs in the feature engine.
* Provider vocabulary belongs in the semantic layer.
* Feature definitions belong in the registry.
* Analytics orchestrates rather than computes.
* The warehouse stores data but does not perform tactical analysis.