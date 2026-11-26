"""Validate the catalog and generate public exports (Python standard library)."""
import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AXES = ['architectures', 'utilization', 'interpretation', 'mitigation', 'applications']


def load(name):
    return json.loads((ROOT / name).read_text())


def review_batches():
    return [load(str(path.relative_to(ROOT))) for path in sorted((ROOT/'data/reviews').glob('source-review-*.json'))]


def check():
    papers, taxonomy, migration = load('data/papers.json'), load('data/taxonomy.json'), load('data/migration.json')
    raw = load('data/sources/' + migration['source_id'] + '.json')
    source = {r['row']: r for r in raw['rows']}
    inherited = [p for p in papers if p['provenance']['source_id'] == migration['source_id']]
    added = [p for p in papers if p['provenance']['source_id'] != migration['source_id']]
    assert len(inherited) == migration['migrated_records'] == len(source)
    assert {p['provenance']['row'] for p in inherited} == set(source)
    assert len({p['id'] for p in papers}) == len(papers)
    arxiv_ids = [p['identifiers']['arxiv'] for p in papers if p['identifiers'].get('arxiv')]
    assert len(set(arxiv_ids)) == len(arxiv_ids)
    allowed = {a: set(taxonomy['core_axes'][a]['categories']) for a in taxonomy['core_axes']}
    allowed.update(applications=set(taxonomy['applications']), architectures=set(taxonomy['architectures']))
    aliases = {(x['axis'], x['source_label']): x['canonical_label'] for x in taxonomy['aliases']}
    cols = dict(zip(AXES, ['Models', 'Utilization', 'Understanding', 'Mitigation', 'Application']))
    for p in papers:
        assert p['title'] and p['links']['paper'].startswith(('https://', 'http://'))
        for axis in AXES:
            assert len(set(p['classification'][axis])) == len(p['classification'][axis])
            assert set(p['classification'][axis]) <= allowed[axis]
    for p in inherited:
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
    review_path = ROOT / 'data/reviews/source-review-2026-10-26.json'
    if added:
        review = load(str(review_path.relative_to(ROOT)))
        digest = hashlib.sha256(json.dumps(inherited, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        batches = review_batches()
        evidence = {}
        for batch in batches:
            assert digest == batch['baseline_records_digest_sha256']
            assert len(batch['included']) == batch['summary']['formal_additions']
            prior = [p for p in papers if p['provenance']['source_id'] < batch['review_id']]
            if batch.get('prior_catalog_digest_sha256'):
                assert len(prior) == batch['prior_catalog_records']
                assert hashlib.sha256(json.dumps(prior, ensure_ascii=False, sort_keys=True).encode()).hexdigest() == batch['prior_catalog_digest_sha256']
            for ev in batch['included']:
                assert ev['catalog_id'] not in evidence
                evidence[ev['catalog_id']] = (batch['review_id'], ev)
            for ev in batch['excluded']:
                if ev['basis'] == 'key_sections_of_full_text':
                    assert ev['source']['sha256'] and ev['sections']
        assert set(evidence) == {p['id'] for p in added}
        assert len(added) == sum(b['summary']['formal_additions'] for b in batches)
        assert len(papers) == batches[-1]['summary']['formal_total']
        for p in added:
            review_id, ev = evidence[p['id']]
            assert p['classification'] == ev['classification']
            assert p['title'] == ev['title'] and p['authors']
            assert p['provenance']['source_id'] == review_id
            assert p['provenance']['source_version'] == ev['source']['version']
            assert p['links']['full_text'] == ev['source']['url']
            assert p['links']['full_text'].endswith(p['identifiers']['arxiv'] + p['provenance']['source_version'])
            assert re.fullmatch(r'20\d{2}-\d{2}-\d{2}', p['date']['value'])
            assert p['date'] == {'value':ev['published'], 'precision':'day'}
            assert p['review']['sections'] and p['review']['classification_rationale'] and p['review']['limits']
            assert p['verification']['classification'] == 'source_sections_checked'
            assert re.fullmatch(r'[0-9a-f]{64}', ev['source']['sha256'])
            for key, ev_key in [('sections','sections'), ('finding','finding'), ('classification_rationale','rationale'), ('limits','limits'), ('fine_grained','fine_grained')]:
                assert p['review'][key] == ev[ev_key]
        state = discovery_state(through=review['review_id'])
        statuses = Counter(p['current_status'] for p in state)
        assert len(state) == review['summary']['new_to_baseline_retrieved']
        assert statuses['included'] == review['summary']['formal_additions']
        assert statuses['awaiting_source_review'] == review['summary']['pending']
        assert sum(statuses[s] for s in ['exclude', 'context_only', 'excluded_keyword_collision']) == review['summary']['excluded_or_context_only']
        assert {p['arxiv_id'] for p in state if p['current_status']=='awaiting_source_review'} == set(review['pending_arxiv_ids'])
    print(f'Validated {len(inherited)} original rows without change and {len(added)} evidence-linked additions ({len(papers)} total).')
    return papers


def discovery_state(through=None):
    """Overlay editorial outcomes without rewriting historical discovery snapshots."""
    first = load('data/candidates/arxiv-2026-10-26.json')
    records = {p['arxiv_id']:dict(p) for p in first['records']}
    supplement = ROOT / 'data/candidates/supplement-2026-10-26.json'
    if supplement.exists():
        for p in load(str(supplement.relative_to(ROOT)))['records']:
            if p['match_status']=='new_discovery':
                records[p['arxiv_id']] = dict(p)
    outcomes = {p['arxiv_id']:p for review in review_batches() if through is None or review['review_id'] <= through
                for p in review['included'] + review['excluded']}
    for ident,p in records.items():
        p['current_status'] = 'excluded_keyword_collision' if p.get('screening_status')=='excluded_keyword_collision' else 'awaiting_source_review'
        p['current_basis'] = p.get('screening_basis', 'metadata_only')
        p['current_note'] = p.get('screening_note', 'Supplemental discovery; scientific inclusion not yet reviewed.')
        if ident in outcomes:
            ev = outcomes[ident]
            p['current_status'] = 'included' if ev['decision']=='include' else ev['decision']
            p['current_basis'] = ev['basis']
            p['current_note'] = ev.get('rationale', ev.get('reason'))
    return sorted(records.values(), key=lambda p:(p['published'], p['arxiv_id']), reverse=True)


def csv_file(path, headers, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    # Avoid spreadsheet formulas in downloaded metadata exports.
    safe = lambda x: "'" + x if isinstance(x, str) and x.startswith(('=', '+', '-', '@')) else x
    with path.open('w', newline='', encoding='utf-8-sig') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(headers)
        w.writerows([[safe(x) for x in row] for row in rows])


def build():
    papers = check()
    heads = ['ID', 'Paper', 'Source date', 'Date precision', 'Publication',
             'Models', 'Fundamental Utilization', 'Mechanistic Interpretation',
             'Strategic Mitigation', 'Application', 'Paper URL', 'Source URL',
             'Legacy New', 'Source row', 'Classification status',
             'Legacy model labels', 'Legacy utilization labels', 'Legacy interpretation labels',
             'Legacy mitigation labels', 'Legacy application labels', 'Publication verification',
             'Relation to attention sinks', 'Checked source sections', 'Classification rationale',
             'Scope and limitations', 'Versioned full text']
    csv_file(ROOT / 'exports/papers.csv', heads, [
        [p['id'], p['title'], p['date']['value'], p['date']['precision'], p['publication']['label'],
         *['; '.join(p['classification'][a]) for a in AXES],
         p['links']['paper'], p['links']['original'], p.get('legacy_new_flag',''), p['provenance'].get('row',''),
         p['verification']['classification'], *['; '.join(p.get('legacy_tags',{}).get(a,[])) for a in AXES],
         p['publication']['verification'], p.get('review',{}).get('relation','legacy_imported'),
         *[p.get('review',{}).get(a,'') for a in ['sections','classification_rationale','limits']],
         p['links'].get('full_text','')] for p in papers])
    esc = lambda x: str(x).replace('|', '\\|').replace('\n', ' ')
    lines = ['# Surveyed paper catalog', '',
             f'{len(papers)} formal records: 208 inherited records and {len(papers)-208} source-section-reviewed additions.',
             'Inherited classification and publication labels were not reassessed. New labels are AI-assisted editorial assignments based on specified primary-source sections, not independent experimental verification.',
             'Dates retain source precision. The source `New` marker is historical.', '',
             '[CSV download](../exports/papers.csv) · [Canonical data](../data/papers.json) · [Migration notes](MIGRATION.md)', '',
             '[Latest classification evidence](REVIEW_20261028.md) · [First source-review batch](REVIEW_20261026.md). Empty categories mean unassigned; no subtype is forced onto a study.', '',
             '| Paper | Date | Models | Fundamental Utilization | Mechanistic Interpretation | Strategic Mitigation | Application | Classification basis |',
             '|---|---|---|---|---|---|---|---|']
    for p in papers:
        lines.append('| ' + ' | '.join([f"[{esc(p['title'])}]({p['links']['paper']})", p['date']['value'],
                                      *[esc('; '.join(p['classification'][a]) or '—') for a in AXES],
                                      p['verification']['classification']]) + ' |')
    path = ROOT / 'docs/CATALOG.md'
    path.parent.mkdir(exist_ok=True)
    path.write_text('\n'.join(lines) + '\n')
    candidate_path = ROOT / 'data/candidates/arxiv-2026-10-26.json'
    if candidate_path.exists():
        ledger = load(str(candidate_path.relative_to(ROOT)))
        state = discovery_state()
        candidates = [p for p in state if p['current_status']=='awaiting_source_review']
        ids = {p['identifiers'].get('arxiv') for p in papers if p['identifiers'].get('arxiv')}
        assert len({p['arxiv_id'] for p in candidates}) == len(candidates)
        assert not ids.intersection(p['arxiv_id'] for p in candidates)
        csv_file(ROOT / 'exports/candidates.csv',
                 ['arXiv ID', 'Paper', 'First submitted (UTC)', 'Latest revision (UTC)', 'Version',
                  'Authors', 'Screening status', 'Screening note', 'Paper URL', 'Authors publication note'],
                 [[p['arxiv_id'], p['title'], p['published'], p['updated'], p['version'],
                   '; '.join(p['authors']), p['current_status'], p['current_note'], p['url'],
                   p['publication_note']] for p in candidates])
        csv_file(ROOT / 'exports/retrieval-ledger.csv',
                 ['arXiv ID', 'Paper', 'First submitted (UTC)', 'Screening status', 'Screening basis', 'Screening note', 'Paper URL'],
                 [[p['arxiv_id'], p['title'], p['published'], p['current_status'], p['current_basis'], p['current_note'], p['url']]
                  for p in state])
        review_path = ROOT / 'data/reviews/source-review-2026-10-26.json'
        if review_path.exists():
            review = load(str(review_path.relative_to(ROOT)))
            all_included = [p for batch in review_batches() for p in batch['included']]
            csv_file(ROOT / 'exports/reviewed-additions.csv',
                     ['arXiv ID','Paper','Relation','Models','Fundamental Utilization','Mechanistic Interpretation',
                      'Strategic Mitigation','Application','Finding','Classification rationale','Limitations',
                      'Checked sections','Versioned full text','Review basis'],
                     [[p['arxiv_id'],p['title'],p['relation'],*['; '.join(p['classification'][a]) for a in AXES],
                       p['finding'],p['rationale'],p['limits'],p['sections'],p['source']['url'],p['basis']] for p in all_included])
            build_review_notes(review)
            for batch in review_batches()[1:]:
                build_later_review_notes(batch)
    print('Generated public catalog and CSV exports.')


def build_review_notes(review):
    s=review['summary']
    lines=['# Source-grounded literature integration — 26 October 2026','',
           'This page documents the narrower source-review stage. The subsequent user-expanded [broad library](LIBRARY.md) includes citation-linked and attention-concentration resources, with reading depth and relation evidence shown separately. Its wider collection does not alter the evidence behind these 24 classifications.','',
           f"At this stage, the formal catalog contained **{s['formal_total']} papers**: 208 unchanged inherited records and **{s['formal_additions']} additions**. Of the additions, {s['recent_additions_since_june']} were first submitted in June–October and {s['earlier_omissions_added']} repairs an earlier omission. See the [current catalog](CATALOG.md) for subsequent batches.",'',
           '## Reading and classification basis','',review['review_method'],'',
           'The fourteen method categories and nine application names are unchanged. Fine-grained mechanisms are retained separately. Empty method labels are intentional when the existing taxonomy does not precisely fit. Registers, high norms, output gates, null logits, and attention-mass transfer are not interchangeable concepts.','',
           '## Coverage','',
           f"Four arXiv query families produced {s['new_to_baseline_retrieved']} distinct records absent from the inherited baseline. Outcomes on 26 October: {s['formal_additions']} included, {s['pending']} awaiting source review, and {s['excluded_or_context_only']} excluded or contextual only. Discovery snapshots are preserved; the current [ledger](../exports/retrieval-ledger.csv) overlays later editorial outcomes.",'',
           'Supplemental searches expanded `sink`/`sinks`, null/gated attention, and spectral terminology, and checked January–May omissions. [Exact queries, pagination and response hashes](../data/candidates/supplement-2026-10-26.json) supplement the [initial snapshot](SEARCH.md). Targeted ACL Anthology and OpenReview checks are not a complete proceedings search. The ACL 2026 GPT-2 mechanistic paper matched an existing record (arXiv:2604.14722), so no duplicate was added.','',
           *['- '+x for x in review['limits']],'',
           '## Included papers and evidence','',
           'Download the [reviewed additions CSV](../exports/reviewed-additions.csv) or inspect the [review decisions](../data/reviews/source-review-2026-10-26.json). Full texts are linked, not redistributed.','']
    taxonomy=load('data/taxonomy.json')
    for p in review['included']:
        lines += [f"### [{p['title']}]({p['source']['url']})",'',
                  f"**Source:** {p['arxiv_id']}{p['source']['version']}; checked {p['sections']}. **Relation:** `{p['relation']}`.",'',
                  '**Finding.** '+p['finding'],'']
        for axis in ['utilization','interpretation','mitigation']:
            labels=p['classification'][axis]
            if labels: lines += ['**'+taxonomy['core_axes'][axis]['name']+':** '+ '; '.join(labels)+'.','']
        lines += ['**Classification.** '+p['rationale'],'',
                  '**Fine-grained terms:** '+ '; '.join(p['fine_grained'])+'.','',
                  '**Limits.** '+p['limits'],'']
    lines += ['## Additional exclusions and context','']
    for p in review['excluded']:
        lines += [f"- [{p['title']}]({p['source_url']}): {p['reason']} Basis: {p['basis']}."]
    (ROOT/'docs/REVIEW_20261026.md').write_text('\n'.join(lines)+'\n')


def build_later_review_notes(review):
    s=review['summary'];taxonomy=load('data/taxonomy.json')
    lines=['# Source review and classification — '+review['as_of'], '',
           f"**{s['formal_additions']} newly classified papers** bring the catalog to **{s['formal_total']} records**. **{s['context_decisions']} other papers** remain reviewed context. All original 208 rows and the previous 24 additions are unchanged.", '',
           review['review_method'], '', review['selection'], '',
           f"This batch includes {s['new_primary_readings']} new key-section readings and scope reassessment of {s['prior_readings_reassessed']} prior readings. The dated arXiv query returned {review['new_search_records']} additional records; that is a bounded query result, not proof of complete coverage.", '',
           '[Canonical decisions and query audit](../data/reviews/'+review['review_id']+'.json) · [All classified papers](CATALOG.md) · [Complete library](LIBRARY.md)', '',
           '## Classified additions','']
    for p in review['included']:
        lines += [f"### [{p['title']}]({p['source']['url']})",'',
                  f"**Checked:** {p['sections']}. **Relation:** `{p['relation']}`.",'',
                  '**Finding.** '+p['finding'],'']
        for a in ['utilization','interpretation','mitigation']:
            if p['classification'][a]:lines += ['**'+taxonomy['core_axes'][a]['name']+':** '+'; '.join(p['classification'][a])+'.','']
        lines += ['**Classification.** '+p['rationale'],'','**Limits.** '+p['limits'],'']
    lines += ['## Reviewed context without forced sink-method labels','']
    for p in review['excluded']:
        lines += [f"### [{p['title']}]({p['source_url']})",'',
                  '**Checked:** '+p['sections']+'.','','**Finding.** '+p['finding'],'',
                  '**Scope decision.** '+p['reason'],'','**Limits.** '+p['limits'],'']
    lines += ['## Scope limits','',*['- '+x for x in review['limits']]]
    (ROOT/'docs'/('REVIEW_'+review['as_of'].replace('-','')+'.md')).write_text('\n'.join(lines)+'\n')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('command', choices=['check', 'build'])
    args = ap.parse_args()
    build() if args.command == 'build' else check()
