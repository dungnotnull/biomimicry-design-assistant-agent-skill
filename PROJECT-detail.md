# PROJECT-detail.md — Biomimicry Design Assistant (Skill 243)

## Executive Summary

The **Biomimicry Design Assistant** is a structured harness skill that helps engineers, product designers, and R&D teams discover nature-proven solutions to technical challenges. By systematically querying the biological world using AskNature's functional taxonomy, peer-reviewed evolutionary biology, and biomaterials literature, the skill identifies organisms and natural structures that have already solved analogous engineering problems over millions of years of selection pressure. It scores each biological analogy for functional alignment and manufacturing transferability, then translates the top candidates into concrete engineering design specifications — including material analogues, processing routes, geometric parameters, and performance benchmarks — grounded in Janine Benyus's Life's Principles and TRIZ bio-inspired heuristics.

---

## Problem Statement

Engineering design is constrained by what designers already know. Conventional solution search (patent databases, standards, textbooks) samples only human-invented solutions from the last few centuries. Nature has been solving analogous structural, fluidic, thermal, adhesive, optical, and mechanical problems for 3.8 billion years under strict resource constraints. The gap between biological knowledge and engineering practice is primarily a translation problem: engineers cannot easily access biological literature, and biologists rarely frame their findings in engineering terms.

Existing tools (AskNature, BioMimicry Institute resources) provide databases of biological strategies but offer no structured workflow for:
1. Mapping a specific engineering function to the correct biological analogy
2. Scoring analogies by transferability given real manufacturing constraints
3. Translating biological mechanisms into production-grade engineering specifications
4. Keeping domain knowledge current with the latest biomimicry research

This skill fills that gap with a four-stage harness that takes the user from problem statement to professional Biomimicry Design Brief.

---

## Target Users & Use Cases

| User | Trigger | Skill Does |
|------|---------|-----------|
| Mechanical engineer | "I need a lightweight structural connector that can flex 50,000 cycles without fatigue" | Finds insect exoskeletal joints, bone trabecular architecture, and plant stem flexure zones; maps to composite layup specs |
| Materials scientist | "I need a dry adhesive that works on rough, wet, and curved surfaces" | Identifies gecko setal arrays, mussel adhesion proteins, and sandcastle worm cement; scores transferability; recommends nano-fabrication routes |
| Architect / HVAC engineer | "Passive ventilation for a 20-story building in a hot, dry climate" | Maps to termite mound thermosiphon, Namibian fog beetle, and lotus leaf thermal emittance; produces HVAC design brief |
| Textile/apparel engineer | "Reduce fluid drag on swimwear without adding rigid structures" | References shark denticle geometry, dolphin skin microstructure; outputs fabric texture spec and manufacturing tolerances |
| Robotics engineer | "Locomotion on loose granular media (sand/gravel)" | Finds sandfish lizard undulation, desert ant gait, and octopus arm compliance; translates to actuator control strategy |
| Packaging designer | "Structural packaging that can absorb high-impact shocks with minimum material" | Maps to woodpecker cranial bone, pomelo peel hierarchy, mantis shrimp telson; produces foam density gradient spec |

---

## Harness Architecture

```
/biomimicry-design-assistant
        │
        ▼
┌─────────────────────────────┐
│  STAGE 1: sub-profile-intake│  ← Structured intake: challenge, constraints, requirements, sustainability
└────────────┬────────────────┘
             │ Structured Problem Profile
             ▼
┌────────────────────────────────────┐
│  STAGE 2: sub-biological-researcher│  ← AskNature taxonomy + ArXiv + domain journals → biological candidates
└────────────┬───────────────────────┘
             │ Biological Strategy Shortlist (≥5 candidates)
             ▼
┌──────────────────────────────┐
│  STAGE 3: sub-analogy-mapper │  ← Function alignment + transferability scoring → ranked analogy matrix
└────────────┬─────────────────┘
             │ Top 3 Biological Analogies (scored)
             ▼
┌──────────────────────────────────┐
│  STAGE 4: sub-design-translator  │  ← Mechanism → engineering spec → material analogue → process route
└────────────┬─────────────────────┘
             │ Draft Design Specifications
             ▼
┌─────────────────────────────────────┐
│  QUALITY GATE: Life's Principles    │  ← Check all 6 Life's Principles categories; require evidence citations
│  + Evidence Audit                   │
└────────────┬────────────────────────┘
             │ Validated Specifications
             ▼
┌─────────────────────────────────────┐
│  FINAL OUTPUT: Biomimicry Design    │  ← Professional design brief with scores, specs, roadmap, references
│  Brief                              │
└─────────────────────────────────────┘
```

---

## Full Sub-Skill Catalog

### sub-profile-intake
- **Purpose:** Elicit and structure the complete engineering problem profile before any biological search begins.
- **Inputs:** Free-text problem description from user
- **Outputs:** Structured Problem Profile JSON — function required, operating environment, material constraints, manufacturing process, scale, performance KPIs, sustainability goals, budget tier
- **Tools:** Read (SECOND-KNOWLEDGE-BRAIN for domain hints), Write (save profile)
- **Quality Gate:** All 8 profile fields populated; ambiguous constraints flagged and clarified with user

### sub-biological-researcher
- **Purpose:** Search AskNature taxonomy and peer-reviewed literature for organisms/structures solving the analogous biological function.
- **Inputs:** Structured Problem Profile (function, environment, constraints)
- **Outputs:** Biological Strategy Shortlist — minimum 5 entries, each with organism, mechanism description, function, source citation, AskNature URL or DOI
- **Tools:** WebSearch (AskNature, ArXiv q-bio, Journal of Bionic Engineering), WebFetch (full abstracts), Read (SECOND-KNOWLEDGE-BRAIN)
- **Quality Gate:** Each entry has ≥1 peer-reviewed or AskNature citation; at least 3 different taxonomic groups represented

### sub-analogy-mapper
- **Purpose:** Rigorously score each biological candidate against the engineering function using structured analogy dimensions.
- **Inputs:** Biological Strategy Shortlist + Structured Problem Profile
- **Outputs:** Ranked Analogy Matrix — each entry scored on Function Alignment (0–10), Environmental Match (0–10), Scale Compatibility (0–10), Transferability (0–10), Weighted Total; top 3 selected
- **Tools:** Read (SECOND-KNOWLEDGE-BRAIN for TRIZ principles), WebSearch (transferability case studies)
- **Quality Gate:** All 4 scoring dimensions populated for every candidate; top 3 have Function Alignment ≥ 7

### sub-design-translator
- **Purpose:** Translate the top biological analogies into engineering specifications with materials, geometry, manufacturing, and performance targets.
- **Inputs:** Top 3 ranked biological analogies + Structured Problem Profile
- **Outputs:** Engineering Design Specification — for each analogy: mechanism description, key geometric parameters, material analogue (natural vs. synthetic), manufacturing route, estimated performance range, existing products/patents, Life's Principles compliance score, implementation effort (Low/Medium/High)
- **Tools:** WebSearch (biomaterials databases, patent search, existing products), WebFetch (patent abstracts), Read (SECOND-KNOWLEDGE-BRAIN)
- **Quality Gate:** Each spec includes material analogue, manufacturing route, ≥1 real-world precedent or patent reference

---

## Skill File Format Specification

### Frontmatter Schema
```yaml
---
name: biomimicry-design-assistant
description: Structured biomimicry workflow — maps engineering challenges to nature's proven solutions and produces production-ready design specifications
---
```

### Required Sections in main.md
1. `## Role & Persona` — domain expert identity
2. `## Workflow` — numbered steps invoking sub-skills
3. `## Sub-skills Available` — list with file references
4. `## Tools` — tool list
5. `## Output Format` — exact structure of final deliverable
6. `## Quality Gates` — checklist before final output

---

## E2E Execution Flow

```
1. User invokes /biomimicry-design-assistant [optional: problem description]
2. Harness runs sub-profile-intake → structured Problem Profile
3. Harness runs sub-biological-researcher using Problem Profile function field
   3a. Query AskNature by function keyword (e.g. "attachment," "thermal regulation")
   3b. Query ArXiv q-bio.PE and cond-mat.mtrl-sci
   3c. Query Journal of Bionic Engineering and Bioinspiration & Biomimetics
   3d. Filter: only include organisms where the mechanism is described in detail
   3e. Build Biological Strategy Shortlist (≥5 entries)
4. Harness runs sub-analogy-mapper
   4a. For each candidate, score 4 dimensions (Function Alignment, Environmental Match, Scale Compatibility, Transferability)
   4b. Apply TRIZ bio-principle filter (does this mechanism leverage an inventive principle?)
   4c. Select top 3 by weighted score
5. Harness runs sub-design-translator on top 3
   5a. Identify key geometric parameters from biology literature
   5b. Map to synthetic material analogues (e.g. chitin → carbon fiber; nacre → ceramic composite)
   5c. Identify applicable manufacturing routes (3D printing, electrospinning, soft lithography, etc.)
   5d. Search patent database for existing bio-inspired implementations
   5e. Calculate Life's Principles compliance for each spec
6. Quality Gate:
   6a. All 6 Life's Principles categories evaluated
   6b. Every biological claim has a citation
   6c. Every engineering spec has a manufacturing route
   6d. Devil's advocate check: what are the key failure modes of each translation?
7. Synthesize final Biomimicry Design Brief
   7a. Executive summary (problem + recommended strategy)
   7b. Biological strategy comparison table
   7c. Full engineering spec for top recommendation
   7d. Alternative specs for #2 and #3
   7e. Implementation roadmap (Proof of Concept → Prototype → Pilot)
   7f. Life's Principles compliance matrix
   7g. References (all citations)
```

---

## SECOND-KNOWLEDGE-BRAIN Integration

**Sources:** ArXiv q-bio.PE, cond-mat.mtrl-sci, cs.RO; AskNature.org; Journal of Bionic Engineering; Bioinspiration & Biomimetics; Nature Materials; Semantic Scholar

**Crawl Config:**
- Keywords: "biomimicry," "biologically inspired design," "bio-inspired materials," "evolutionary optimization," "natural structures engineering"
- Frequency: Weekly (Sunday 02:00 UTC)
- Append Format: `| Title | Authors | Year | Venue | DOI | Relevance |`
- Deduplication: DOI hash check

**Append Protocol:** `tools/knowledge_updater.py` fetches, parses, scores, deduplicates, and appends to the `## Key Research Papers` table in `SECOND-KNOWLEDGE-BRAIN.md`.

---

## Quality Gates Definition

Before the final Biomimicry Design Brief is presented, ALL of the following must be true:

1. **Profile complete:** All 8 Problem Profile fields populated
2. **Biological coverage:** ≥5 distinct biological strategies identified, ≥3 taxonomic groups
3. **Citation coverage:** Every biological mechanism cites a peer-reviewed source or AskNature entry
4. **Scoring complete:** All 4 analogy dimensions scored for every candidate
5. **Top-3 quality:** Top 3 analogies have Function Alignment ≥ 7/10
6. **Spec completeness:** Each engineering spec includes material analogue + manufacturing route + precedent/patent
7. **Life's Principles:** All 6 Life's Principles categories evaluated for the primary recommendation
8. **Devil's advocate:** Failure modes and limitations documented for each translation
9. **Evidence hierarchy:** All claims ranked by evidence tier (peer-reviewed > AskNature > case study > popular science)

---

## Test Scenarios

See `tests/test-scenarios.md` for 5+ concrete test scenarios.

---

## Key Design Decisions

1. **Function-first search:** The search is always led by the engineering function (e.g. "attachment in wet conditions"), not by guessing which organism to copy. This follows AskNature's taxonomy and avoids naive mimicry.
2. **Structured scoring over intuition:** The 4-dimension scoring rubric (Function Alignment, Environmental Match, Scale Compatibility, Transferability) makes the analogy selection reproducible and auditable.
3. **TRIZ integration:** TRIZ bio-inspired principles (e.g. "Parameter Change," "Self-Service," "Dynamism") are checked against each biological strategy to identify cross-domain inventive insight.
4. **Life's Principles as a compliance gate:** Every proposed design is evaluated against all 6 of Janine Benyus's Life's Principles before it can be included in the final brief. This ensures sustainability alignment.
5. **Evidence hierarchy enforcement:** The skill explicitly tags each biological claim with its evidence tier and flags when only low-tier evidence is available.
6. **Manufacturing reality check:** Sub-skill sub-design-translator is specifically designed to prevent "beautiful biology, impossible engineering" — it requires a manufacturable process route for every spec.
7. **Self-improving knowledge base:** Weekly crawl of ArXiv + domain journals ensures the skill's biological analogy pool grows continuously without manual curation.
