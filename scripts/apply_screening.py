"""Apply explicit, versioned screening decisions to the discovery ledger."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-26'


def main():
    path = ROOT / f'data/candidates/arxiv-{DATE}.json'
    data = json.loads(path.read_text())
    decisions = json.loads((ROOT / f'data/screening/{DATE}.json').read_text())
    related = decisions['related_candidates']
    checked = decisions['sink_abstract_checked']
    encountered = set()
    for p in data['records']:
        ident = p['arxiv_id']
        if 'direct_sink' in p['retrieved_by']:
            p['screening_status'] = 'sink_keyword_candidate'
            p['screening_basis'] = 'abstract_checked' if ident in checked else 'keyword_retrieval_only'
            p['screening_note'] = checked.get(ident, 'Contains attention-sink terminology in title or abstract; relevance and taxonomy need review.')
        elif ident in related:
            encountered.add(ident)
            p['screening_status'] = 'related_candidate'
            p['screening_basis'] = 'title_and_abstract_excerpt'
            p['screening_note'] = related[ident]
        else:
            p['screening_status'] = 'excluded_keyword_collision'
            p['screening_basis'] = 'title_screening'
            p['screening_note'] = ('Register/registered refers to preregistration, linguistic style, geometric registration, '
                                   'hardware or another non-target use, rather than Transformer registers or massive activations.')
    assert encountered == set(related), 'A screening override did not resolve to a retrieved record.'
    retained = [p for p in data['records'] if p['screening_status'] != 'excluded_keyword_collision']
    s = data['summary']
    s['retrieval_records_before_screening'] = len(data['records'])
    s['candidate_records'] = len(retained)
    s['direct_sink_candidates'] = sum(p['screening_status'] == 'sink_keyword_candidate' for p in retained)
    s['related_only_candidates'] = sum(p['screening_status'] == 'related_candidate' for p in retained)
    s['excluded_keyword_collisions'] = len(data['records']) - len(retained)
    s['abstract_checked_sink_candidates'] = sum(p['screening_status'] == 'sink_keyword_candidate' and p['screening_basis'] == 'abstract_checked' for p in retained)
    s['by_month'] = dict(sorted(Counter(p['published'][:7] for p in retained).items()))
    s['by_month_and_scope'] = {
        month: {scope: sum(p['published'].startswith(month) and p['screening_status'] == scope for p in retained)
                for scope in ['sink_keyword_candidate', 'related_candidate']}
        for month in s['by_month']}
    s['screening_state'] = 'Initial inventory; not an accepted-paper count'
    # All retrieval records remain in the ledger, including exclusions.
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(s, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
