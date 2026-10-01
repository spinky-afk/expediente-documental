#!/usr/bin/env python3
import json
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=R/'datos/informe-estructurado.json'
d=json.loads(p.read_text());d=[x for x in d if not x.get('github_extension')]
parts=[{'type':'heading','text':'Archivo íntegro autorizado y conexión GitHub verificada'},{'type':'paragraph','text':'El usuario autorizó subir todos los originales investigados y todo research, incluidos los datos privados, a un repositorio privado de spinky-afk. GitHub CLI 2.102.0 y Git LFS 3.8.0 se instalaron con verificación SHA-256; OAuth quedó autorizado y API user verificó spinky-afk. evidencia/originales conserva los originales sin exclusiones y evidencia/investigacion todos los datos, claves y entregables. El estado remoto observado se registra en estado-publicacion.json; las credenciales de la herramienta están fuera del expediente.'}]+[{'type':'link','text':s['id']+' · '+s['title'],'url':s['url']} for s in json.loads((R/'datos/github-fuentes-web.json').read_text())['sources'][2:]]
for x in parts:x['github_extension']=True
d[3:3]=parts;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
