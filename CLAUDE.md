# CLAUDE.md — Skill 243: Biomimicry Design Assistant

## Skill Identity
- **Skill Name:** biomimicry-design-assistant
- **Tagline:** Find nature's proven engineering solutions and translate them into production-ready design specifications.
- **Current Phase:** Production-ready - Phases 0-5 complete (design-validated; live-run deferred to production stage)
- **Source Idea Number:** 243
- **Cluster:** science-industry

---

## Problem This Skill Solves

Engineers frequently reinvent solutions that nature solved over billions of years of evolutionary optimization. The Biomimicry Design Assistant bridges the gap between biological knowledge and engineering practice by systematically searching the living world for analogous strategies, mapping them to the user's engineering challenge, scoring their transferability, and translating biological mechanisms into concrete design specifications. The skill is grounded in Janine Benyus's Biomimicry 3.8 Life's Principles, the AskNature functional taxonomy, TRIZ bio-inspired heuristics, and the Biologically Inspired Design (BID) methodology — and it continuously ingests new research from ArXiv, Journal of Bionic Engineering, and Bioinspiration & Biomimetics.

---

## Harness Flow Summary

```
/biomimicry-design-assistant invoked
  Step 1 → sub-profile-intake         : Capture engineering challenge, constraints, performance targets, sustainability goals
  Step 2 → sub-biological-researcher  : Search AskNature + literature for organisms solving analogous problems
  Step 3 → sub-analogy-mapper         : Score and rank biological analogies by function alignment and transferability
  Step 4 → sub-design-translator      : Translate top analogies into engineering specs, materials, manufacturing routes
  Step 5 → Quality Gate Review        : Verify Life's Principles compliance, evidence citations, design completeness
  Step 6 → Main Harness               : Synthesize final Biomimicry Design Brief
```

---

## Sub-Skills

| File | Description |
|------|-------------|
| `skills/sub-profile-intake.md` | Collects and structures the engineering problem statement, constraints, requirements, and sustainability goals |
| `skills/sub-biological-researcher.md` | Searches AskNature and peer-reviewed literature for organisms/structures solving analogous problems |
| `skills/sub-analogy-mapper.md` | Maps biological functions to engineering functions; scores analogies by relevance and transferability |
| `skills/sub-design-translator.md` | Translates biological mechanisms into engineering specifications, material analogues, and manufacturing routes |

---

## Tools Required
- **WebSearch** — search ArXiv, AskNature, Journal of Bionic Engineering, Bioinspiration & Biomimetics
- **WebFetch** — retrieve full-text abstracts and AskNature strategy pages
- **Read** — access SECOND-KNOWLEDGE-BRAIN.md for cached knowledge
- **Write** — produce the final Biomimicry Design Brief deliverable
- **Bash** — run `tools/knowledge_updater.py` for scheduled knowledge updates

---

## Knowledge Sources
- **ArXiv:** `q-bio.PE` (populations & evolution), `cond-mat.mtrl-sci` (biomaterials), `cs.RO` (bio-inspired robotics)
- **AskNature.org** — AskNature Strategy Database (function-organized biological strategies)
- **Journal of Bionic Engineering** (ScienceDirect)
- **Bioinspiration & Biomimetics** (IOP Publishing)
- **Nature Materials** — news & research articles
- **Semantic Scholar** — keyword searches: "biomimicry," "biologically inspired design," "bio-inspired materials"
- **USPTO/EPO Patent Databases** — bio-inspired patent landscape

---

## Supporting Python Tools
- `tools/knowledge_updater.py` — crawl4ai pipeline that fetches latest papers from ArXiv q-bio, Journal of Bionic Engineering, Bioinspiration & Biomimetics; deduplicates by DOI; appends to SECOND-KNOWLEDGE-BRAIN.md

---

## Build Status

All Phases 0-5 are complete and design-validated:

- [x] `skills/sub-profile-intake.md` - 8-field schema + AskNature translation + 3 worked intake examples
- [x] `skills/sub-biological-researcher.md` - AskNature + ArXiv (q-bio.PE, cond-mat.mtrl-sci, cs.RO) + journal query templates + SECOND-KNOWLEDGE-BRAIN fallback
- [x] `skills/sub-analogy-mapper.md` - 4-dimension scoring rubric + TRIZ mapping + gecko/termite worked scorings
- [x] `skills/sub-design-translator.md` - material-analogue table + manufacturing-route selection + patent templates + Life's-Principles grid + effort estimation
- [x] `skills/main.md` - full 7-step harness + 9-point quality gate + devil's-advocate + Biomimicry Design Brief format
- [x] `tools/knowledge_updater.py` - crawl4ai (primary) -> requests -> feedparser transport, DOI-hash dedup, recency+relevance scoring, brain updater; `--mock-rss` offline self-test
- [x] `tests/test-scenarios.md` - 7 scenarios with pass/fail log (design-validated)
- [x] `tests/harness-dry-run-gecko-adhesion.md` - Phase 0 gecko dry-run validation
- [x] `tests/termite-ventilation-reference-brief.md` - Phase 2 E2E reference brief
- [x] `SECOND-KNOWLEDGE-BRAIN.md` - seeded with 24 foundational papers + 15 case studies + frameworks
- [x] `PROJECT-detail.md` + `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` - specification + roadmap (all phases marked done)

**Production-stage (resource-deferred) items:** live model/network runs for each test scenario and the first live `knowledge_updater.py` crawl. These are explicitly deferred to conserve resources; all code and contracts are complete and ready for execution.

---

## Cross-Skill Reuse (science-industry cluster)

Skill 243 sits in the `science-industry` cluster alongside aquaculture, agriculture, materials, and bioprocess skills. Two of its four sub-skills are designed for cluster-wide reuse, and several external cluster sub-skills are reusable here:

**Shareable out of Skill 243:**
- `sub-biological-researcher` - general-purpose AskNature + ArXiv (q-bio/cond-mat/cs.RO) + domain-journal literature search with evidence-tier tagging. Directly reusable by aquaculture, agriculture, food, and bio-process skills that need a peer-reviewed biological evidence layer.
- `sub-analogy-mapper` - the 4-dimension scoring rubric (Function Alignment / Environmental Match / Scale Compatibility / Transferability) + TRIZ mapping is domain-agnostic and can rank any cross-domain analogy, not only biology to engineering.

**Reusable into Skill 243 from the cluster:**
- `sub-evaluation-framework-selector` - chooses the appropriate evidence/scoring framework for a given engineering domain (e.g. ISO LCA vs. TRIZ) before sub-design-translator runs.
- `sub-scoring-engine` - a generic weighted scoring engine can back sub-analogy-mapper's weighted total computation.
- `sub-improvement-roadmap` - can standardise the "Implementation Roadmap" section of the final Biomimicry Design Brief across the cluster.

**Reuse protocol:** each shared sub-skill exposes a documented input/output contract in its `## Inputs` and `## Outputs` sections; cluster skills invoke it by file path and pass the documented structured payload. At least 2 sub-skills are identified as shareable (sub-biological-researcher, sub-analogy-mapper), satisfying Phase 5.

---

## Deployment & Cron Setup

`tools/knowledge_updater.py` keeps `SECOND-KNOWLEDGE-BRAIN.md` current with the latest biomimicry research. Schedule a weekly run (Sunday 02:00 UTC) so the knowledge base refreshes before the working week.

### Dependencies
```bash
pip install crawl4ai requests feedparser
# crawl4ai is optional but preferred (JS-rendered pages); the script degrades to
# requests then feedparser if crawl4ai is not installed.
```

### Offline self-test (no network - safe in CI)
```bash
python tools/knowledge_updater.py --mock-rss --dry-run
# Parses an embedded sample ArXiv RSS; verifies dedup, relevance filter,
# recency scoring, ranking, and append formatting with zero network access.
```

### One-off live dry run (no file write)
```bash
python tools/knowledge_updater.py --dry-run
```

### Cron (Linux/macOS) - weekly Sunday 02:00 UTC
```cron
# m h dom mon dow command
0 2 * * 0 cd /path/to/q-bio.PE && /usr/bin/python3 tools/knowledge_updater.py >> logs/knowledge_updater.log 2>&1
```

### Windows Task Scheduler (equivalent weekly schedule)
```powershell
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "tools\knowledge_updater.py" -WorkingDirectory "D:\skills\q-bio.PE"
$trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Sunday -At 2:00AM
Register-ScheduledTask -TaskName "BiomimicryKnowledgeUpdater" -Action $action -Trigger $trigger -Description "Weekly refresh of SECOND-KNOWLEDGE-BRAIN.md"
```

### Production notes
- Run from the repository root so `BRAIN_PATH_DEFAULT` resolves to `SECOND-KNOWLEDGE-BRAIN.md`.
- The updater appends only novel DOIs (SHA-256 dedup) and never rewrites existing rows, so it is safe to re-run.
- `--max-entries N` caps how many rows are appended per run (default 30).
- A `## Knowledge Update Log` row is written with a UTC timestamp on every successful run.

---

## Cross-References
- `PROJECT-detail.md` — full technical specification
- `PROJECT-DEVELOPMENT-PHASE-TRACKING.md` — build roadmap and milestone tracking
- `SECOND-KNOWLEDGE-BRAIN.md` — self-improving domain knowledge base
