#!/usr/bin/env python3
"""Publica únicamente en el repositorio privado del login previamente verificado."""
from pathlib import Path
import subprocess,os,json,sys
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];ROOT=R.parent/'expediente-documental';BIN=R.parents[1]/'.tools/github/bin';GH=BIN/'gh'
env=dict(os.environ,PATH=str(BIN)+':'+os.environ.get('PATH',''),GH_CONFIG_DIR=str(BIN.parent/'config'))
def cmd(args,check=True):return subprocess.run(args,cwd=ROOT,env=env,check=check,capture_output=True,text=True)
login=cmd([str(GH),'api','user','--jq','.login']).stdout.strip();assert login=='spinky-afk',login
name=login+'/expediente-documental'
res=cmd([str(GH),'api','repos/'+name],check=False)
if res.returncode:
 if '404' not in res.stderr:raise RuntimeError(res.stderr[:500])
 res=cmd([str(GH),'api','user/repos','-X','POST','-f','name=expediente-documental','-F','private=true','-f','description=Archivo documental personal: originales íntegros, cronología y referencias locales.'])
repo=json.loads(res.stdout);assert repo['private'] is True and repo['owner']['login']==login
remote=cmd(['git','remote','get-url','origin'],check=False)
if remote.returncode:cmd(['git','remote','add','origin',repo['clone_url']])
else:assert remote.stdout.strip()==repo['clone_url'],remote.stdout
print(json.dumps({'repository':repo['html_url'],'visibility':'private','step':'Subiendo Git y objetos LFS completos'},ensure_ascii=False),flush=True)
subprocess.run(['git','push','-u','origin','main'],cwd=ROOT,env=env,check=True)
head=cmd(['git','rev-parse','HEAD']).stdout.strip()
ref=json.loads(cmd([str(GH),'api','repos/'+name+'/git/ref/heads/main']).stdout)
assert ref['object']['sha']==head
verified=json.loads(cmd([str(GH),'api','repos/'+name]).stdout);assert verified['private'] is True
p=ROOT/'estado-publicacion.json';state=json.loads(p.read_text());state.update(github_connected=True,verified_github_login=login,remote_repository=repo['html_url'],remote_visibility='private',uploaded_at_utc=datetime.now(timezone.utc).isoformat(),verified_uploaded_commit=head,site_publication='local_in_private_repository',pages_enabled=False,full_private_evidence_uploaded=True);p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n')
# Conservar el hecho de publicación en el registro, sin incluir credenciales.
p=R/'registro.md';s=p.read_text();s+='\n\nPublicación GitHub comprobada: '+repo['html_url']+' · privado · '+state['uploaded_at_utc']+' · commit '+head+'. Git y LFS terminaron correctamente; la referencia remota main coincide.\n';p.write_text(s)
for target in [ROOT/'sitio/registro.md',ROOT/'sitio/investigacion/registro.md',ROOT/'evidencia/investigacion/registro.md']:
 target.write_text(s);target.chmod(0o600)
# Actualizar la huella del registro modificado en la copia completa.
import hashlib
p=ROOT/'manifiesto-evidencia-completa.json';manifest=json.loads(p.read_text())
for row in manifest['files']:
 if row['repository_path']=='evidencia/investigacion/registro.md':row['bytes']=len(s.encode());row['sha256']=hashlib.sha256(s.encode()).hexdigest()
manifest['bytes']=sum(x['bytes'] for x in manifest['files']);p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
p=ROOT/'README.md';s=p.read_text();s+='\n\nRepositorio verificado: ['+name+']('+repo['html_url']+'). Visibilidad privada. La subida incluye evidencia íntegra y objetos LFS. El sitio se consulta localmente después de clonar; GitHub Pages permanece desactivado.\n';p.write_text(s)
cmd(['git','add','--all']);cmd(['git','commit','-m','Registra publicación privada y verificación del expediente completo'])
subprocess.run(['git','push','origin','main'],cwd=ROOT,env=env,check=True)
final_head=cmd(['git','rev-parse','HEAD']).stdout.strip();ref=json.loads(cmd([str(GH),'api','repos/'+name+'/git/ref/heads/main']).stdout);assert ref['object']['sha']==final_head
print(json.dumps({'repository':repo['html_url'],'visibility':'private','final_commit':final_head,'remote_commit_verified':True,'full_private_evidence_uploaded':True},ensure_ascii=False),flush=True)
