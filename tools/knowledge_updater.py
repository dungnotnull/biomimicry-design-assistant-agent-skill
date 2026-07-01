"""
knowledge_updater.py ? Biomimicry Design Assistant (Skill 243)
==============================================================
Automated knowledge pipeline for SECOND-KNOWLEDGE-BRAIN.md.

Fetches the latest biomimicry-relevant research from:
  - ArXiv q-bio.PE (populations & evolution)            ? RSS, via crawl4ai
  - ArXiv cond-mat.mtrl-sci (biomaterials)              ? RSS, via crawl4ai
  - ArXiv cs.RO (bio-inspired robotics)                 ? RSS, via crawl4ai
  - Journal of Bionic Engineering / Bioinspiration &     ? Semantic Scholar
    Biomimetics / Nature Materials                       keyword queries
  - SECOND-KNOWLEDGE-BRAIN.md                            ? offline fallback

For each candidate the script:
  1. normalises and hashes its DOI (SHA-256, 16-char) for deduplication,
  2. scores recency (0-5) and domain-keyword relevance (0-5),
  3. ranks by combined score,
  4. appends the top-N new rows to the ``## Key Research Papers`` table and
     writes a timestamped row to the ``## Knowledge Update Log``.

Recommended schedule: ``cron 0 2 * * 0``  (Sunday 02:00 UTC).

Requirements (install only what you use):
  pip install crawl4ai requests feedparser

The script degrades gracefully: if crawl4ai is not installed it falls back to
``requests`` then to ``feedparser``'s own fetcher. A ``--mock-rss`` mode
exercises the entire parse -> dedup -> score -> append pipeline against an
embedded sample ArXiv RSS with **zero network access**, which is the
production dry-run / CI test.

Usage:
  python knowledge_updater.py                     # live fetch + write
  python knowledge_updater.py --dry-run           # live fetch, no write
  python knowledge_updater.py --mock-rss          # offline self-test (no net)
  python knowledge_updater.py --mock-rss --dry-run
  python knowledge_updater.py --brain-path PATH --max-entries 30
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import quote_plus

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BRAIN_PATH_DEFAULT = Path(__file__).resolve().parent.parent / "SECOND-KNOWLEDGE-BRAIN.md"

ARXIV_FEEDS = [
    {
        "name": "ArXiv q-bio.PE",
        "url": "https://export.arxiv.org/rss/q-bio.PE",
        "category": "Evolutionary Biology",
    },
    {
        "name": "ArXiv cond-mat.mtrl-sci",
        "url": "https://export.arxiv.org/rss/cond-mat.mtrl-sci",
        "category": "Biomaterials / Materials Science",
    },
    {
        "name": "ArXiv cs.RO",
        "url": "https://export.arxiv.org/rss/cs.RO",
        "category": "Bio-inspired Robotics",
    },
]

SEMANTIC_SCHOLAR_API = "https://api.semanticscholar.org/graph/v1/paper/search"
SEMANTIC_SCHOLAR_FIELDS = "title,authors,year,venue,externalIds,abstract"

DOMAIN_SEARCH_QUERIES = [
    "biomimicry engineering design",
    "biologically inspired materials",
    "bio-inspired structures mechanical",
    "natural structures engineering application",
    "evolutionary optimization engineering",
    "gecko adhesion synthetic",
    "shark skin drag reduction",
    "spider silk engineering",
    "lotus effect coating",
    "termite mound architecture",
    "nacre composite material",
    "hierarchical biological structure engineering",
]

RELEVANCE_KEYWORDS = [
    "biomimicry", "biologically inspired", "bio-inspired", "biomimetic",
    "natural structure", "evolutionary design", "biological mechanism",
    "bionic", "nature-inspired", "living material", "self-healing",
    "superhydrophobic", "structural color", "gecko", "lotus", "spider silk",
    "nacre", "bone scaffold", "shark skin", "termite", "mussel adhesion",
]

MAX_RESULTS_PER_QUERY = 10
RECENCY_WINDOW_DAYS = 180            # ~6 months
REQUEST_DELAY_SECONDS = 1.5          # be polite to public APIs
DEFAULT_MAX_ENTRIES = 30

# ---------------------------------------------------------------------------
# Embedded mock RSS ? used by --mock-rss for offline dry-run / CI testing.
# Two entries reuse DOIs already present in the seeded brain (dedup test);
# the remaining entries are novel and should survive dedup + relevance filter.
# ---------------------------------------------------------------------------

MOCK_ARXIV_RSS = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>ArXiv q-bio.PE (mock)</title>
    <link>https://arxiv.org/list/q-bio.PE/recent</link>
    <description>Mock ArXiv RSS feed for knowledge_updater self-test</description>
    <item>
      <title>Biomimetic drag-reducing riblet surfaces inspired by shark skin for marine coatings</title>
      <link>https://arxiv.org/abs/2607.00001</link>
      <description>Engineered polymer riblet arrays reproducing shark-skin denticle geometry reduce turbulent boundary-layer drag by up to 8 percent in tow-tank tests.</description>
      <pubDate>Tue, 01 Jul 2025 00:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Resilin-mimetic elastomers for high-cycle bio-inspired flexible joints in soft robotics</title>
      <link>https://arxiv.org/abs/2607.00002</link>
      <description>Recombinant-resilin-inspired silicone networks achieve millions of flex cycles, enabling biomimetic compliant joints for bio-inspired robotics.</description>
      <pubDate>Wed, 02 Jul 2025 00:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Termite-mound thermosiphon ventilation applied to passive-cooling building envelopes</title>
      <link>https://arxiv.org/abs/2607.00003</link>
      <description>Field measurements of a termite-mound-inspired chimney stack demonstrate passive cooling without mechanical fans in hot-arid climates.</description>
      <pubDate>Thu, 03 Jul 2025 00:00:00 GMT</pubDate>
    </item>
    <item>
      <title>Adhesive force of a single gecko foot-hair (dedup probe)</title>
      <link>https://doi.org/10.1038/35015073</link>
      <description>Already-seeded classic gecko setal adhesion paper. DOI 10.1038/35015073 is already present in the brain and must be skipped by the deduplicator.</description>
      <pubDate>Mon, 01 Jan 2000 00:00:00 GMT</pubDate>
    </item>
    <item>
      <title>A pure algebraic topology preprint</title>
      <link>https://arxiv.org/abs/2607.00004</link>
      <description>Abstract containing no engineering or biological terms whatsoever so the relevance scorer filters it out.</description>
      <pubDate>Fri, 04 Jul 2025 00:00:00 GMT</pubDate>
    </item>
  </channel>
</rss>
"""

# ---------------------------------------------------------------------------
# DOI / utility helpers
# ---------------------------------------------------------------------------

_DOI_PATTERN = re.compile(r"\b(10\.\d{4,9}/[^\s|>\]]+)", re.IGNORECASE)
_ARXIV_ABS_PATTERN = re.compile(r"arxiv\.org/abs/([0-9]{4}\.[0-9]{4,5}|[a-z\-]+/[0-9]{7})",
                                re.IGNORECASE)


def doi_hash(doi: str) -> str:
    """Return a stable 16-char SHA-256 prefix for a normalised DOI string."""
    return hashlib.sha256(doi.strip().lower().encode("utf-8")).hexdigest()[:16]


def normalise_arxiv_link_to_doi(link: str) -> str:
    """Convert an arxiv.org/abs/<id> URL into the synthetic DOI 10.48550/arXiv.<id>."""
    m = _ARXIV_ABS_PATTERN.search(link or "")
    if not m:
        return ""
    arxiv_num = m.group(1)
    # strip any trailing version suffix such as v2
    arxiv_num = re.sub(r"v\d+$", "", arxiv_num)
    return f"10.48550/arXiv.{arxiv_num}"


def extract_existing_dois(brain_text: str) -> set[str]:
    """
    Extract every DOI already cited in SECOND-KNOWLEDGE-BRAIN.md and return
    their hashes. Also includes synthetic arXiv DOIs (10.48550/arXiv.*).
    """
    found = _DOI_PATTERN.findall(brain_text)
    arxiv_synthetic = re.findall(r"arXiv\.([0-9]{4}\.[0-9]{4,5}|[a-z\-]+/[0-9]{7})",
                                 brain_text, re.IGNORECASE)
    for ax in arxiv_synthetic:
        found.append(f"10.48550/arXiv.{ax}")
    return {doi_hash(d) for d in found}


def compute_relevance_score(title: str, abstract: str) -> int:
    """
    Domain relevance on a 0-5 scale. Title matches weight 2, abstract weight 1.
    """
    title_lower = (title or "").lower()
    text_lower = ((title or "") + " " + (abstract or "")).lower()
    score = 0
    for kw in RELEVANCE_KEYWORDS:
        if kw in title_lower:
            score += 2
        elif kw in text_lower:
            score += 1
    return min(score, 5)


def compute_recency_score(year: Optional[int]) -> int:
    """Recency on a 0-5 scale relative to the current UTC year."""
    if year is None:
        return 0
    age = datetime.now(timezone.utc).year - year
    return max(0, 5 - age)


def format_table_row(entry: dict) -> str:
    """Render a paper entry as a Markdown row for the brain's papers table."""
    authors = (entry.get("authors") or "Unknown")
    if len(authors) > 60:
        authors = authors[:57] + "..."
    title = (entry.get("title") or "").replace("|", "-")
    year = entry.get("year", "N/A")
    venue = (entry.get("venue") or "ArXiv").replace("|", "-")
    doi = entry.get("doi", "")
    relevance = entry.get("relevance_note", "Biomimicry/bio-inspired engineering")
    return f"| {title} | {authors} | {year} | {venue} | {doi} | {relevance} |"


# ---------------------------------------------------------------------------
# Network layer: crawl4ai (primary) -> requests -> feedparser-direct
# ---------------------------------------------------------------------------

def _fetch_raw_via_crawl4ai(url: str) -> str:
    """Fetch raw page body with crawl4ai. Returns feed-parseable text (RSS XML)."""
    from crawl4ai import AsyncWebCrawler  # imported lazily so --mock-rss works without it

    async def _crawl() -> str:
        async with AsyncWebCrawler(verbose=False) as crawler:
            result = await crawler.arun(url=url)
            if not result.success:
                return ""
            # crawl4ai exposes the raw HTML/XML on .html and a derived .markdown.
            # For RSS we want the raw XML so feedparser can read the items.
            return getattr(result, "html", "") or getattr(result, "markdown", "") or ""

    return asyncio.run(_crawl())


def _fetch_raw_via_requests(url: str) -> str:
    """Fetch raw body with the requests library (no JS rendering)."""
    import requests  # lazy import

    resp = requests.get(url, timeout=30, headers={"User-Agent": "biomimicry-knowledge-updater/1.0"})
    resp.raise_for_status()
    return resp.text


def _fetch_raw(url: str) -> str:
    """
    Fetch the raw body of a URL using the first available transport, in this
    order of preference: crawl4ai, requests, feedparser-direct. Returns the
    body as text, or an empty string if every transport failed.
    """
    # 1. crawl4ai (preferred ? handles JS-rendered and RSS pages)
    try:
        body = _fetch_raw_via_crawl4ai(url)
        if body and len(body) > 50:
            return body
    except Exception as exc:  # noqa: BLE001 - transport fallback is intentional
        print(f"    crawl4ai unavailable/failed ({exc}); trying requests...")

    # 2. requests (plain HTTP)
    try:
        body = _fetch_raw_via_requests(url)
        if body:
            return body
    except Exception as exc:  # noqa: BLE001
        print(f"    requests failed ({exc}); trying feedparser direct...")

    # 3. feedparser direct fetch (last resort; may bypass transport issues)
    try:
        import feedparser  # lazy import

        parsed = feedparser.parse(url)
        if parsed and getattr(parsed, "entries", None):
            # Re-serialise a minimal RSS from what feedparser parsed so the
            # common _parse_feed() path can still be used uniformly.
            return _serialise_parsed_feed(parsed)
    except Exception as exc:  # noqa: BLE001
        print(f"    feedparser direct failed ({exc})")

    return ""


def _serialise_parsed_feed(parsed) -> str:
    """Best-effort re-serialisation of a feedparser object back into RSS XML."""
    import xml.sax.saxutils as su

    parts = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0"><channel>']
    feed = getattr(parsed, "feed", None) or {}
    parts.append(f"<title>{su.escape(feed.get('title', 'feed'))}</title>")
    for e in parsed.entries:
        parts.append("<item>")
        parts.append(f"<title>{su.escape(e.get('title', ''))}</title>")
        parts.append(f"<link>{su.escape(e.get('link', ''))}</link>")
        parts.append(f"<description>{su.escape(e.get('summary', ''))}</description>")
        if e.get("published"):
            parts.append(f"<pubDate>{su.escape(e['published'])}</pubDate>")
        parts.append("</item>")
    parts.append("</channel></rss>")
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Feed parsing (shared by live fetch and mock RSS)
# ---------------------------------------------------------------------------

def _parse_year(entry: dict) -> Optional[int]:
    """Best-effort extraction of a 4-digit publication year from a feed entry."""
    # feedparser exposes a parsed struct_time under *_parsed when the date
    # is in a recognised format (RFC822 / ISO8601).
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if parsed and hasattr(parsed, "tm_year"):
        return int(parsed.tm_year)
    # Fallback: scan the raw date string for any 4-digit year (1970-2099).
    for text in (entry.get("published", ""), entry.get("updated", "")):
        m = re.search(r"\b(19[7-9]\d|20\d{2})\b", text or "")
        if m:
            return int(m.group(1))
    return None


def _parse_feed(raw: str, feed_config: dict, existing_dois: set[str]) -> list[dict]:
    """Parse an RSS/Atom body with feedparser and build scored paper entries."""
    import feedparser  # lazy import

    parsed = feedparser.parse(raw)
    results: list[dict] = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=RECENCY_WINDOW_DAYS)

    for entry in parsed.entries[: MAX_RESULTS_PER_QUERY * 3]:
        link = entry.get("link", "") or entry.get("id", "")
        doi = normalise_arxiv_link_to_doi(link) or (entry.get("doi") or "")

        # Some arXiv items carry the DOI inside a <dc:identifier> or <arxiv:doi>
        if not doi:
            m = _DOI_PATTERN.search(str(entry.get("summary", "")) + " " + str(entry.get("id", "")))
            if m:
                doi = m.group(1)

        if not doi:
            continue

        h = doi_hash(doi)
        if h in existing_dois:
            continue  # already in brain

        title = re.sub(r"\s+", " ", entry.get("title", "")).strip()
        abstract = entry.get("summary", "") or entry.get("description", "")
        relevance = compute_relevance_score(title, abstract)
        if relevance < 1:
            continue  # not relevant enough

        year = _parse_year(entry)

        authors_raw = entry.get("authors", [])
        if authors_raw:
            names = [a.get("name", "") for a in authors_raw[:3] if a.get("name")]
            authors_str = ", ".join(names)
            if len(authors_raw) > 3:
                authors_str += " et al."
        else:
            authors_str = "Unknown"
        if not authors_str:
            authors_str = "Unknown"

        results.append({
            "title": title,
            "authors": authors_str,
            "year": year or datetime.now(timezone.utc).year,
            "venue": feed_config["name"],
            "doi": doi,
            "relevance_note": feed_config["category"],
            "_relevance_score": relevance,
            "_recency_score": compute_recency_score(year),
            "_doi_hash": h,
        })

    return results


def fetch_arxiv_rss(feed_config: dict, existing_dois: set[str], mock: bool = False) -> list[dict]:
    """Fetch + parse a single ArXiv RSS feed (live or mock)."""
    label = feed_config["name"]
    if mock:
        print(f"  [mock] Parsing embedded sample RSS for {label} ... ", end="", flush=True)
        entries = _parse_feed(MOCK_ARXIV_RSS, feed_config, existing_dois)
        print(f"found {len(entries)} new relevant papers.")
        return entries

    print(f"  Fetching {label} RSS ... ", end="", flush=True)
    raw = _fetch_raw(feed_config["url"])
    if not raw:
        print("FAILED (no transport could retrieve the feed).")
        return []
    entries = _parse_feed(raw, feed_config, existing_dois)
    print(f"found {len(entries)} new relevant papers.")
    return entries


# ---------------------------------------------------------------------------
# Semantic Scholar fetcher (live only)
# ---------------------------------------------------------------------------

def fetch_semantic_scholar(query: str, existing_dois: set[str]) -> list[dict]:
    """Keyword search via the Semantic Scholar Graph API."""
    import requests  # lazy import

    results: list[dict] = []
    params = {
        "query": query,
        "fields": SEMANTIC_SCHOLAR_FIELDS,
        "limit": MAX_RESULTS_PER_QUERY,
    }
    try:
        resp = requests.get(SEMANTIC_SCHOLAR_API, params=params, timeout=20,
                             headers={"User-Agent": "biomimicry-knowledge-updater/1.0"})
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:  # noqa: BLE001
        print(f"FAILED ({exc})")
        return results

    for paper in data.get("data", []):
        ext_ids = paper.get("externalIds") or {}
        doi = ext_ids.get("DOI", "")
        arxiv_id = ext_ids.get("ArXiv", "")
        if not doi and arxiv_id:
            doi = f"10.48550/arXiv.{arxiv_id}"
        if not doi:
            continue

        h = doi_hash(doi)
        if h in existing_dois:
            continue

        title = paper.get("title") or ""
        abstract = paper.get("abstract") or ""
        relevance = compute_relevance_score(title, abstract)
        if relevance < 2:  # higher bar for SS to avoid noise
            continue

        year = paper.get("year")
        authors_list = paper.get("authors") or []
        names = [a.get("name", "") for a in authors_list[:3] if a.get("name")]
        authors_str = ", ".join(names)
        if len(authors_list) > 3:
            authors_str += " et al."
        if not authors_str:
            authors_str = "Unknown"

        results.append({
            "title": title.replace("|", "-"),
            "authors": authors_str,
            "year": year or datetime.now(timezone.utc).year,
            "venue": (paper.get("venue") or "Journal / Conference"),
            "doi": doi,
            "relevance_note": f"relevance={relevance}/5; query: {query[:40]}",
            "_relevance_score": relevance,
            "_recency_score": compute_recency_score(year),
            "_doi_hash": h,
        })

    return results


# ---------------------------------------------------------------------------
# Deduplication + ranking
# ---------------------------------------------------------------------------

def deduplicate_and_rank(entries: Iterable[dict]) -> list[dict]:
    """Remove duplicates by DOI hash; rank by recency + relevance (desc)."""
    seen: dict[str, dict] = {}
    for entry in entries:
        h = entry["_doi_hash"]
        incumbent = seen.get(h)
        if incumbent is None:
            seen[h] = entry
            continue
        if (entry["_relevance_score"] + entry["_recency_score"]
                > incumbent["_relevance_score"] + incumbent["_recency_score"]):
            seen[h] = entry
    return sorted(
        seen.values(),
        key=lambda e: e["_relevance_score"] + e["_recency_score"],
        reverse=True,
    )


# ---------------------------------------------------------------------------
# SECOND-KNOWLEDGE-BRAIN.md writer
# ---------------------------------------------------------------------------

_TABLE_HEADER_RE = re.compile(
    r"(## Key Research Papers\s*\n\|[^\n]+\|\s*\n\|[-| :]+\|\s*\n)",
    re.MULTILINE,
)
_LOG_HEADER_RE = re.compile(
    r"(## Knowledge Update Log\s*\n\|[^\n]+\|\s*\n\|[-| :]+\|\s*\n)",
    re.MULTILINE,
)


def update_brain(brain_path: Path, new_entries: list[dict], dry_run: bool = False) -> int:
    """Append new paper rows + a log row to the brain file. Returns count appended."""
    if not brain_path.exists():
        print(f"ERROR: Brain file not found at {brain_path}")
        return 0

    brain_text = brain_path.read_text(encoding="utf-8")

    match = _TABLE_HEADER_RE.search(brain_text)
    if not match:
        print("WARNING: '## Key Research Papers' table not found; creating a new one.")
        insert_pos = len(brain_text)
        prefix = ("\n\n## Key Research Papers\n"
                  "| Title | Authors | Year | Venue | DOI/Link | Relevance |\n"
                  "|-------|---------|------|-------|----------|----------|\n")
    else:
        insert_pos = match.end()
        prefix = ""

    rows = [format_table_row(e) for e in new_entries]
    if not rows:
        print("No new entries to append.")
        return 0

    insert_text = prefix + "\n".join(rows) + "\n"
    new_brain_text = brain_text[:insert_pos] + insert_text + brain_text[insert_pos:]

    # Append a timestamped row to the Knowledge Update Log.
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    log_row = (f"| {timestamp} | ArXiv + Semantic Scholar | {len(rows)} | "
               f"Automated DOI hash | Weekly updater run |\n")
    log_match = _LOG_HEADER_RE.search(new_brain_text)
    if log_match:
        log_insert_pos = log_match.end()
        new_brain_text = new_brain_text[:log_insert_pos] + log_row + new_brain_text[log_insert_pos:]

    if dry_run:
        print(f"\n[DRY RUN] Would append {len(rows)} entries to {brain_path}")
        for row in rows[:5]:
            print(f"  {row[:120]}")
        if len(rows) > 5:
            print(f"  ... and {len(rows) - 5} more")
        return len(rows)

    brain_path.write_text(new_brain_text, encoding="utf-8")
    print(f"\nSuccessfully appended {len(rows)} new entries to {brain_path}")
    return len(rows)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update SECOND-KNOWLEDGE-BRAIN.md with the latest biomimicry research.",
    )
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be appended without modifying the brain file.")
    parser.add_argument("--mock-rss", action="store_true",
                        help="Offline self-test: parse an embedded sample ArXiv RSS "
                             "with no network access. Used for CI / dedup verification.")
    parser.add_argument("--brain-path", type=Path, default=BRAIN_PATH_DEFAULT,
                        help=f"Path to SECOND-KNOWLEDGE-BRAIN.md (default: {BRAIN_PATH_DEFAULT})")
    parser.add_argument("--max-entries", type=int, default=DEFAULT_MAX_ENTRIES,
                        help=f"Maximum number of new entries to append per run (default: {DEFAULT_MAX_ENTRIES}).")
    args = parser.parse_args()

    brain_path: Path = args.brain_path
    mock: bool = args.mock_rss

    print("Biomimicry Design Assistant ? Knowledge Updater")
    print(f"Brain file: {brain_path}")
    print(f"Mode: {'MOCK-RSS (offline self-test)' if mock else 'LIVE'}"
          f"{' [DRY RUN]' if args.dry_run else ' [WRITE]'}")
    print("=" * 60)

    if not brain_path.exists():
        print(f"ERROR: Brain file not found: {brain_path}")
        return 1

    brain_text = brain_path.read_text(encoding="utf-8")
    existing_dois = extract_existing_dois(brain_text)
    print(f"Existing DOIs (hashed) in brain: {len(existing_dois)}\n")

    all_entries: list[dict] = []

    # ArXiv RSS feeds (live via crawl4ai/requests/feedparser, or mock).
    print("--- ArXiv RSS Feeds ---")
    for feed_config in ARXIV_FEEDS:
        all_entries.extend(fetch_arxiv_rss(feed_config, existing_dois, mock=mock))
        if not mock:
            time.sleep(REQUEST_DELAY_SECONDS)

    # Semantic Scholar keyword queries (live only ? skipped in mock mode).
    if not mock:
        print("\n--- Semantic Scholar Queries ---")
        for query in DOMAIN_SEARCH_QUERIES:
            print(f"  Query: '{query}' ... ", end="", flush=True)
            entries = fetch_semantic_scholar(query, existing_dois)
            print(f"{len(entries)} new results.")
            all_entries.extend(entries)
            time.sleep(REQUEST_DELAY_SECONDS)
    else:
        print("\n--- Semantic Scholar Queries ---")
        print("  [mock] Skipped (offline self-test).")

    print("\n--- Deduplication ---")
    print(f"Total candidates collected: {len(all_entries)}")
    ranked_entries = deduplicate_and_rank(all_entries)
    print(f"After deduplication: {len(ranked_entries)}")

    top_entries = ranked_entries[: args.max_entries]
    print(f"Top entries selected for append: {len(top_entries)}")

    if top_entries:
        print("\nTop 5 by relevance + recency:")
        for i, entry in enumerate(top_entries[:5], 1):
            total = entry["_relevance_score"] + entry["_recency_score"]
            print(f"  {i}. [{total}/10] {entry['title'][:70]} ({entry['year']})")

    print("\n--- Updating Brain ---")
    appended = update_brain(brain_path, top_entries, dry_run=args.dry_run)

    print(f"\nDone. {appended} new entries added.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
