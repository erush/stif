# STIF Warehouse Design

Version: 0.1

Project: Soccer Tactical Intelligence Framework (STIF)

---

# Purpose

The STIF warehouse provides a canonical analytical layer between the raw SkillCorner Open Data repository and the tactical feature engineering pipeline.

Rather than querying raw CSV and JSON files directly, every downstream analytical process will operate from a normalized DuckDB warehouse.

This approach provides:

- reproducibility
- simplified analytics
- consistent relationships
- reusable SQL
- extensibility for future data providers

---

# Design Philosophy

STIF follows a warehouse-first architecture.

```
Raw Provider Data

↓

Canonical Warehouse

↓

Analytical Views

↓

Feature Engineering

↓

Competition Output
```

The warehouse intentionally mirrors the provider data while introducing a consistent relational structure.

No tactical calculations occur during ingestion.

Business logic belongs exclusively in the analytics layer.

---

# Data Sources

Version 1 of STIF consumes three primary SkillCorner datasets.

## Match Metadata

Source

```
{id}_match.json
```

Purpose

Provides match context including:

- competition
- venue
- kickoff
- pitch dimensions
- teams
- lineups
- player participation
- officials

---

## Dynamic Events

Source

```
{id}_dynamic_events.csv
```

Purpose

Primary source for tactical feature engineering.

Contains event-level actions throughout the match.

---

## Phases of Play

Source

```
{id}_phases_of_play.csv
```

Purpose

Provides structured attacking and defending phases throughout the match.

This dataset enables higher-level tactical segmentation beyond individual events.

---

## Tracking Data

Source

```
{id}_tracking_extrapolated.jsonl
```

Status

Not included in STIF Version 1.

Reserved for future releases.

---

# Warehouse Architecture

The warehouse is implemented in DuckDB.

Database

```
warehouse/soccer.duckdb
```

The warehouse consists of dimension tables and fact tables.

---

# Dimension Tables

## dim_match

One record per match.

Primary Key

```
match_id
```

Contains

- competition
- season
- kickoff
- venue
- pitch dimensions
- home team
- away team

---

## dim_team

One record per team.

Primary Key

```
team_id
```

Contains

- team name
- home/away mappings
- competition metadata where available

---

## dim_player

One record per player.

Primary Key

```
player_id
```

Contains

- player name
- team
- jersey number
- position
- minutes played

---

# Fact Tables

## fact_match

Normalized information extracted from match metadata.

Granularity

One record per match.

---

## fact_dynamic_events

Primary analytical table.

Granularity

One record per event.

Contains

- event identifiers
- timestamps
- event type
- coordinates
- player
- team
- contextual attributes

No derived metrics are stored.

---

## fact_phases

Granularity

One record per phase.

Contains

- attacking team
- defending team
- phase type
- start frame
- end frame
- duration

---

## fact_tracking

Reserved.

Not implemented in Version 1.

---

# Relationships

```
dim_match

        │

        ├──────────────┐

        │              │

fact_dynamic_events    fact_phases

        │

        │

dim_team

        │

        │

dim_player
```

---

# Data Lineage

```
SkillCorner Repository

↓

Warehouse Loaders

↓

DuckDB

↓

SQL Analytics

↓

Python Feature Builders

↓

features.csv
```

Every tactical attribute must be traceable to one or more provider fields.

---

# Ingestion Order

1. Match metadata
2. Teams
3. Players
4. Dynamic events
5. Phases of play
6. Validation
7. Analytical views

This dependency order ensures all foreign keys exist before loading fact tables.

---

# Naming Standards

Dimensions

```
dim_*
```

Facts

```
fact_*
```

Analytics

```
analytics_*
```

Views

```
vw_*
```

Temporary objects

```
tmp_*
```

---

# Analytical Layer

The warehouse intentionally contains no tactical intelligence.

Feature engineering occurs only after ingestion.

Primary analytical domains include:

- Territory Control
- Ball Progression
- Possession Structure
- Transition Play
- Defensive Pressure
- Chance Creation
- Set Piece Organization

Each domain produces reusable analytical views before generating final competition attributes.

---

# Validation

Every warehouse build validates:

- row counts
- duplicate primary keys
- null primary keys
- referential integrity
- event coverage
- phase coverage
- match coverage

Failures halt downstream processing.

---

# Version Roadmap

## Version 1

- Match metadata
- Dynamic events
- Phases of play
- Tactical feature engineering
- Kaggle competition submission

## Version 2

- Tracking integration
- Spatial intelligence
- Player movement analytics
- Possession geometry

## Version 3

- Tactical similarity
- Team style clustering
- Match intelligence agents
- Automated tactical reporting

---

# Success Criteria

The warehouse is considered complete when:

- all SkillCorner matches are successfully ingested
- all warehouse tables pass validation
- every tactical feature is derived exclusively from warehouse tables
- the competition notebook reproduces the complete pipeline from raw data to features.csv without manual intervention

The warehouse serves as the canonical data foundation for all future STIF development.