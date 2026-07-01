# Biomimicry Design Assistant

> A structured, production-ready harness that maps an engineering challenge to
> nature's proven solutions and returns a *Biomimicry Design Brief* ? scored
> biological analogies, engineering specifications, manufacturing routes, and a
> Life's-Principles compliance matrix, all grounded in cited evidence.

Life's Principles (Janine Benyus), the **AskNature** functional taxonomy, **TRIZ**
bio-inspired heuristics (Vincent et al., 2006), and the **Biologically Inspired
Design (BID)** methodology (Goel et al., Georgia Tech).

[![phase](https://img.shields.io/badge/phases%200--5-complete-brightgreen)](PROJECT-DEVELOPMENT-PHASE-TRACKING.md)
[![license](https://img.shields.io/badge/license-MIT-blue)](#license)
[![python](https://img.shields.io/badge/python-3.10%2B-blue)](#dependencies)

---

## What it does

```
/biomimicry-design-assistant [problem description]
   Step 1  sub-profile-intake         capture & structure the 8-field Problem Profile
   Step 2  sub-biological-researcher  search AskNature + ArXiv + journals -> >=5 candidates
   Step 3  sub-analogy-mapper         4-dimension score + TRIZ -> top 3 analogies
   Step 4  sub-design-translator      biology -> material + manufacturing + precedent
   Step 5  quality gate (9-point)     evidence, compliance, completeness
   Step 6  devil's advocate           failure modes + comparison to conventional
   Step 7  Biomimicry Design Brief    executive summary, comparison, specs, roadmap, references
```

Every biological claim is tagged with an evidence tier (Peer-Reviewed >
AskNature > Case Study > Expert Opinion > Popular Science). The harness never
invents biology from memory ? each candidate must trace to a citable source.

---

## Dependencies

- **Runtime (knowledge updater only):** Python 3.10+
  ```bash
  pip install crawl4ai requests feedparser
  # crawl4ai optional but preferred; script degrades to requests then feedparser.
  ```
- **Harness itself:** no runtime dependencies ? the skills are structured
  Markdown prompt programs invoked by an LLM agent (Claude Code) using
  WebSearch / WebFetch / Read / Write / Bash.

---

## Quick start

### Offline self-test (no network ? CI-safe)
```bash
python tools/knowledge_updater.py --mock-rss --dry-run
```
Parses an embedded sample ArXiv RSS and verifies DOI-hash deduplication, the
relevance filter, recency scoring, ranking, and append formatting ? all with
zero network access.

### Live knowledge refresh (dry run, no write)
```bash
python tools/knowledge_updater.py --dry-run
```

### Live knowledge refresh (writes to SECOND-KNOWLEDGE-BRAIN.md)
```bash
python tools/knowledge_updater.py
```

### Weekly schedule
See the *Deployment & Cron Setup* section in `CLAUDE.md` for cron and Windows
Task Scheduler equivalents (Sunday 02:00 UTC).

---

## Quality gates

The harness refuses to emit a final brief until all nine checks pass (or are
explicitly flagged): profile complete; >=5 biological strategies across >=3
taxonomic groups; every mechanism cited; all 4 scoring dimensions populated;
top-3 Function Alignment >= 7/10; each spec has material + manufacturing +
precedent/patent; all 6 Life's-Principles categories evaluated; devil's-advocate
failure modes documented; evidence tiers tagged.

---

## Test scenarios

Seven diverse scenarios cover nanotechnology (gecko dry adhesive), architecture
(termite passive ventilation), marine engineering (shark-skin anti-fouling),
materials science (pomelo impact packaging), filtration (Nepenthes SLIPS),
soft robotics (resilin joints), and optics (Morpho structural color). See
`tests/test-scenarios.md`.

---

## License

MIT ? see repository header. The skill content, knowledge base, and pipeline
are released for open-source reuse. Cited biological literature remains the
property of its respective authors and publishers (cited, not redistributed).
