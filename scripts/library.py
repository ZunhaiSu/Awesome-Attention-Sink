"""Build the broad, deduplicated library while preserving the original taxonomy subset."""
import argparse
from collections import Counter

from catalog import AXES, ROOT, check as check_core, csv_file, load

def merged():
 broad=load('data/library/broad-2026-10-26.json')
 rows={p['id']:dict(p) for p in broad['records']}
 current_notes={p['arxiv_id']:p for p in load('data/library/concentration-reading-2026-10-26.json')['records']}
 for p in rows.values():
  if p['identifiers'].get('arxiv') in current_notes:
   p['reading_note']={**p.get('reading_note',{}),**current_notes[p['identifiers']['arxiv']]}
  p['classification']={a:[] for a in AXES}
  p['classification_status']='unassigned'
  p['date_precision']='day'
  p['source_row']=''
  note=p.get('reading_note')
  if note:
   p['review_note']=note['finding']+' Limits: '+note['limits']
   p['review_url']=note['source_url']
  elif p.get('context_reading_note'):
   p['review_note']=p['context_reading_note']['reason']
   p['review_url']=p['context_reading_note']['source']['url']
  else:p['review_note']='';p['review_url']=''
 for core in load('data/papers.json'):
  p=rows.get(core['id'],{})
  ev=list(dict.fromkeys(['prior_classified_catalog']+p.get('evidence',[])))
  p.update(id=core['id'],title=core['title'],identifiers={**p.get('identifiers',{}),**core['identifiers']},
   authors=core.get('authors',p.get('authors',[])),date=core['date']['value'],date_precision=core['date']['precision'],
   date_basis='Original source precision' if core['verification']['classification']=='legacy_imported' else 'arXiv first submitted, UTC',
   links=core['links'],evidence=ev,classification=core['classification'],
   classification_status=core['verification']['classification'],source_row=core['provenance'].get('row',''))
  p.setdefault('reading_status','legacy_imported_not_reassessed')
  p.setdefault('metadata_sources',[])
  p.setdefault('review_note','');p.setdefault('review_url','');p.setdefault('identifier_note','')
  if core.get('review'):
   p['reading_status']='key_sections_checked'
   p['review_note']=core['review']['finding']+' Limits: '+core['review']['limits']
   p['review_url']=core['links']['full_text']
  rows[core['id']]=p
 return sorted(rows.values(),key=lambda p:(p['date'],p['id']),reverse=True)

def stats(rows):
 return {'library_records':len(rows),
  'prior_classified_records':sum(p['classification_status']!='unassigned' for p in rows),
  'additional_to_prior_catalog':sum(p['classification_status']=='unassigned' for p in rows),
  'evidence_counts':dict(Counter(e for p in rows for e in p['evidence'])),
  'reading_status_counts':dict(Counter(p['reading_status'] for p in rows))}

def check():
 check_core()
 broad=load('data/library/broad-2026-10-26.json')
 rows=merged();s=stats(rows)
 assert len({p['id'] for p in rows})==len(rows)
 assert s['library_records']==len(load('data/papers.json'))+broad['summary']['additional_to_core']
 assert s['prior_classified_records']==232
 assert len({x for p in broad['records'] for x in p['source_work_ids']})==broad['summary']['openalex_unique_records']
 for q in broad['queries']:
  assert q['pagination_complete']
  assert sum(p['returned'] for p in q['pages'])==q['returned']
 for p in rows:
  assert p['title'] and p['evidence'] and p['links']['paper'].startswith(('http://','https://'))
  if 'citation_in_primary_reference_list' in p['evidence']:
   ev=p['reference_check'];assert ev['status']=='reference_verified' and ev['matches'] and ev['sha256']
  if p['classification_status']=='unassigned':assert not any(p['classification'][a] for a in AXES)
 assert s['evidence_counts']['citation_in_primary_reference_list']==broad['summary']['reference_lists_verified']
 assert s['reading_status_counts']['key_sections_checked']==28
 assert s['reading_status_counts']['key_sections_checked_context']==1
 print(f"Validated broad library: {len(rows)} records; relation evidence and reading depth kept distinct.")
 return rows

def build():
 rows=check();s=stats(rows);broad=load('data/library/broad-2026-10-26.json')
 csv_file(ROOT/'exports/library.csv',
  ['ID','Paper','Date','Date precision','Date basis','Reading status','Relation evidence','Models',
   'Fundamental Utilization','Mechanistic Interpretation','Strategic Mitigation','Application',
   'Classification basis','Authors','Paper URL','Reading note and limitations','Checked full text',
   'Metadata sources','Identity note','Original source row'],
  [[p['id'],p['title'],p['date'],p['date_precision'],p['date_basis'],p['reading_status'],'; '.join(p['evidence']),
    *['; '.join(p['classification'][a]) for a in AXES],p['classification_status'],'; '.join(p['authors']),
    p['links']['paper'],p['review_note'],p['review_url'],'; '.join(p['metadata_sources']),p['identifier_note'],p['source_row']] for p in rows])
 import json
 (ROOT/'exports/library-summary.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
 lines=['# Broad attention-sink and attention-concentration library','',
  f"**{len(rows):,} bibliographic records**, including the unchanged 232-record classified subset and {s['additional_to_prior_catalog']:,} additional records. The user-expanded scope includes papers citing StreamingLLM and related attention-concentration work. A title/abstract does not need to contain the exact phrase attention sink.",'',
  '[Download the complete library CSV](../exports/library.csv) · [Source snapshot and exact queries](../data/library/broad-2026-10-26.json) · [Additional source readings](BROAD_READING.md) · [Original classification subset](CATALOG.md)','',
  '## Inclusion evidence','',
  '- `seed_citation_index`: OpenAlex indexes a citation edge to StreamingLLM. The index can miss or mismatch references.',
  '- `seed_title_fulltext_index`: an exact-title full-text index query matched the seed title. This is a discovery signal and is not described as a checked citation.',
  '- `citation_in_primary_reference_list`: the seed title or arXiv ID was found in the linked primary paper’s bibliography, with a locator and source hash.',
  '- `attention_concentration_keywords`: arXiv title/abstract retrieval covers concentration, attention/entropy collapse, saturation, and attention entropy. Scientific relevance may still need reading.',
  '- Prior sink/register leads and the previously contextual RATS paper remain available in this broader collection.','',
  '## Search completeness and reading depth','',
  'All pages returned by the documented queries were retrieved. The source queries yielded 54 citation-edge records and 1,971 exact-title full-text hits in OpenAlex (2,009 unique OpenAlex IDs), plus 198 arXiv concentration records. Identifier/title deduplication and reconciliation with the prior catalog produce the library total above. These are bibliographic records; publication versions without a shared identifier or title may remain separate.','',
  'The 60 newest arXiv-linked discovery records were checked for the seed reference: 57 bibliographies confirmed it; 3 HTML versions were unavailable. This convenience batch is not a representative sample. The remaining index hits are not claimed to have been read or citation-verified.','',
  'Twenty-eight records have specified key-section checks (24 from the prior update and 4 new concentration readings), and one has a contextual key-section reading. The original 208 classifications remain inherited. Reading a reference list alone does not verify a method classification.','',
  'Coverage remains limited by index updates, unavailable full texts, vocabulary, and unresolved publication versions. A citation can be background-only; it does not by itself establish direct sink research. Low-rank/smoothed attention and low per-query entropy also require different interpretations.','',
  'The fourteen method categories and nine application names remain intact. Unread or broader related records can have empty method labels. The broad library is a collection of potential resources for the survey, and inclusion does not automatically add a claim or citation to a frozen manuscript.','',
  'Primary index documentation: [OpenAlex citations](https://help.openalex.org/data/works/citations/) and [paging](https://help.openalex.org/api/paging/). The seed is [Efficient Streaming Language Models with Attention Sinks](https://arxiv.org/abs/2309.17453).','',
  '## Latest 100 records','',
  'The complete collection is in the CSV above. Dates below preserve their source basis; an indexed publication date is not necessarily first arXiv submission.','',
  '| Paper | Date | Reading status | Relation evidence |','|---|---|---|---|']
 esc=lambda x:str(x).replace('|','\\|').replace('\n',' ')
 for p in rows[:100]:
  lines.append('| '+ ' | '.join([f"[{esc(p['title'])}]({p['links']['paper']})",p['date'],p['reading_status'],esc('; '.join(p['evidence']))])+' |')
 (ROOT/'docs/LIBRARY.md').write_text('\n'.join(lines)+'\n')
 notes=load('data/library/concentration-reading-2026-10-26.json')
 by_arxiv={p['identifiers'].get('arxiv'):p for p in rows if p['identifiers'].get('arxiv')}
 lines=['# Additional attention-concentration readings','',notes['review_method'],'']
 for p in notes['records']:
  lines += [f"## [{by_arxiv[p['arxiv_id']]['title']}]({p['source_url']})",'',
    '**Checked sections:** '+p['sections']+'.','',
    '**Finding.** '+p['finding'],'','**Relevance.** '+p['relevance'],'',
    '**Limits.** '+p['limits'],'','**Taxonomy.** '+p['taxonomy_note'],'']
 (ROOT/'docs/BROAD_READING.md').write_text('\n'.join(lines)+'\n')
 print(json.dumps(s,indent=2))

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('command',choices=['check','build']);args=ap.parse_args()
 build() if args.command=='build' else check()
