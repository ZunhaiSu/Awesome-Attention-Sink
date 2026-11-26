# Recent-literature inventory, 2026-10-26

This page preserves the **initial discovery stage**, before source-grounded integration. For current totals, see [reviewed additions and remaining gaps](REVIEW_20261026.md). The current CSV ledger overlays subsequent decisions without changing the original snapshots.

The user subsequently expanded the scope to citation-linked and attention-concentration literature. The [broader library](LIBRARY.md) is now the primary collection view; the counts on this page remain historical.

## Scope and counts

The formal migrated catalog contains **208 records**. The discovery window is **2026-06-01–2026-10-26**, based on arXiv's first-submission date (UTC), because the latest month represented in the source date column is May 2026. This is a stated search window, not proof that the original collection covered every earlier month exhaustively.

Two queries returned 124 entries and **121 distinct arXiv IDs**. Identifier, DOI (where available), and exact normalized-title comparison found no match to the migrated baseline. One similar-title pair is retained for manual checking; the two records have different arXiv IDs.

Initial screening retained **53 attention-sink keyword candidates** and **20 related outlier/register candidates**. It excluded **48 lexical collisions** involving preregistration, linguistic register, geometric registration, hardware registers, or other non-target senses. Exclusions remain in the retrieval ledger.

| First-submission month | AS keyword candidates | Related candidates | Total retained |
|---|---:|---:|---:|
| 2026-06 | 10 | 4 | 14 |
| 2026-07 | 10 | 3 | 13 |
| 2026-08 | 7 | 4 | 11 |
| 2026-09 | 13 | 4 | 17 |
| 2026-10, through cutoff | 13 | 5 | 18 |
| Total | 53 | 20 | 73 |

**These are candidate counts, not 73 newly accepted catalog entries.** Eight AS candidates have had abstract checks; the remaining AS hits still require screening. The 20 related candidates were screened using titles and abstract excerpts. No candidate has been marked as a completed full-text review, and none has been merged into the formal catalog. A keyword hit is not a claim of direct attention-sink evidence.

## Queries

The complete query strings, official API URLs, page counts, retrieval-response hashes, version dates, and author-supplied publication notes are in [the discovery ledger](../data/candidates/arxiv-2026-10-26.json).

1. **Attention-sink terminology:** title or abstract contains `attention sink` or `attention sinks`.
2. **Related mechanisms:** title contains `massive activation`, `massive activations`, `register token`, `register tokens`, or `registers`, restricted to cs.LG, cs.CL, cs.CV, cs.AI, or stat.ML.

Both queries include `submittedDate:[202606010000 TO 202610262359]`. All result pages were fetched. The broad register query is intentionally screened for semantic collisions rather than counted wholesale.

## Files and reproduction

- [Retained candidates, CSV](../exports/candidates.csv)
- [All 121 retrieval records and screening decisions, CSV](../exports/retrieval-ledger.csv)
- [Explicit screening decisions](../data/screening/2026-10-26.json)

```sh
python scripts/inventory_recent.py --since 2026-06-01 --until 2026-10-26 --cache /path/to/local/cache
python scripts/apply_screening.py
python scripts/catalog.py build
```

The query establishes completeness only for its returned pages. It does not establish exhaustive field coverage, recover every paper with different terminology, or detect all revisions and new publications of older preprints. arXiv publication comments are author supplied. Full-text scope decisions, formal taxonomy assignments, older omissions, and proceedings verification remain separate work.

Candidate relevance and summary notes are editorial assessments; the original paper URLs are the primary sources. Full abstracts are not redistributed in this repository.
