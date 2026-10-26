"""Validate the catalog and generate public exports (Python standard library)."""
import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AXES = ['architectures', 'utilization', 'interpretation', 'mitigation', 'applications']


def load(name):
    return json.loads((ROOT / name).read_text())


def check():
    papers, taxonomy, migration = load('data/papers.json'), load('data/taxonomy.json'), load('data/migration.json')
    raw = load('data/sources/' + migration['source_id'] + '.json')
    source = {r['row']: r for r in raw['rows']}
    assert len(papers) == migration['migrated_records'] == len(source)
    assert len({p['id'] for p in papers}) == len(papers)
    allowed = {a: set(taxonomy['core_axes'][a]['categories']) for a in taxonomy['core_axes']}
    allowed.update(applications=set(taxonomy['applications']), architectures=set(taxonomy['architectures']))
    aliases = {(x['axis'], x['source_label']): x['canonical_label'] for x in taxonomy['aliases']}
    cols = dict(zip(AXES, ['Models', 'Utilization', 'Understanding', 'Mitigation', 'Application']))
    for p in papers:
        assert p['title'] and p['links']['paper'].startswith(('https://', 'http://'))
        v = source[p['provenance']['row']]['values']
        assert p['title'] == v['Paper'].strip() and p['links']['original'] == v['Link']
        assert p['publication']['label'] == v['Pub']
        assert p['legacy_new_flag'] == (v['Label'] == 'New')
        digits = str(v['DATE'])
        precision = 'year' if digits.endswith('00') else 'month'
        expected = str(2000 + int(digits[:2])) + ('' if precision == 'year' else '-' + digits[-2:])
        assert p['date'] == {'value': expected, 'precision': precision}
        for axis in AXES:
            tags = [] if v[cols[axis]] in {None, '', 'N/A'} else [t.strip() for t in v[cols[axis]].split(',')]
            assert tags == p['legacy_tags'][axis]
            expected_tags = list(dict.fromkeys(aliases[(axis, t)] for t in tags))
            assert expected_tags == p['classification'][axis]
            assert set(p['classification'][axis]) <= allowed[axis]
    assert sum(len(v['categories']) for v in taxonomy['core_axes'].values()) == 14
    assert len(taxonomy['applications']) == 9
    print(f'Validated {len(papers)} migrated records against every original row and category mapping.')
    return papers


def csv_file(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    # Avoid spreadsheet formulas in downloaded metadata exports.
    safe = lambda x: "'" + x if isinstance(x, str) and x.startswith(('=', '+', '-', '@')) else x
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows([[safe(x) for x in row] for row in rows])


def build():
    papers = check()
    heads = ['ID', 'Paper', 'Source date', 'Date precision', 'Publication (imported)',
             'Models', 'Fundamental Utilization', 'Mechanistic Interpretation',
             'Strategic Mitigation', 'Application', 'Paper URL', 'Source URL',
             'Legacy New', 'Source row', 'Classification status',
             'Legacy model labels', 'Legacy utilization labels', 'Legacy interpretation labels',
             'Legacy mitigation labels', 'Legacy application labels']
    csv_file(ROOT / 'exports/papers.csv', heads, [
        [p['id'], p['title'], p['date']['value'], p['date']['precision'], p['publication']['label'],
         *['; '.join(p['classification'][a]) for a in AXES],
         p['links']['paper'], p['links']['original'], p['legacy_new_flag'], p['provenance']['row'],
         p['verification']['classification'], *['; '.join(p['legacy_tags'][a]) for a in AXES]] for p in papers])
    esc = lambda x: str(x).replace('|', '\\|').replace('\n', ' ')
    lines = ['# Surveyed paper catalog', '',
             f'{len(papers)} records migrated from the supplied Feishu export on 2026-10-26.',
             'Classification and publication labels are inherited; they were not reassessed during migration.',
             'Dates retain source precision. The source `New` marker is historical.', '',
             '[CSV download](../exports/papers.csv) · [Canonical data](../data/papers.json) · [Migration notes](MIGRATION.md)', '',
             '| Paper | Date | Models | Fundamental Utilization | Mechanistic Interpretation | Strategic Mitigation | Application |',
             '|---|---|---|---|---|---|---|']
    for p in papers:
        lines.append('| ' + ' | '.join([f"[{esc(p['title'])}]({p['links']['paper']})", p['date']['value'],
                                      *[esc('; '.join(p['classification'][a]) or '—') for a in AXES]]) + ' |')
    path = ROOT / 'docs/CATALOG.md'
    path.parent.mkdir(exist_ok=True)
    path.write_text('\n'.join(lines) + '\n')
    candidate_path = ROOT / 'data/candidates/arxiv-2026-10-26.json'
    if candidate_path.exists():
        candidates = load(str(candidate_path.relative_to(ROOT)))['records']
        ids = {p['identifiers'].get('arxiv') for p in papers if p['identifiers'].get('arxiv')}
        assert len({p['arxiv_id'] for p in candidates}) == len(candidates)
        assert not ids.intersection(p['arxiv_id'] for p in candidates)
        csv_file(ROOT / 'exports/candidates.csv',
                 ['arXiv ID', 'Paper', 'First submitted (UTC)', 'Latest revision (UTC)', 'Version',
                  'Authors', 'Screening status', 'Screening note', 'Paper URL', 'Authors publication note'],
                 [[p['arxiv_id'], p['title'], p['published'], p['updated'], p['version'],
                   '; '.join(p['authors']), p['screening_status'], p['screening_note'], p['url'],
                   p['publication_note']] for p in candidates])
    print('Generated public catalog and CSV exports.')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=['check', 'build'])
    args = ap.parse_args()
    build() if args.command == 'build' else check()
