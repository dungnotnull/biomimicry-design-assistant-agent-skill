---
name: biomimicry-biological-researcher
description: Searches AskNature taxonomy, ArXiv, and domain biology journals to identify organisms and natural structures that solve the same functional problem as the user's engineering challenge.
---

## Purpose

Conduct a rigorous, multi-source literature search to discover biological strategies that perform the same function as the engineering challenge. The output is a Biological Strategy Shortlist of at least 5 candidates, each with a verified peer-reviewed or AskNature citation, covering at least 3 distinct taxonomic groups. This sub-skill never invents biological analogies from memory — every entry must be traceable to a citable source.

---

## Inputs

- **Structured Problem Profile** from sub-profile-intake, specifically:
  - Required Function (engineering phrasing)
  - AskNature Function Translation (vocabulary for AskNature search)
  - Operating Environment (constrains which biological contexts are relevant)
  - Key Search Constraints (hard filters for relevance)

---

## Workflow

### Step 1 — Formulate Search Queries

Construct queries for each source using the AskNature Function Translation as the primary vocabulary:

**AskNature Query:**
```
Search: https://asknature.org/strategy/[function-keyword]/
Example: https://asknature.org/strategy/attach/
         https://asknature.org/strategy/regulate-temperature/
```

**ArXiv Queries (q-bio.PE, cond-mat.mtrl-sci, and cs.RO):**
```
WebSearch: arxiv q-bio.PE "[AskNature function]" biomimicry OR "bio-inspired"
WebSearch: arxiv cond-mat.mtrl-sci "[material property]" bio-inspired 2022 2023 2024 2025
WebSearch: arxiv cs.RO "[locomotion / sensing / actuation function]" "bio-inspired" OR "biomimetic" robot
```

**Journal of Bionic Engineering:**
```
WebSearch: "Journal of Bionic Engineering" "[function keyword]" site:sciencedirect.com
```

**Bioinspiration & Biomimetics (IOP):**
```
WebSearch: "Bioinspiration Biomimetics" "[function keyword]" site:iopscience.iop.org
```

**Semantic Scholar (backup):**
```
WebSearch: semanticscholar.org "[function]" "biological" OR "organism" engineering analogy
```

**SECOND-KNOWLEDGE-BRAIN.md (offline fallback):**
- If WebSearch is unavailable, search the Key Research Papers table and Case Studies in SECOND-KNOWLEDGE-BRAIN.md.
- Clearly flag in the output: "Source: SECOND-KNOWLEDGE-BRAIN (offline — no live search performed)".

### Step 2 — Environmental Constraint Filtering

Apply the Operating Environment filter from the Problem Profile:
- If environment is **aquatic/marine** → prioritize marine organisms (fish, mollusks, crustaceans, marine algae)
- If environment is **hot and dry** → prioritize desert organisms (cacti, desert beetles, scorpions, camels)
- If environment is **high humidity/wet** → prioritize tropical organisms, amphibians, aquatic invertebrates
- If environment is **high UV exposure** → prioritize high-altitude or desert organisms with UV adaptation
- If environment is **high mechanical load** → prioritize load-bearing biological structures (bone, shell, wood, tendons)
- If environment is **micro-scale** → focus on cellular/subcellular mechanisms

Remove any biological candidate that operates in an incompatible environment from the shortlist.

### Step 3 — Collect Biological Candidates

For each retrieved source, extract the following information:

| Field | What to Record |
|-------|---------------|
| **Organism** | Scientific name + common name |
| **Taxonomic Group** | Kingdom → Phylum → Class (at least to Class level) |
| **Mechanism** | How does the organism perform the function? (2–3 sentence description of the physical/chemical mechanism) |
| **Key Parameters** | Size scales, material composition, geometry (if reported) |
| **Function** | What function does this mechanism serve for the organism? |
| **Environmental Context** | In which environment does the organism use this mechanism? |
| **Evidence Tier** | Peer-Reviewed / AskNature / Case Study / Expert Opinion / Popular Science |
| **Citation** | Author, Year, Journal/Source, DOI or URL |

Aim for a diverse shortlist — apply these diversity rules:
- **Taxonomic diversity:** At least 3 different phyla represented (e.g., Arthropoda, Vertebrata, Plantae)
- **Mechanism diversity:** Not all candidates should use the same physical principle (e.g., if 3 use adhesion via van der Waals, also search for capillary adhesion, interlocking, or chemical bonding mechanisms)
- **Scale diversity:** Where possible, include mechanisms from different scale levels (nano, micro, macro)

### Step 4 — Evidence Quality Check

For each candidate, verify:
- **Peer-reviewed source:** Is the mechanism described in a journal article with DOI? (Preferred tier)
- **AskNature entry:** Is there an AskNature strategy page describing this mechanism? (Acceptable tier)
- **Case study only:** Is the only source a product case study or news article? (Flag as low-evidence; include only if no better source exists)

Reject any candidate that cannot be traced to at least a case study-level source. Never include a biological analogy from memory without citation.

### Step 5 — SECOND-KNOWLEDGE-BRAIN Cross-Reference

Search `SECOND-KNOWLEDGE-BRAIN.md` (specifically the Famous Biomimicry Case Studies table) to:
- Identify if any classic case study directly matches the engineering function.
- Add matching classic cases to the shortlist with their original citations.
- Flag classic cases as "well-established analogy" for prioritization in sub-analogy-mapper.

### Step 6 — Compile and Format the Biological Strategy Shortlist

Format the complete shortlist as a table:

```
BIOLOGICAL STRATEGY SHORTLIST
═══════════════════════════════════════════════════════════════════════
Function searched: [AskNature functional vocabulary]
Engineering function: [original user phrasing]
Total candidates found: [N]
Candidates included: [N≥5]
Taxonomic groups covered: [list]
═══════════════════════════════════════════════════════════════════════

| # | Organism | Taxonomic Group | Mechanism (summary) | Environment | Evidence Tier | Citation |
|---|---------|----------------|--------------------|-----------|---------|----|
| 1 | ... | ... | ... | ... | Peer-Reviewed | Author (Year) DOI |
| 2 | ... | ... | ... | ... | AskNature | URL |
...

NOTES:
- Candidates marked [CLASSIC] are well-established biomimicry case studies.
- Candidates marked [LOW-EVIDENCE] have only case study or popular science sources.
- Candidates marked [OFFLINE] were retrieved from SECOND-KNOWLEDGE-BRAIN without live search.
```

---

## Outputs

- **Biological Strategy Shortlist** — formatted table with ≥5 candidates, organism, mechanism, environment, evidence tier, and citation for each
- **Search Coverage Report** — which sources were searched and how many results each returned (used for transparency and reproducibility)
- **Taxonomic Diversity Summary** — confirms ≥3 phyla represented

---

## Quality Gate

Before passing the shortlist to sub-analogy-mapper, verify:

- [ ] At least 5 biological strategies are documented in the shortlist
- [ ] At least 3 different taxonomic groups (phyla) are represented
- [ ] Every entry has at least one cited source (peer-reviewed, AskNature, or case study)
- [ ] At least 3 entries are supported by peer-reviewed or AskNature sources (not just case studies)
- [ ] Mechanism descriptions are specific enough to extract geometric parameters (not just "bird has streamlined beak")
- [ ] The Environmental Constraint filter was applied (no candidates from incompatible environments)
- [ ] If web search was unavailable, this limitation is documented with [OFFLINE] flags

**Failure action:** If fewer than 5 candidates are found with the primary AskNature function term, broaden the search using related function terms (e.g., if "attach in wet conditions" yields only 3, also search "bind," "fasten," and "adhere"). If only offline sources were used, flag the entire shortlist as "Reduced confidence — live search unavailable."
