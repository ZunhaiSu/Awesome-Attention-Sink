"""Retrieve broad citation/attention-concentration leads without inventing method labels."""
import argparse
import hashlib
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from inventory_recent import query_arxiv

SEED='W4387294617'
TITLE='Efficient Streaming Language Models with Attention Sinks'

def save(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

def openalex(cache,name,filters,search=None):
 records=[]; pages=[]; page=1; total=None
 while total is None or len(records)<total:
  params={'filter':filters,'per_page':100,'page':page,
   'select':'id,title,doi,publication_date,authorships,primary_location,locations,referenced_works,type'}
  if search: params['search']=search
  url='https://api.openalex.org/works?'+urllib.parse.urlencode(params)
  req=urllib.request.Request(url,headers={'User-Agent':'AttentionSinkCatalog/1.2 (bibliographic source collection)'})
  with urllib.request.urlopen(req,timeout=40) as response: blob=response.read()
  data=json.loads(blob); count=data['meta']['count']
  if total is None: total=count
  if count!=total: raise RuntimeError('Changing result count; snapshot requires reconciliation.')
  found=data['results']
  if not found and len(records)<total: raise RuntimeError('Incomplete paging')
  save(cache/f'{name}-{page}.json',data)
  pages.append({'url':url,'sha256':hashlib.sha256(blob).hexdigest(),'page':page,'returned':len(found),'reported_total':total})
  records.extend(found)
  print(name,page,len(records),'/',total,flush=True)
  page+=1
  if len(records)<total: time.sleep(0.4)
 return records,{'name':name,'pages':pages,'reported_total':total,'returned':len(records),'pagination_complete':len(records)==total}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cache',type=Path,required=True);args=ap.parse_args()
 cache=args.cache;cache.mkdir(parents=True,exist_ok=True)
 queries=[]; merged={}
 for name,filt,search in [
  ('seed_citation_edges',f'cites:{SEED},to_publication_date:2026-10-26',None),
  ('seed_title_fulltext_mentions','to_publication_date:2026-10-26','"'+TITLE+'"')]:
  results,audit=openalex(cache,name,filt,search);queries.append(audit)
  for p in results:
   ident=p['id']
   if ident not in merged: merged[ident]={**p,'retrieved_by':[]}
   merged[ident]['retrieved_by'].append(name)
 save(cache/'openalex_metadata.json',{'seed':{'arxiv':'2309.17453','openalex':SEED,'title':TITLE},'queries':queries,'records':list(merged.values())})
 query='(ti:"attention concentration" OR abs:"attention concentration" OR ti:"attention collapse" OR abs:"attention collapse" OR ti:"entropy collapse" OR abs:"entropy collapse" OR ti:"attention saturation" OR abs:"attention saturation" OR ti:"attention entropy" OR abs:"attention entropy" OR ti:"attention hotspot" OR abs:"attention hotspot" OR ti:"attention hot spots" OR abs:"attention hot spots") AND (cat:cs.LG OR cat:cs.CL OR cat:cs.CV OR cat:cs.AI OR cat:stat.ML) AND submittedDate:[202601010000 TO 202610262359]'
 found,pages=query_arxiv(query,cache,'attention_concentration')
 save(cache/'concentration_metadata.json',{'as_of':'2026-10-26','query':query,'pages':pages,'records':found})
 print('attention_concentration',len(found),flush=True)

if __name__=='__main__':main()
