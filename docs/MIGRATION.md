# Feishu catalog migration

The 2026-10-26 migration preserves the supplied **AS Paper List.xlsx** as a row-level source snapshot in `data/sources/feishu-2026-10-26.json`. The original file's SHA-256 is recorded there. No source row is discarded or scientifically reclassified.

`data/papers.json` is the authoritative migrated catalog. `exports/papers.csv` and `docs/CATALOG.md` are generated from it. New literature is inventoried separately and does not change this baseline.

## Terminology and provenance

- All 14 formal method categories and nine application categories retain the names used in the revised survey. The complete label mapping is in `data/taxonomy.json`.
- Legacy labels, including finer distinctions under “Others”, remain beside canonical labels and in the original row snapshot. For example, both legacy Softmax Limitations and No-Op Theory labels map to **Softmax Limitations and No-Op Theory**, without dropping the individual source tags.
- Spelling variants such as `Outliers Circuits` and `Mechansim Interpretability` are mapped to **Outlier Circuits** and **Mechanism Interpretability**. This normalizes terminology, not evidence or scientific scope.
- Empty or `N/A` categories mean unassigned in the source. They do not establish absence of the corresponding mechanism.
- Publication labels are imported as supplied and explicitly marked as not independently reverified. Links to an abstract, preprint, project, or publisher page retain their original provenance.
- Legacy `DATE` is YYMM. `2500` means year precision (2025); `2605` means month precision (May 2026). Neither is converted to an invented publication day.
- The legacy `New` marker is preserved as a historical flag. It is not counted as newly discovered literature in this update.
- Migration verification checks source preservation; it does not claim that every original paper has been reread.

## Reproduce

The one-time importer requires `openpyxl`. From this repository:

```sh
python scripts/import_feishu.py /path/to/AS\ Paper\ List.xlsx --date 2026-10-26
python scripts/catalog.py build
```

Normal validation and export use only Python's standard library:

```sh
python scripts/catalog.py check
python scripts/catalog.py build
```

The supplied workbook is not modified. The website and manuscript projects are outside this migration step.
