# Contributing papers and corrections

Open an issue with the title, stable paper link (arXiv ID or DOI preferred), publication status, and a short explanation of relevance. Include a source for any proposed classification or numerical claim. A preprint and its published version normally belong to the same study.

Propose the appropriate existing categories without shortening their names. Labels may overlap. Distinguish direct attention-sink measurements from related outlier, register, and routing evidence.

Candidate records remain outside `data/papers.json` until reviewed. Record whether screening used the title, abstract, or full text. An author's venue announcement should remain distinct from a verified proceedings record.

For catalog changes, update the authoritative data, then run:

```sh
python scripts/catalog.py build
python scripts/catalog.py check
```

Include generated exports with the change. Preserve original source rows and explain corrections. Online catalog updates do not silently alter the literature coverage of a frozen manuscript version.
