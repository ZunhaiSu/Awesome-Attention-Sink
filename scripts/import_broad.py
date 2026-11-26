"""Normalize broad bibliographic leads and preserve the evidence behind each relation."""
import argparse
import hashlib
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

from catalog import AXES, ROOT, discovery_state, load

def norm(s):return ''.join(c for c in unicodedata.normalize('NFKC',s).casefold() if c.isalnum())
def save(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cache',type=Path,required=True)
 ap.add_argument('--fulltext-cache',type=Path,required=True);args=ap.parse_args()
 oa=json.loads((args.cache/'openalex_metadata.json').read_text())
 conc=json.loads((args.cache/'concentration_metadata.json').read_text())
 refs=json.loads((args.cache/'reference_checks.json').read_text())
 core=load('data/papers.json')
 reading=load('data/library/concentration-reading-2026-10-26.json')
 by_core_title={norm(p['title']):p['id'] for p in core}
 by_core_arxiv={p['identifiers']['arxiv']:p['id'] for p in core if p['identifiers'].get('arxiv')}
 by_core_doi={p['identifiers']['doi'].casefold():p['id'] for p in core if p['identifiers'].get('doi')}
 records={};by_arxiv={};by_doi={};by_title={};self_hits=[]

 def add(item):
  arxiv=item['identifiers'].get('arxiv');doi=item['identifiers'].get('doi')
  title_key=norm(item['title'])
  if arxiv=='2604.10098' or title_key==norm('Attention Sink in Transformers: A Survey on Utilization, Interpretation, and Mitigation'):
   self_hits.append(item['id']);return
  catalog_id=by_core_arxiv.get(arxiv) or by_core_doi.get(doi) or by_core_title.get(title_key)
  key=by_arxiv.get(arxiv) if arxiv else None
  key=key or (by_doi.get(doi) if doi else None)
  if not key and catalog_id in records:key=catalog_id
  if not key:
   title_match=by_title.get(title_key)
   other=records[title_match]['identifiers'].get('arxiv') if title_match else None
   if arxiv and other and arxiv!=other:
    item['identifier_note']='Exact title but a different arXiv ID; kept separate for version/identity review.'
   else:key=title_match
  if not key:
   key=catalog_id or item['id'];item['id']=key;item['core_catalog_id']=catalog_id
   records[key]=item
  else:
   old=records[key]
   if catalog_id:
    assert not old.get('core_catalog_id') or old['core_catalog_id']==catalog_id
    old['core_catalog_id']=catalog_id
   old['evidence']=list(dict.fromkeys(old['evidence']+item['evidence']))
   old['source_work_ids']=list(dict.fromkeys(old['source_work_ids']+item['source_work_ids']))
   old['metadata_sources']=list(dict.fromkeys(old['metadata_sources']+item['metadata_sources']))
   old['title_variants']=list(dict.fromkeys(old['title_variants']+item['title_variants']))
   if arxiv and not old['identifiers'].get('arxiv'):old['identifiers']['arxiv']=arxiv
   if doi and not old['identifiers'].get('doi'):old['identifiers']['doi']=doi
   if item['date_basis']=='arXiv first submitted, UTC':
    old['date']=item['date'];old['date_basis']=item['date_basis'];old['links']['paper']=item['links']['paper']
   if not old['authors']:old['authors']=item['authors']
  if arxiv:by_arxiv[arxiv]=key
  if doi:by_doi[doi]=key
  by_title[title_key]=key

 for p in oa['records']:
  urls=[p.get('doi') or '']
  for loc in p.get('locations',[]):
   urls += [loc.get('landing_page_url') or '',loc.get('pdf_url') or '']
  aids=sorted(set(re.findall(r'(?:arxiv\.org/(?:abs|pdf)/|arxiv\.)(\d{4}\.\d{4,5})',' '.join(urls),re.I)))
  identifiers={}
  if len(aids)==1:identifiers['arxiv']=aids[0]
  if p.get('doi'):identifiers['doi']=p['doi'].removeprefix('https://doi.org/').casefold()
  ident=('as-arxiv-'+aids[0]) if len(aids)==1 else 'as-openalex-'+p['id'].split('/')[-1]
  ev=[]
  if 'seed_citation_edges' in p['retrieved_by']:
   assert 'https://openalex.org/W4387294617' in p['referenced_works']
   ev.append('seed_citation_index')
  if 'seed_title_fulltext_mentions' in p['retrieved_by']:ev.append('seed_title_fulltext_index')
  link='https://arxiv.org/abs/'+aids[0] if len(aids)==1 else ((p.get('primary_location') or {}).get('landing_page_url') or p.get('doi') or p['id'])
  add({'id':ident,'title':p['title'],'title_variants':[p['title']],'identifiers':identifiers,
   'authors':[a['author']['display_name'] for a in p['authorships'] if a.get('author') and a['author'].get('display_name')],
   'date':p['publication_date'],'date_basis':'OpenAlex indexed publication date; not necessarily arXiv first submission',
   'links':{'paper':link},'evidence':ev,'source_work_ids':[p['id']],
   'metadata_sources':[p['id'].replace('https://openalex.org/','https://api.openalex.org/works/')],
   'reading_status':'index_metadata_only','indexed_document_type':p['type'],
   'identifier_note':'Multiple arXiv IDs in indexed locations; no automatic identity collapse.' if len(aids)>1 else ''})

 def arxiv_record(p,evidence):
  return {'id':'as-arxiv-'+p['arxiv_id'],'title':p['title'],'title_variants':[p['title']],
   'identifiers':{'arxiv':p['arxiv_id']},'authors':p['authors'],'date':p['published'],
   'date_basis':'arXiv first submitted, UTC','links':{'paper':p['url']},'evidence':evidence,
   'source_work_ids':[],'metadata_sources':[p['url']],'reading_status':'metadata_only',
   'indexed_document_type':'preprint','identifier_note':''}

 for p in conc['records']:add(arxiv_record(p,['attention_concentration_keywords']))
 # The prior narrower queue is included in the broad collection, not discarded.
 for p in discovery_state():
  if p['current_status']=='awaiting_source_review' or p['current_status']=='context_only':
   add(arxiv_record(p,['prior_sink_keyword_discovery' if 'direct_sink' in p.get('retrieved_by',[]) else 'prior_related_discovery']))
 ref_map={r['arxiv_id']:r for r in refs['records']}
 note_map={r['arxiv_id']:r for r in reading['records']}
 context_map={r['arxiv_id']:r for r in load('data/reviews/source-review-2026-10-26.json')['excluded'] if r['decision']=='context_only' and r['basis']=='key_sections_of_full_text'}
 for item in records.values():
  aid=item['identifiers'].get('arxiv')
  if aid in ref_map:
   item['reference_check']=ref_map[aid]
   if ref_map[aid]['status']=='reference_verified':
    item['evidence'].append('citation_in_primary_reference_list')
    item['reading_status']='reference_list_checked'
  if aid in note_map:
   item['reading_note']=note_map[aid]
   item['reading_status']='key_sections_checked'
   src=json.loads((args.fulltext_cache/(aid+'.source.json')).read_text())
   assert src['url']==item['reading_note']['source_url']
   item['reading_note']['source_sha256']=src['sha256']
  if aid in context_map:
   item['context_reading_note']=context_map[aid]
   item['reading_status']='key_sections_checked_context'
 assert set(note_map)<=set(by_arxiv)
 kept_source_ids={x for p in records.values() for x in p['source_work_ids']}
 assert kept_source_ids=={p['id'] for p in oa['records']}, 'An indexed version was lost during reconciliation.'
 result={'as_of':'2026-10-26','seed':oa['seed'],
  'scope':'Broad research library: citation links, indexed full-text mentions of the seed, attention concentration/collapse/entropy, and the prior review queue. Evidence and reading depth are separate from original method categories.',
  'queries':oa['queries']+[{'name':'attention_concentration','query':conc['query'],'pages':conc['pages'],'returned':len(conc['records']),'pagination_complete':sum(p['returned'] for p in conc['pages'])==len(conc['records'])}],
  'summary':{'openalex_unique_records':len(oa['records']),'arxiv_concentration_records':len(conc['records']),
   'normalized_broad_records':len(records),'matched_core_records':sum(bool(p['core_catalog_id']) for p in records.values()),
   'additional_to_core':sum(not p['core_catalog_id'] for p in records.values()),
   'reference_lists_attempted':len(refs['records']),'reference_lists_verified':sum(p['status']=='reference_verified' for p in refs['records']),
   'additional_key_section_readings':len(reading['records'])},
  'self_survey_hits_excluded':self_hits,
  'limits':['A complete retrieved page set is not exhaustive coverage of the research field.',
   'OpenAlex citation edges and full-text title hits are separate signals. Indexed mentions are not represented as verified citations.',
   'Citation-only and keyword-only entries are included with unassigned method labels until the scientific content is read.',
   'Persistent sink behavior, low per-query entropy, and low-rank or smoothed attention are related but distinct measurements.',
   'Identifiers and exact normalized titles drive deduplication. Different-title publication versions can remain unresolved.',
   'OpenAlex dates and document types are inherited metadata, not independently verified publication claims.',
   'The 60 primary reference checks are a newest-arXiv convenience batch, not a representative sample.'],
  'records':sorted(records.values(),key=lambda p:(p['date'],p['id']),reverse=True)}
 save(ROOT/'data/library/broad-2026-10-26.json',result)
 print(json.dumps(result['summary'],indent=2))

if __name__=='__main__':main()
