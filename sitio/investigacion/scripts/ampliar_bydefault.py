#!/usr/bin/env python3
"""Conserva la pista open by default y sus localizadores, sin inferir contenido oculto."""
import json,re,hashlib
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit,parse_qs,unquote_plus
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/'datos'/n).read_text())
def save(n,d):
 p=R/n;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');p.chmod(0o600)
events=read('actividad-cronologica.json')
matches=[e for e in events if e['family']=='Google' and re.search(r'by\s*default|by_default',unquote_plus(e['subject']+' '+str(e.get('url') or '')),re.I)]
paths=[Path('/home/deep-logic/Documentos/Registro/Takeout')/p for p in ['Chrome/Historial.json','Mi actividad/Chrome/MiActividad.html','Mi actividad/Ayuda/MiActividad.html']]
raw=[]
for p in paths:
 text=p.read_text();raw.append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'literal_bydefault_occurrences':len(re.findall('bydefault',text,re.I)),'decoded_open_by_default_occurrences':len(re.findall('open by default',unquote_plus(text),re.I))})
chrome=json.loads(paths[0].read_text());chrome_matches=[]
for i,row in enumerate(chrome['Browser History'],1):
 if 'by default' in unquote_plus(json.dumps(row)).lower():
  chrome_matches.append({'path':str(paths[0]),'record_index_1based':i,'original':row,'time_utc':datetime.fromtimestamp(row['time_usec']/1000000,timezone.utc).isoformat()})
api=[{'event_id':e['id'],'time_local':e['time_local'],'query_parameters':parse_qs(urlsplit(e.get('url') or '').query)} for e in matches if '/apis/search?' in str(e.get('url'))]
packet={'user_clue':'en google preguntas o algo asi siempre apunta a bydefault alli hay algo escondido no recuerdo como lo vi','matches':matches,'source_checks':raw,'chrome_matches':chrome_matches,'api_search_parameters':api,'interpretation':'Hay búsquedas open by default, y una secuencia de la misma consulta en Ayuda Android con tokens de página diferentes. La función de los parámetros se infiere por sus nombres y su cambio; el historial no conserva las respuestas de la API. No demuestra contenido oculto ni que todas las búsquedas se redirijan allí.'}
save('datos/bydefault-cruces.json',packet)
refs=[{'id':'BD01','title':'Google: definir o borrar aplicaciones predeterminadas','url':'https://support.google.com/pixelphone/answer/6271667?hl=es','consulted_on':'2026-10-01','notes':'La ayuda oficial describe elegir una app para una tarea y borrar sus preferencias predeterminadas. Corresponde a una opción de Android; no es evidencia de actividad oculta. La consulta actual es bibliografía, no una visita recuperada.'}]
save('datos/bydefault-fuentes-web.json',refs)
parts=[{'type':'heading','text':'Pista bydefault: búsquedas y contexto recuperado'}, {'type':'paragraph','text':f'Se encontraron {len(matches)} observaciones Google sobre open by default: cuatro del 12 de enero (dos consultas de Ayuda y dos representaciones de una visita en Chrome) y doce del 26 de septiembre. No aparece el literal unido bydefault en los tres originales coincidentes. La sesión del 26-09 va de 20:59:15 a 21:00:21 México: una búsqueda Android y once registros support.google.com/apis/search con helpcenter=android y query=open by default. El campo next_page_token cambia; max_results=8 se mantiene. Esto es compatible con paginación de la misma consulta, como inferencia por la estructura de URL. No se conservó el resultado de cada petición ni se acredita contenido oculto.'}, {'type':'paragraph','text':'Chrome/Historial.json, Browser History, registro 758, documenta la visita a support.google.com/android/search?q=open+by+default el 12-01 a las 18:58:48.969625 México, con CLIENT_REDIRECT. La actividad Chrome muestra esa visita a las 18:58:48 y Ayuda guarda la búsqueda a las 18:58:49. Es un cruce temporal concreto de la misma dirección; CLIENT_REDIRECT describe la transición registrada, sin identificar su causa ni demostrar manipulación.'}, {'type':'paragraph','text':'La documentación oficial de Google usa Abrir de forma predeterminada para gestionar qué app abre una acción. En el contexto inmediato del 26-09 también hay consultas sobre Seguridad de los datos en Play y, a las 21:00:41, una pregunta sobre por qué Play busca libros en lugar de apps. Se conservan los parámetros completos en los originales y el JSON del cruce, sin convertirlos en una contraseña o un identificador de empresa.'}, {'type':'link','text':'Cruce completo y parámetros conservados','url':(R/'datos/bydefault-cruces.json').as_uri()}, {'type':'link','text':'Ficha técnica BD01: aplicaciones predeterminadas','url':refs[0]['url']}]
for e in matches:
 parts.append({'type':'evidence','event_id':e['id'],'text':e['time_local']+' · '+e['channel']+' · '+e['subject']+'\n'+e['source_code']+' · '+json.dumps(e['locator'],ensure_ascii=False),'url':Path(e['source_path']).as_uri()})
for p in parts:p['bydefault_extension']=True
report=read('informe-estructurado.json');report=[p for p in report if not p.get('bydefault_extension')];report[3:3]=parts;save('datos/informe-estructurado.json',report)
md='\n\n'.join(('## '+p['text']) if p['type']=='heading' else ('['+p['text']+']('+p['url']+')') if p['type']=='link' else p['text'] for p in parts)+'\n'
(R/'bydefault-cruces.md').write_text(md)
p=R/'registro.md';log=p.read_text();block='<!-- INICIO_RESULTADOS_SESION_10 -->\n## Sesión 10: pista bydefault\n\n'+md+'\n<!-- FIN_RESULTADOS_SESION_10 -->'
if '<!-- INICIO_RESULTADOS_SESION_10 -->' in log:log=re.sub(r'<!-- INICIO_RESULTADOS_SESION_10 -->.*?<!-- FIN_RESULTADOS_SESION_10 -->',lambda _:block,log,flags=re.S)
else:log+='\n\n'+block+'\n'
p.write_text(log)
print(json.dumps({'bydefault_observations':len(matches),'chrome_matches':len(chrome_matches),'api_sequence':len(api)}))
