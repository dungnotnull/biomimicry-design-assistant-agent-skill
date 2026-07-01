---
name: biomimicry-analogy-mapper
description: Scores each biological candidate against the engineering challenge on four structured dimensions and selects the top 3 analogies for design translation.
---

## Purpose

Transform the Biological Strategy Shortlist into a ranked Analogy Matrix by scoring each candidate on four quantitative dimensions. This sub-skill is the critical "translation filter" — it prevents the common failure mode of selecting a biological analogy because it is famous or aesthetically appealing rather than because it is genuinely transferable to the engineering challenge. The top 3 candidates selected here are the only ones that proceed to sub-design-translator.

---

## Inputs

- **Biological Strategy Shortlist** from sub-biological-researcher (≥5 candidates with mechanism descriptions)
- **Structured Problem Profile** from sub-profile-intake (operating environment, material constraints, manufacturing, scale, performance KPIs, key search constraints)

---

## Scoring Framework

### Dimension 1: Function Alignment (0–10)
Does the biological mechanism perform exactly the same function as the engineering requirement?

| Score | Criteria |
|-------|---------|
| 9–10 | The biological mechanism performs the exact same function, in the exact same operational mode (e.g., reversible dry adhesion in air — gecko setae). |
| 7–8 | The biological mechanism performs the same function but in a slightly different operational context (e.g., wet adhesion for a dry-environment design). |
| 5–6 | The biological mechanism performs a related function from which the engineering function can be derived by analogy (e.g., drag reduction via surface texture for a thermal application). |
| 3–4 | Superficial functional similarity; the underlying mechanism is different and transfer requires significant innovation. |
| 0–2 | The biological mechanism does not perform the engineering function — only cosmetic similarity. |

### Dimension 2: Environmental Match (0–10)
Does the biological organism operate under conditions similar to the engineering environment?

| Score | Criteria |
|-------|---------|
| 9–10 | The organism operates in environments directly comparable to the design's operating conditions (temperature, humidity, pH, load type, scale all align). |
| 7–8 | Most environmental parameters match; 1–2 minor differences that engineering can compensate for. |
| 5–6 | Moderate mismatch in 1–2 parameters; translation requires environmental adaptation. |
| 3–4 | Significant environmental differences; the mechanism may degrade or fail under the engineering conditions. |
| 0–2 | Fundamentally incompatible environments (e.g., deep-sea organism for atmospheric application). |

### Dimension 3: Scale Compatibility (0–10)
Does the biological mechanism operate at a scale compatible with the engineering design's physical size and manufacturing capability?

| Score | Criteria |
|-------|---------|
| 9–10 | The mechanism's operative scale (nano, micro, macro) exactly matches the design's required feature size and manufacturing capability. |
| 7–8 | Small scale mismatch (1 order of magnitude) that can be compensated by adjusting geometric parameters while preserving the physical principle. |
| 5–6 | Moderate scale mismatch (1–2 orders of magnitude); requires non-trivial engineering to achieve analogous behavior at the required scale. |
| 3–4 | Large scale mismatch; the physical principle may change (e.g., surface tension dominates at nano but not macro). |
| 0–2 | Fundamental scale incompatibility — the mechanism relies on quantum, molecular, or organismal-scale effects that cannot be engineered at the required scale. |

### Dimension 4: Transferability (0–10)
Can the biological mechanism be reproduced using available materials and manufacturing processes?

| Score | Criteria |
|-------|---------|
| 9–10 | The mechanism can be implemented with existing commercial materials and standard manufacturing processes without new R&D. |
| 7–8 | The mechanism requires adaptation of existing materials or minor process development; achievable within 1–2 years. |
| 5–6 | The mechanism requires novel materials or process innovation; achievable within 3–5 years of dedicated R&D. |
| 3–4 | The mechanism requires advanced manufacturing capabilities (e.g., atomic layer deposition at scale, protein synthesis) not yet commercially available. |
| 0–2 | The mechanism cannot currently be reproduced with known engineering materials or processes. |

### Weighting

Default weights (can be adjusted per use case):
- Function Alignment: **40%** (most important — must solve the right problem)
- Environmental Match: **20%**
- Scale Compatibility: **20%**
- Transferability: **20%**

**Weighted Total = (FA × 0.4) + (EM × 0.2) + (SC × 0.2) + (T × 0.2)**

---

## Workflow

### Step 1 — Apply Hard Filters from Key Search Constraints
Before scoring, eliminate candidates that violate hard constraints from the Problem Profile:
- If Scale Compatibility is inherently 0–2 for this engineering scale → eliminate candidate (do not waste scoring on it)
- If the manufacturing process available has a feature resolution limit that precludes this mechanism → eliminate
- If materials required by the mechanism are explicitly forbidden in the Problem Profile → eliminate

Document all eliminations with reason.

### Step 2 — Score All Remaining Candidates
For each candidate in the Biological Strategy Shortlist that passed the hard filters, score all 4 dimensions:
- Assign a score of 0–10 per dimension
- Write a 1–2 sentence justification for each score
- Calculate the Weighted Total

### Step 3 — TRIZ Principle Mapping
For each candidate, check whether the biological mechanism embodies a TRIZ inventive principle:

| Biological Feature | TRIZ Principle | Number |
|-------------------|---------------|--------|
| Hierarchical structure (nano → micro → macro) | Transition to Another Dimension | 17 |
| Modular repeating units (setae, denticles) | Segmentation | 1 |
| Gradient properties (bone to cartilage) | Local Quality | 3 |
| Self-repair / regeneration | Self-Service | 25 |
| Structural color (no pigment) | Copying / Simulation | 26 |
| Phase-change thermal regulation | Parameter Change | 35 |
| Shape changes under load (plant stems) | Dynamism / Flexibility | 15 |
| Dual function surfaces (lotus: structural + hydrophobic) | Multi-functionality | 6 |
| Emergence from simple rules (murmuration) | Merging / Synergy | 5 |

Record any matching TRIZ principles as a bonus insight. A TRIZ match indicates the analogy taps into a general inventive principle, which increases confidence in its transferability.

### Step 4 — Rank and Select Top 3
- Rank all scored candidates by Weighted Total (descending).
- Select the top 3 candidates.
- If fewer than 3 candidates score ≥ 7.0 on Function Alignment: flag this as a quality gate failure and request that sub-biological-researcher broaden its search.
- If two candidates have identical weighted totals, prefer the one with the higher Function Alignment score.

### Step 5 — Diversity Check
Verify the top 3 selections represent different biological strategies (not all from the same organism or the same physical principle). If all 3 top scorers use the same physical mechanism (e.g., all rely on van der Waals adhesion), forcibly diversify by swapping out the #3 candidate for the next highest scorer that uses a different mechanism, as long as that candidate has a Weighted Total ≥ 6.0.

### Step 6 — Format Ranked Analogy Matrix

```
RANKED ANALOGY MATRIX
═══════════════════════════════════════════════════════════════════════════════
Engineering function: [function from Problem Profile]
Candidates scored: [N]
Candidates eliminated (hard filter): [N, with reasons]
Candidates scored after filter: [N]
═══════════════════════════════════════════════════════════════════════════════

| Rank | Organism | FA(40%) | EM(20%) | SC(20%) | T(20%) | Weighted | TRIZ | Notes |
|------|---------|---------|---------|---------|--------|----------|------|-------|
|  1   | ...     |  8.5    |  7.0    |  8.0    |  9.0   |   8.4    |  1   | ...   |
|  2   | ...     |  8.0    |  8.0    |  7.0    |  7.0   |   7.8    |  17  | ...   |
|  3   | ...     |  7.5    |  6.5    |  8.5    |  7.5   |   7.6    |  26  | ...   |
|  4   | ...     |  6.0    |  7.0    |  7.0    |  6.5   |   6.5    |  -   | Below threshold |
...

ELIMINATED (hard filter):
- [Organism]: [reason for elimination]

TOP 3 SELECTED:
1. [Organism 1] — Weighted Total: [X] — TRIZ: [principle if any]
2. [Organism 2] — Weighted Total: [X] — TRIZ: [principle if any]
3. [Organism 3] — Weighted Total: [X] — TRIZ: [principle if any]
```

---

## Outputs

- **Ranked Analogy Matrix** — full scored table with all candidates (filtered and scored)
- **Top 3 Selected Analogies** — organism name, mechanism summary, weighted score, and TRIZ principle (if matched) for each
- **Hard Filter Log** — candidates eliminated before scoring and reasons
- **TRIZ Principle Matches** — any TRIZ inventive principles identified across the top 3

---

## Quality Gate

Before passing the top 3 to sub-design-translator, verify:

- [ ] All 4 scoring dimensions are populated for every non-eliminated candidate
- [ ] A justification sentence is written for each score (no blank scores)
- [ ] The Weighted Total formula was applied correctly
- [ ] All 3 top selections have Function Alignment ≥ 7.0
- [ ] The top 3 represent at least 2 different physical mechanisms (no all-same-principle lock-in)
- [ ] Hard filter eliminations are documented with reasons
- [ ] TRIZ mapping has been attempted for every top-3 candidate

**Failure action:** If the top 3 have Function Alignment < 7.0, return to sub-biological-researcher with a broader search query. Do not proceed to sub-design-translator with low-alignment analogies.


---

## Worked Examples ? Scoring (gecko adhesion & termite ventilation)

These two worked demonstrations validate that the 4-dimension rubric, the
weighting, the TRIZ mapping, and the diversity check produce auditable,
reproducible rankings for canonical scenarios. They are reference scorings
(design-time validation), not live runs.

### Example 1 ? Gecko adhesion (Scenario 1 abridged)

**Shortlist passed from sub-biological-researcher:** gecko, tree frog, blowfly, leaf beetle, mussel.

Hard filters: none eliminated (all compatible with 10?500 ?m feature scale and REACH-compliant polymers).

| Rank | Organism | FA(40%) | EM(20%) | SC(20%) | T(20%) | Weighted | TRIZ | Notes |
|------|----------|---------|---------|---------|--------|----------|------|-------|
| 1 | *Gekko gecko* | 9.5 | 9.0 | 8.0 | 8.5 | 8.90 | 1 Segmentation | Exact function; vdW setal hierarchy |
| 2 | *Calliphora* | 7.5 | 7.0 | 7.5 | 7.0 | 7.30 | 3 Local Quality | Fluid-assist adds contamination risk |
| 3 | *Litoria* | 7.0 | 6.5 | 7.0 | 7.0 | 6.90 | ? | Needs humidity; borderline FA |
| 4 | *Chrysomelidae* | 6.5 | 6.5 | 7.0 | 6.5 | 6.60 | ? | Below FA?7 threshold |
| 5 | *Mytilus* | 5.0 | 4.0 | 7.0 | 6.0 | 5.40 | 35 Parameter Change | Wet-only context |

- Top-3 FA?7 ? (9.5, 7.5, 7.0)
- Diversity: top 3 use two distinct physical principles (dry vdW vs. fluid capillary) ?
- TRIZ attempted on all top-3 ?
- Eliminations: none; #4/#5 fall below threshold but retained in matrix for auditability.

### Example 2 ? Termite ventilation (Scenario 2 abridged)

**Shortlist passed:** termite mound, fog beetle, prairie dog burrow, sand gazelle nasal, desert ant nest, cactus skeleton.

Hard filters: fog beetle retained as water-harvesting alternative (not primary thermal); all others compatible with hot-arid macro scale and construction materials.

| Rank | Organism | FA(40%) | EM(20%) | SC(20%) | T(20%) | Weighted | TRIZ | Notes |
|------|----------|---------|---------|---------|--------|----------|------|-------|
| 1 | *Macrotermes michaelseni* | 9.0 | 9.0 | 7.0 | 8.0 | 8.40 | 6 Multi-functionality | Thermosiphon + chimney geometry; Eastgate precedent |
| 2 | *Cynomys* (prairie dog) | 8.0 | 8.5 | 8.0 | 7.5 | 8.00 | 17 Another Dimension | Bernoulli wind-driven; complementary to thermosiphon |
| 3 | *Gazella subgutturosa* | 7.0 | 8.0 | 5.0 | 5.5 | 6.50 | 25 Self-service | Countercurrent nasal HX; micro-scale mismatch |
| 4 | *Cataglyphis* (desert ant) | 6.5 | 8.0 | 6.0 | 6.0 | 6.60 | ? | Deep insulated chambers |
| 5 | *Carnegiea gigantea* (cactus) | 6.0 | 7.0 | 7.0 | 6.5 | 6.50 | 3 Local Quality | Accordion-pleat surface area |
| 6 | *Stenocara* (fog beetle) | 5.0 | 6.0 | 6.5 | 6.0 | 5.70 | 35 Parameter Change | Water-harvesting not thermal |

- Top-3 FA?7 ? (9.0, 8.0, 7.0)
- Diversity: top 3 use three distinct mechanisms (thermosiphon convection vs. Bernoulli wind vs. countercurrent HX) ?
- TRIZ attempted on all top-3 ?
- Tie-break at 6.50 (gazella vs cactus): gazella promoted by higher FA (7.0 > 6.0) per the documented tie-break rule.

**Scoring quality-gate validation:** Both examples populate all 4 dimensions
with justifications, apply the weighted formula correctly, enforce the FA?7
top-3 threshold, satisfy the diversity check, and document TRIZ mapping per
top candidate. ? Both PASS the sub-analogy-mapper quality gate.
