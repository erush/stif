# STIF Feature Backlog

## Purpose

This document captures the tactical feature roadmap for STIF.

Features listed here represent future engineering work beyond the initial feature set. Every proposed feature is intended to satisfy the goals of the SkillCorner Soccer Feature Engineering Hackathon:

- Novel
- Interpretable
- Aggregated
- Reproducible
- Tactically meaningful

Each feature should ultimately become:

- a FeatureSpec
- documented methodology
- reproducible SQL implementation
- exported feature column
- evaluation entry
- write-up section

---

# Priority Definitions

| Priority | Meaning |
|----------|---------|
| ★★★★★ | Must implement before submission |
| ★★★★☆ | Strong candidate |
| ★★★☆☆ | Valuable extension |
| ★★☆☆☆ | Future work |
| ★☆☆☆☆ | Research idea |

---

# Territory Domain

## Territorial Persistence

Priority: ★★★★★

### Concept

Measures sustained occupation of the attacking third.

### Motivation

Attacking pressure is not simply entering the final third—it is remaining there.

### Proposed Computation

Count possessions containing multiple consecutive attacking-third engagements before leaving.

### Interpretation

Higher values indicate sustained territorial control.

Status: Planned

---

## Deep Territory Progressions

Priority: ★★★★★

### Concept

Possessions beginning in the defensive third and eventually reaching the attacking third.

### Interpretation

Measures complete-field progression.

Status: Planned

---

## Territory Switching

Priority: ★★★★☆

### Concept

Counts lateral movement between channels during possession.

Example

Wide Left

↓

Center

↓

Wide Right

↓

Half Space

### Interpretation

Measures ability to manipulate defensive shape.

Status: Planned

---

## Central Occupation Sequences

Priority: ★★★☆☆

Counts repeated center-channel occupation during possessions.

Status: Planned

---

## Half-Space Dominance

Priority: ★★★★☆

Counts possessions utilizing both half spaces.

Status: Planned

---

# Progression Domain

## Multi-Line Progressions

Priority: ★★★★★

### Concept

Possessions breaking

- First line
- Second line
- Last line

within one attacking sequence.

Interpretation

Measures complete progression through defensive structure.

Status: Planned

---

## Progressive Build-Up Chains

Priority: ★★★★★

Multiple forward trajectories during build-up.

Status: Planned

---

## Vertical Progression Volume

Priority: ★★★★☆

Forward progressions before entering attacking third.

Status: Planned

---

## Progressive Variety

Priority: ★★★☆☆

Different progression mechanisms used within one possession.

Status: Planned

---

# Transition Domain

## Transition Burst

Priority: ★★★★★

### Concept

Rapid advancement through multiple thirds during one possession.

Interpretation

Measures transition speed.

Status: Planned

---

## Transition Continuity

Priority: ★★★★★

Chains of

Direct

↓

Quick Break

↓

Finish

Status: Planned

---

## Chaotic Recoveries

Priority: ★★★★☆

Recoveries immediately following chaotic phases.

Status: Planned

---

## Counter Transition Frequency

Priority: ★★★☆☆

Transitions initiated immediately after regaining possession.

Status: Planned

---

# Pressure Domain

## Pressing Waves

Priority: ★★★★★

### Concept

Consecutive pressure events before defensive reset.

Interpretation

Measures sustained pressing.

Status: Planned

---

## High Press Recoveries

Priority: ★★★★★

Recoveries following high-block pressure.

Status: Planned

---

## Counter-Press Chains

Priority: ★★★★☆

Multiple counter-press events during one defensive sequence.

Status: Planned

---

## Pressure Escalation

Priority: ★★★☆☆

Pressure intensity increasing during defensive sequences.

Status: Planned

---

# Possession Domain

## Stable Build-Up

Priority: ★★★★★

### Concept

Build-up phases successfully reaching Create phase without disruption.

Interpretation

Measures clean build-up.

Status: Planned

---

## Long Possession Chains

Priority: ★★★★★

Counts long possession sequences.

Status: Planned

---

## Possession Recycling

Priority: ★★★★☆

Backward

↓

Forward

↓

Backward

circulation patterns.

Status: Planned

---

## Controlled Progressions

Priority: ★★★☆☆

Forward progressions occurring without possession loss.

Status: Planned

---

# Chance Creation Domain

## Penetration Diversity

Priority: ★★★★★

### Concept

Distinct off-ball run types within possessions.

Interpretation

Measures attacking creativity.

Status: Planned

---

## Multi-Runner Attacks

Priority: ★★★★★

Possessions containing multiple coordinated run types.

Example

Support

+

Overlap

+

Run Ahead

Status: Planned

---

## Receiving Diversity

Priority: ★★★★☆

Different receiving movements within possessions.

Status: Planned

---

## Wide-to-Central Attacks

Priority: ★★★☆☆

Attacks transitioning from wide areas into central zones.

Status: Planned

---

# Set Piece Domain

## Restart Territory Gain

Priority: ★★★★★

### Concept

Territory gained immediately after throw-ins, corners, goal kicks or free kicks.

Interpretation

Measures effectiveness of restart structure.

Status: Planned

---

## Restart Pressure

Priority: ★★★★☆

Pressure generated immediately after attacking restarts.

Status: Planned

---

## Set Piece Momentum

Priority: ★★★☆☆

Multiple attacking restarts occurring within one attacking spell.

Status: Planned

---

## Defensive Restart Stability

Priority: ★★★☆☆

Successful defensive restarts avoiding immediate pressure.

Status: Planned

---

# Candidate Feature Ranking

| Feature | Domain | Novelty | Tactical Value | Difficulty | Priority |
|----------|--------|----------|----------------|------------|----------|
| Territorial Persistence | Territory | High | High | Medium | ★★★★★ |
| Deep Territory Progressions | Territory | High | High | Low | ★★★★★ |
| Multi-Line Progressions | Progression | High | High | Medium | ★★★★★ |
| Progressive Build-Up Chains | Progression | Medium | High | Medium | ★★★★★ |
| Transition Burst | Transition | High | High | Medium | ★★★★★ |
| Transition Continuity | Transition | High | High | Medium | ★★★★★ |
| Pressing Waves | Pressure | High | High | Medium | ★★★★★ |
| High Press Recoveries | Pressure | High | High | Low | ★★★★★ |
| Stable Build-Up | Possession | High | High | Medium | ★★★★★ |
| Long Possession Chains | Possession | Medium | High | Low | ★★★★★ |
| Penetration Diversity | Chance Creation | High | High | Medium | ★★★★★ |
| Multi-Runner Attacks | Chance Creation | High | High | Medium | ★★★★★ |
| Restart Territory Gain | Set Pieces | High | High | Medium | ★★★★★ |

---

# Guiding Principles

Every feature added to STIF should satisfy the following requirements:

- Derived from SkillCorner event or phase-of-play data only.
- Aggregated at the match/team level.
- Fully reproducible.
- Easily interpretable by analysts and coaches.
- Capture meaningful tactical behavior rather than simple event totals.
- Avoid normalized values, percentages, ratios, or machine-learned representations.
- Be implementable through the declarative FeatureSpec registry.
- Integrate with the feature engine, documentation generator, evaluation framework, and tactical profile system.

---

# Long-Term Vision

The initial STIF submission focuses on approximately 20–50 high-quality engineered features for the Kaggle Soccer Feature Engineering Hackathon.

Following the competition, this backlog serves as the roadmap for expanding STIF into a comprehensive tactical intelligence platform capable of supporting scouting, coaching, research, and match analysis through increasingly rich, interpretable soccer attributes.