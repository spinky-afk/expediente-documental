#!/usr/bin/env python3
from pathlib import Path
import subprocess,os,json
R=Path(__file__).resolve().parents[1];ROOT=R.parent/'expediente-documental';BINS=R.parents[1]/'.tools/github/bin'
env=dict(os.environ,PATH=str(BINS)+':'+os.environ.get('PATH',''),GH_CONFIG_DIR=str(BINS.parent/'config'))
def git(*args):return subprocess.run(['git',*args],cwd=ROOT,env=env,check=True,capture_output=True,text=True).stdout.strip()
manifest=json.loads((ROOT/'manifiesto-evidencia-completa.json').read_text());assert manifest['original_files']==858 and not manifest['private_data_exclusions']
git('config','--local','user.name','Archivo documental');git('config','--local','user.email','archivo@localhost')
git('config','--local','credential.https://github.com.helper','!'+str(BINS/'gh')+' auth git-credential')
large=[]
for p in sorted(ROOT.rglob('*')):
 if p.is_file() and '.git' not in p.parts and p.stat().st_size>50*1024*1024:
  rel=str(p.relative_to(ROOT));git('lfs','track','--filename',rel);large.append({'path':rel,'bytes':p.stat().st_size})
p=ROOT/'git-lfs-archivos-grandes.json';p.write_text(json.dumps({'files':large,'threshold_bytes':50*1024*1024},ensure_ascii=False,indent=2)+'\n')
git('add','--all')
# Verificar que ningún archivo en el índice supere 100 MiB como blob normal.
blobs=subprocess.run(['git','ls-files','-s'],cwd=ROOT,env=env,check=True,capture_output=True,text=True).stdout
ids=sorted({line.split()[1] for line in blobs.splitlines()});sizes=subprocess.run(['git','cat-file','--batch-check=%(objectname) %(objectsize)'],cwd=ROOT,env=env,input='\n'.join(ids)+'\n',check=True,capture_output=True,text=True).stdout
assert all(int(line.split()[1])<=100*1024*1024 for line in sizes.splitlines()),'Un blob supera 100 MiB'
subprocess.run(['git','commit','-m','Conserva expediente íntegro, correo y datos privados autorizados con Git LFS'],cwd=ROOT,env=env,check=True,stdout=subprocess.DEVNULL)
print(json.dumps({'commit':git('rev-parse','HEAD'),'tracked_files':len(blobs.splitlines()),'large_files_with_lfs':len(large),'originals':858,'private_data_exclusions':[]}),flush=True)
