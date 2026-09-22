from pathlib import Path
import json,sys,urllib.request,concurrent.futures
root=Path(__file__).resolve().parents[1]
def run(name):
 data=json.loads((root/'raw'/f'{name}_task.json').read_text())
 if data.get('status')!='SUCCEEDED':return name+' not ready'
 dest=root/'raw'/name;dest.mkdir(exist_ok=True)
 for fmt in ['glb','stl']:
  url=data.get('model_urls',{}).get(fmt)
  target=dest/f'model.{fmt}'
  if url and not target.exists():
   with urllib.request.urlopen(url,timeout=120) as response,target.with_suffix('.download').open('wb') as out:
    while chunk:=response.read(1024*1024):out.write(chunk)
   target.with_suffix('.download').rename(target)
  print(name,fmt,target.stat().st_size if target.exists() else 'missing',flush=True)
 return name+' done'
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for result in pool.map(run,sys.argv[1:]):print(result,flush=True)
