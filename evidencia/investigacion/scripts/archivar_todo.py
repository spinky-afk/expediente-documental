#!/usr/bin/env python3
"""Copia íntegramente originales investigados y research al repositorio privado."""
from pathlib import Path
import hashlib,json,shutil
from datetime import datetime,timezone
R=Path(__file__).resolve().parents[1];ROOT=R.parent/'expediente-documental';DEST=ROOT/'evidencia'
ORIGINS={'google':Path('/home/deep-logic/Documentos/Registro/Takeout'),'facebook':Path('/home/deep-logic/Documentos/facebook'),'uber':Path('/home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data'),'mail':Path('/home/deep-logic/Documentos/Todo el correo, con Spam y Papelera incluidos.mbox')}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
manifest=[]
def copy(p,target,kind):
 target.parent.mkdir(parents=True,exist_ok=True);target.parent.chmod(0o700);shutil.copy2(p,target);target.chmod(0o600)
 a=sha(p);assert sha(target)==a
 manifest.append({'source_path':str(p),'repository_path':str(target.relative_to(ROOT)),'kind':kind,'bytes':p.stat().st_size,'sha256':a})
for key,root in ORIGINS.items():
 for p in ([root] if root.is_file() else sorted(root.rglob('*'))):
  if p.is_file():copy(p,DEST/'originales'/key/(p.name if root.is_file() else p.relative_to(root)),'original')
for p in sorted(R.rglob('*')):
 if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc':copy(p,DEST/'investigacion'/p.relative_to(R),'research')
expected=sum(1 for r in manifest if r['kind']=='original');assert expected==858,expected
private=['vapid-recuperada.json','claves-recuperadas.md','vapid-private.pem','clave-respaldo-github-local.txt']
assert all((DEST/'investigacion/privado'/n).exists() for n in private)
assert (DEST/'originales/google/Chrome/Configuración.json').exists()
report={'created_at_utc':datetime.now(timezone.utc).isoformat(),'visibility_required':'private','private_data_exclusions':[],'original_files':expected,'research_files':len(manifest)-expected,'bytes':sum(r['bytes'] for r in manifest),'files':manifest,'authorization':'El propietario pidió subir todo, incluidos los datos privados necesarios como pruebas. Se copian íntegros los originales investigados y todos los archivos de research. Las credenciales OAuth de la herramienta GitHub son configuración externa, no documentación investigada.'}
p=ROOT/'manifiesto-evidencia-completa.json';p.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');p.chmod(0o600)
print(json.dumps({k:v for k,v in report.items() if k!='files'},ensure_ascii=False),flush=True)
