# STIF Competition Features

## Overview

This document defines the competition-specific tactical features developed for the SkillCorner Soccer Feature Engineering Hackathon.

Unlike traditional event statistics, these features are designed to capture higher-level tactical behaviors through interpretable, aggregated match-level attributes.

All competition features:

- are aggregated at the match/team level
- are fully reproducible
- use only SkillCorner Open Data
- dynamically process all matches in the repository
- avoid percentages, ratios, normalized values, and machine-learned representations
- emphasize tactical behavior rather than isolated event counts

The objective is to engineer attributes that describe **how teams play**, rather than simply **what events occurred**.

---

# Originality Statement

Many existing soccer metrics summarize isolated events such as passes, recoveries, shots, or entries into the attacking third.

STIF instead focuses on engineering **higher-order tactical attributes** that describe relationships between events within possessions, phases of play, and territorial sequences.

Examples include:

- sustaining territorial pressure rather than counting entries
- coordinated pressing rather than isolated pressure events
- complete-field progression rather than individual line breaks
- stable build-up structures rather than possession totals
- attacking movement diversity rather than individual runs

The resulting feature set is intended to provide interpretable tactical information suitable for coaching, scouting, tactical analysis, and future analytical modeling.

---

# Competition Rule Compliance

Every competition feature satisfies the official hackathon requirements.

- ✓ Aggregated match/team-level attributes
- ✓ Derived exclusively from SkillCorner Open Data
- ✓ Dynamic loading of all matches
- ✓ Fully reproducible
- ✓ No percentages
- ✓ No ratios
- ✓ No per-minute or per-possession metrics
- ✓ No normalized values
- ✓ No machine learning
- ✓ No embeddings
- ✓ No proprietary external datasets

---

# Competition Feature Summary

| Feature | Domain | Status |
|----------|--------|--------|
| Territorial Persistence | Territory | Implemented |
| Deep Territory Progressions | Territory | Implemented |
| Multi-Line Progressions | Progression | Implemented |
| Transition Burst Possessions | Transition | Implemented |
| Stable Build-Up Sequences | Possession | Implemented |
| Pressing Wave Events | Pressure | Implemented |
| Penetration Diversity Possessions | Chance Creation | Implemented |
| Territory Switching | Territory | Planned |
| Dual Half-Space Possessions | Territory | Planned |
| Multi-Runner Attacks | Chance Creation | Planned |
| High Press Recoveries | Pressure | Planned |
| Long Possession Sequences | Possession | Planned |
| Progressive Build-Up Chains | Progression | Planned |
| Transition Continuity | Transition | Planned |
| Restart Territory Gain | Set Pieces | Planned |

---

# Implemented Competition Features

---

## Territorial Persistence

### Soccer Question

Can a team sustain territorial pressure after entering the attacking third?

### Tactical Motivation

Traditional territorial statistics measure entries into advanced areas. This feature measures a team's ability to remain there once possession has been established.

### Computation

For every possession:

- identify attacking-third engagements
- count consecutive attacking-third engagements
- aggregate the total across the match

### Interpretation

Higher values indicate sustained territorial dominance.

### Novelty

Measures territorial persistence rather than territorial volume.

### Limitations

Does not distinguish between dangerous and harmless possession.

---

## Deep Territory Progressions

### Soccer Question

How often does a team successfully progress possession from defensive territory into the attacking third?

### Tactical Motivation

Captures complete-field progression rather than isolated forward movement.

### Computation

Count possessions that touch both:

- defensive third
- attacking third

### Interpretation

Higher values indicate effective progression through the entire field.

### Novelty

Measures complete territorial advancement instead of individual progression events.

### Limitations

Does not evaluate the quality of the attack after progression.

---

## Multi-Line Progressions

### Soccer Question

How frequently does a possession penetrate multiple defensive lines?

### Tactical Motivation

Breaking multiple defensive structures is a defining characteristic of successful positional attacks.

### Computation

Count possessions containing:

- first-line break
- second-line break
- last-line break

### Interpretation

Higher values indicate complete progression through defensive organization.

### Novelty

Measures complete progression sequences rather than isolated line-breaking actions.

### Limitations

Treats all line breaks equally regardless of tactical context.

---

## Transition Burst Possessions

### Soccer Question

How often are transitions converted into rapid territorial advances?

### Tactical Motivation

Fast transitions frequently generate numerical advantages before defenses become organized.

### Computation

Count transition possessions reaching both:

- defensive third
- attacking third

### Interpretation

Higher values indicate explosive transition play.

### Novelty

Measures successful transition sequences instead of simply counting transition events.

### Limitations

Does not evaluate the final attacking outcome.

---

## Stable Build-Up Sequences

### Soccer Question

How consistently can a team construct attacks without structural disruption?

### Tactical Motivation

Successful positional teams often progress from organized build-up into chance creation while maintaining control.

### Computation

Count possessions containing:

- Build-Up
- Create

without entering:

- Chaotic
- Disruption

phases.

### Interpretation

Higher values indicate stable possession structures.

### Novelty

Measures build-up quality rather than possession quantity.

### Limitations

Does not measure tempo or attacking effectiveness.

---

## Pressing Wave Events

### Soccer Question

Can a team sustain coordinated defensive pressure rather than isolated pressing actions?

### Tactical Motivation

Effective pressing typically occurs in coordinated waves rather than individual actions.

### Computation

Identify consecutive pressure events before defensive reset and aggregate sustained waves.

### Interpretation

Higher values indicate sustained coordinated pressure.

### Novelty

Measures pressure continuity rather than pressure frequency.

### Limitations

Does not account for opponent quality or pressing success.

---

## Penetration Diversity Possessions

### Soccer Question

How varied is a team's attacking movement during possession?

### Tactical Motivation

Successful attacks frequently combine multiple coordinated movement patterns.

### Computation

Count possessions containing at least three distinct off-ball run types.

### Interpretation

Higher values indicate greater attacking movement diversity.

### Novelty

Measures coordinated movement variety rather than individual runs.

### Limitations

Does not evaluate whether those movements generated scoring opportunities.

---

# Planned Competition Features

## Territory

- Territory Switching
- Dual Half-Space Possessions

## Progression

- Progressive Build-Up Chains

## Transition

- Transition Continuity

## Pressure

- High Press Recoveries

## Possession

- Long Possession Sequences

## Chance Creation

- Multi-Runner Attacks

## Set Pieces

- Restart Territory Gain

---

# Feature Engineering Philosophy

Every competition feature begins with a tactical question rather than a statistical operation.

The engineering workflow follows the same process for every feature.

```
Soccer Question
        ↓
Tactical Hypothesis
        ↓
Event Relationships
        ↓
Aggregated Feature
        ↓
Interpretation
        ↓
Validation
```

Instead of asking:

> What can be counted?

STIF asks:

> What tactical behavior should be measurable?

This philosophy encourages interpretable features that can support coaching, scouting, tactical research, and future analytical models.

---

# Long-Term Vision

The SkillCorner Soccer Feature Engineering Hackathon submission represents Version 1 of STIF.

The long-term objective is to establish a reusable tactical feature engineering framework capable of supporting:

- coaching
- scouting
- recruitment
- opponent analysis
- tactical research
- historical comparison

through interpretable, reproducible soccer attributes derived entirely from event data.

While the competition submission focuses on a curated set of high-value tactical features, the underlying framework is designed to support continued expansion as new tactical concepts are developed and validated.