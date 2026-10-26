# Contributing papers and corrections

Open an issue with the title, stable paper link (arXiv ID or DOI preferred), publication status, and a short explanation of relevance. Include a source for any proposed classification or numerical claim. A preprint and its published version normally belong to the same study.

Propose the appropriate existing categories without shortening their names. Labels may overlap. Distinguish direct attention-sink measurements from related outlier, register, and routing evidence.

Candidate records remain outside `data/papers.json` until reviewed. Record whether screening used the title, abstract, or full text. An author's venue announcement should remain distinct from a verified proceedings record.

For a reviewed addition, record the versioned primary-source URL, checked sections, substantive finding, classification rationale, fine-grained mechanism, and limits in `data/reviews/`. Specify whether the reading was assisted and whether only key sections were checked. Do not infer a circuit from high norms, assign Geometric Anchoring to every spectral study, or confuse output-gate offsets with attention-logit biases. Keep diagnostic or negative interventions distinct from successful mitigation methods. An empty method category is preferable to a forced fit.

Initial and supplemental retrieval snapshots are historical evidence. Preserve them and overlay new outcomes through review decisions. The Feishu importer is a one-time baseline tool, not an update command for the growing catalog.

The expanded library also accepts citation-linked and attention-concentration resources. Store the precise relation evidence and reading status in `data/library/`; an index-only lead may be included with unassigned method labels. A citation or spectral-collapse metric alone does not establish a persistent attention sink. Preserve the original category names when a source supports a classification. Run `python scripts/library.py build` and `python scripts/library.py check` for these updates. The prior queue and exclusions describe the earlier, narrower screening stage, not universal exclusion from the expanded library.

For catalog changes, update the authoritative data, then run:

```sh
python scripts/catalog.py build
python scripts/catalog.py check
```

Include generated exports with the change. Preserve original source rows and explain corrections. Online catalog updates do not silently alter the literature coverage of a frozen manuscript version.
