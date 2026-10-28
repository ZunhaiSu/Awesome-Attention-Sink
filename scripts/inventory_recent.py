"""Retrieve recent arXiv metadata into a separate, unmerged candidate inventory.

This discovers candidates; it does not infer taxonomy labels or acceptance.
"""
import argparse
import datetime as dt
import difflib
import hashlib
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = {'a': 'http://www.w3.org/2005/Atom', 'ar': 'http://arxiv.org/schemas/atom',
      'o': 'http://a9.com/-/spec/opensearch/1.1/'}


def norm(value):
    return ''.join(c for c in value.casefold() if c.isalnum())


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def query_arxiv(query, cache, name):
    entries, pages, total, start = [], [], None, 0
    while total is None or start < total:
        params = {'search_query': query, 'start': start, 'max_results': 200,
                  'sortBy': 'submittedDate', 'sortOrder': 'descending'}
        url = 'https://export.arxiv.org/api/query?' + urllib.parse.urlencode(params)
        req = urllib.request.Request(url, headers={'User-Agent': 'AttentionSinkCatalog/1.0 (public literature metadata)'})
        with urllib.request.urlopen(req, timeout=35) as response:
            blob = response.read()
        page = ET.fromstring(blob)
        total = int(page.findtext('o:totalResults', default='0', namespaces=NS))
        found = page.findall('a:entry', NS)
        if total and not found:
            raise RuntimeError('arXiv returned an incomplete page; inventory is not complete.')
        cache.mkdir(parents=True, exist_ok=True)
        (cache / f'{name}-{start}.xml').write_bytes(blob)
        pages.append({'url': url, 'sha256': hashlib.sha256(blob).hexdigest(),
                      'start': start, 'returned': len(found), 'total_results': total})
        for entry in found:
            get = lambda key: entry.findtext(key, default='', namespaces=NS)
            match = re.search(r'(\d{4}\.\d{4,5})(v\d+)?$', get('a:id'))
            if not match:
                raise ValueError('Unexpected arXiv entry identifier: ' + get('a:id'))
            entries.append({
                'arxiv_id': match[1], 'version': match[2] or '',
                'title': ' '.join(get('a:title').split()),
                'published': get('a:published')[:10], 'updated': get('a:updated')[:10],
                'authors': [a.findtext('a:name', default='', namespaces=NS) for a in entry.findall('a:author', NS)],
                'url': 'https://arxiv.org/abs/' + match[1],
                'publication_note': get('ar:journal_ref') or get('ar:comment'),
                'doi': get('ar:doi') or None,
                # Keep abstracts only in the local retrieval cache for screening.
                '_abstract': ' '.join(get('a:summary').split()),
            })
        start += len(found)
        if start < total:
            time.sleep(3.2)
    return entries, pages


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--since', default='2026-06-01')
    ap.add_argument('--until', default='2026-10-26')
    ap.add_argument('--cache', type=Path, required=True)
    args = ap.parse_args()
    if (ROOT / 'data/reviews' / f'source-review-{args.until}.json').exists():
        raise SystemExit('This discovery snapshot has review decisions. Preserve it and retrieve into a new dated or supplemental snapshot.')
    for value in [args.since, args.until]:
        dt.date.fromisoformat(value)
    date_filter = f'submittedDate:[{args.since.replace("-", "")}0000 TO {args.until.replace("-", "")}2359]'
    queries = {
        'direct_sink': '(ti:"attention sink" OR abs:"attention sink" OR ti:"attention sinks" OR abs:"attention sinks") AND ' + date_filter,
        'related_outlier_register': '(ti:"massive activation" OR ti:"massive activations" OR ti:"register token" OR ti:"register tokens" OR ti:"registers") AND (cat:cs.LG OR cat:cs.CL OR cat:cs.CV OR cat:cs.AI OR cat:stat.ML) AND ' + date_filter,
    }
    migrated = json.loads((ROOT / 'data/papers.json').read_text())
    old_ids = {p['identifiers']['arxiv']: p for p in migrated if p['identifiers'].get('arxiv')}
    old_dois = {p['identifiers']['doi'].casefold(): p for p in migrated if p['identifiers'].get('doi')}
    old_titles = {norm(p['title']): p for p in migrated}
    records, queries_out, duplicates, cached = {}, [], [], {}
    for ix, (name, query) in enumerate(queries.items()):
        if ix:
            time.sleep(3.2)
        found, pages = query_arxiv(query, args.cache, name)
        queries_out.append({'name': name, 'query': query, 'pages': pages})
        print(name, 'returned', len(found), flush=True)
        for paper in found:
            ident = paper['arxiv_id']
            cached[ident] = paper.copy()
            assert args.since <= paper['published'] <= args.until
            if ident in records:
                records[ident]['retrieved_by'].append(name)
                continue
            duplicate = old_ids.get(ident) or old_titles.get(norm(paper['title']))
            if not duplicate and paper['doi']:
                duplicate = old_dois.get(paper['doi'].casefold())
            if duplicate:
                duplicates.append({'arxiv_id': ident, 'catalog_id': duplicate['id'], 'retrieved_by': name})
                continue
            record = {k: v for k, v in paper.items() if not k.startswith('_')}
            record.update(retrieved_by=[name], screening_status='awaiting_review',
                          screening_note='Not in the migrated baseline by identifier or exact normalized title; scientific inclusion remains unreviewed.',
                          possible_baseline_matches=[])
            for title, old in old_titles.items():
                ratio = difflib.SequenceMatcher(None, norm(paper['title']), title).ratio()
                if ratio >= 0.78:
                    record['possible_baseline_matches'].append({'catalog_id': old['id'], 'title': old['title'], 'similarity': round(ratio, 3)})
            records[ident] = record
    papers = sorted(records.values(), key=lambda p: (p['published'], p['arxiv_id']), reverse=True)
    summary = {
        'as_of': args.until, 'publication_window': [args.since, args.until], 'date_basis': 'arXiv first submitted date, UTC',
        'baseline_records': len(migrated), 'retrieval_queries': len(queries_out),
        'retrieved_entries_before_cross_query_dedup': sum(sum(p['returned'] for p in q['pages']) for q in queries_out),
        'unique_retrieved_arxiv_ids': len(cached),
        'matched_existing_records': len({p['arxiv_id'] for p in duplicates}),
        'candidate_records': len(papers),
        'direct_sink_candidates': sum('direct_sink' in p['retrieved_by'] for p in papers),
        'related_only_candidates': sum('direct_sink' not in p['retrieved_by'] for p in papers),
        'possible_title_matches': sum(bool(p['possible_baseline_matches']) for p in papers),
        'by_month': dict(sorted(Counter(p['published'][:7] for p in papers).items())),
        'new_formal_inclusions': 0,
    }
    result = {'summary': summary, 'queries': queries_out, 'existing_matches': duplicates,
              'limits': ['This is a keyword-bounded discovery inventory, not exhaustive field coverage.',
                         'All query pages were fetched; inclusion and taxonomy require human review.',
                         'Related outlier/register hits do not establish attention-sink evidence.',
                         'Different-title versions without shared identifiers can require manual resolution.',
                         'The publication window does not detect every revision of older work.',
                         'arXiv comments are author-supplied and do not independently verify acceptance.'],
              'records': papers}
    save(ROOT / 'data/candidates' / f'arxiv-{args.until}.json', result)
    save(args.cache / 'screening_metadata.json', list(cached.values()))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
