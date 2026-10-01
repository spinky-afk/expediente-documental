#!/usr/bin/env python3
"""Hallazgos con referencias y un visor de cronología completamente local."""
import hashlib
import html
import json
import os
import re
from pathlib import Path
from datetime import datetime, timezone

OUT=Path(__file__).resolve().parents[1]
FB=Path('/home/deep-logic/Documentos/facebook')
GOOGLE=Path('/home/deep-logic/Documentos/Registro/Takeout')
def read(name):return json.loads((OUT/name).read_text())
def write(name,text):
    p=OUT/name;p.write_text(text,encoding='utf-8');os.chmod(p,0o600)
def json_write(name,obj):write(name,json.dumps(obj,ensure_ascii=False,indent=2)+'\n')

events=read('datos/actividad-cronologica.json');summary=read('datos/actividad-resumen.json')
sources=read('datos/catalogo-fuentes.json');byid={r['id']:r for r in events};bysource={r['path']:r for r in sources}
businesses=read('datos/facebook-empresas-identificadores.json');assets=read('datos/facebook-files-inventario.json')
shared=read('datos/facebook-identificadores-compartidos.json');relations=read('datos/actividad-correlaciones.json')
web=[
 {'id':'F01','title':'Meta: historial cifrado y almacenamiento seguro de Messenger',
  'url':'https://about.fb.com/news/2024/03/end-to-end-encryption-on-messenger-explained/',
  'status':'contenido verificado','relationship':'Referencia consultada ahora; no es una visita recuperada del historial.',
  'notes':'El almacenamiento seguro permite recuperar conversaciones cifradas en otros dispositivos mediante un PIN de seis dígitos o una clave guardada en Google Drive o iCloud.'},
 {'id':'F02','title':'Google: configuración avanzada e ID del Perfil de Negocio',
  'url':'https://support.google.com/business/answer/10737668?hl=es-419','status':'contenido verificado',
  'relationship':'Referencia consultada ahora; no es una visita recuperada del historial.',
  'notes':'El ID identifica una ficha de negocio en Google. Se consulta en Más, Configuración del Perfil de Negocio, Configuración avanzada.'},
 {'id':'F03','title':'Google: encontrar una empresa en Búsqueda y Maps',
  'url':'https://support.google.com/business/answer/145585?hl=es-419','status':'contenido verificado',
  'relationship':'Referencia consultada ahora; no es una visita recuperada del historial.',
  'notes':'Con la cuenta asociada se puede encontrar el perfil buscando el nombre y ciudad o mi negocio; también mediante Maps.'},
 {'id':'F04','title':'Messenger: ayuda sobre descarga del historial cifrado',
  'url':'https://www.facebook.com/help/messenger-app/677912386869109',
  'status':'acceso bloqueado o redirigido a inicio de sesión; contenido no verificado',
  'relationship':'Intento de consulta actual, no utilizado para afirmar instrucciones de descarga.',
  'notes':'No se inventa una secuencia de menús a partir de esta página inaccesible.'},
]
for s in web:s['consulted_on']='2026-10-01'
json_write('datos/facebook-google-fuentes-web.json',web)

def ref(r):
    loc=r['locator'];idx=next((f'{k}={v}' for k,v in loc.items() if 'index' in k or 'pointer' in k),'')
    pos=f"; línea {loc['html_line_1based']}, columna {loc['html_column_0based']}" if 'html_line_1based' in loc else ''
    return f"{r['source_code']} · {idx}{pos}"

parts=[]
def h(t):parts.append({'type':'heading','text':t})
def p(t):parts.append({'type':'paragraph','text':t})
def link(t,url):parts.append({'type':'link','text':t,'url':url})
def evidence(r):
    parts.append({'type':'evidence','event_id':r['id'],'text':f"{r['time_local']} · {r['channel']} · {r['subject']}\n{ref(r)}",'url':r.get('url')})

h('Hallazgos: Facebook, Google y números de identificación')
p('Actualizado el 1 de octubre de 2026. La solicitud actual autoriza crear y actualizar el PDF desde ahora. Las indicaciones anteriores de esperar al final se conservan como historial de la investigación.')
p(f"La cronología integra {summary['dated_observations']:,} observaciones fechadas de {summary['source_files']} archivos consultados, de {summary['earliest'][:10]} a {summary['latest'][:10]}. Google y Facebook se ordenan conjuntamente por instante UTC y se muestran en America/Mexico_City. Hay {summary['undated_observations']} secciones sin fecha, conservadas por separado.")
h('Qué significan los números')
p('Se encontró una relación explícita entre una página y su conversación: Epazote Tulancingo. El catálogo contiene 87 entidades de actividad fuera de Meta. Ninguno de sus identificadores de empresa o de evento aparece en el texto ni en los enlaces de las conversaciones exportadas. Este resultado no cubre reconocimiento automático del texto de todas las fotos o videos ni mensajes ausentes de la exportación.')
p('Los campos con nombre Identificador se conservan con su contexto: uno identifica la entidad en el encabezado del archivo y otro aparece dentro del bloque de eventos. No se ha demostrado que este último identifique de manera única un evento: se repite entre fechas y entre entidades. Tampoco se ha demostrado que el Identificador de entidad sea un Meta Business Manager ID.')
page=summary['page_ids'][0];chat_source=page['source_path']
p(f"Epazote Tulancingo: page_id={page['page_id']}. Aparece en el parámetro extra_params de un enlace interno de Messenger del 28-08-2026 a las 17:29:03, en el mensaje de sistema 'Empezaste a seguir'. No prueba que alguien escribiera o enviara ese número manualmente. Referencia: {page['source_code']}, mensaje #14, línea 13, columna 5030.")
link('Conversación original de Epazote Tulancingo',Path(chat_source).as_uri())
p('La carpeta epazotetulancingo_1514670583749704 tiene otro número: 1514670583749704. Se conserva como sufijo de carpeta/conversación, sin equipararlo al page_id. Ninguno de los dos coincide con los identificadores de las 87 entidades revisadas.')
p('Ejemplo ChatGPT: Identificador de entidad 6558176734212414; Identificador dentro de eventos 562278416645613; sufijo de archivo 105529809654844465. Son tres campos distintos. El sufijo de archivo se repite en otros archivos y no se usa para identificar una empresa.')
h('Relaciones entre entidades de actividad fuera de Meta')
p('Hay ocho valores del campo Identificador de evento compartidos por más de una entidad. Esto es una coincidencia literal documentada, no una prueba de que los nombres correspondan a una misma empresa o de que hayan intercambiado mensajes contigo.')
for r in shared:
    names='; '.join(f"{b['name']} [entidad {b['business_id']}]" for b in r['businesses'])
    p(f"Evento {r['event_identificador']} → {names}.")
h('Epazote: Messenger, una captura de WhatsApp y Google Maps')
for ident in sorted(summary['epazote_event_ids'],key=lambda id:byid[id]['time_utc']):evidence(byid[ident])
photo=FB/'your_facebook_activity/messages/inbox/epazotetulancingo_1514670583749704/photos/1395635869197307.jpg'
photo_event=next(r for r in events if any('1395635869197307.jpg' in u for u in r.get('attachment_links',[])))
p(f"Se inspeccionó visualmente la foto adjunta enviada el 27-08-2026 a las 21:50:38 ({photo_event['id']}; {ref(photo_event)}). Es una captura de una conversación de WhatsApp con 'Epazote / Restaurante Epazote', que incluye un comprobante por $650.00, concepto 'paquete', referencia 7116298, beneficiario visible Rafael Santos y cuentas bancarias parcialmente ocultas. La referencia 7116298 es bancaria, no un identificador de empresa de Facebook o de Google. No se atribuye al beneficiario la propiedad legal del restaurante. La captura no proporciona un historial completo de WhatsApp ni un enlace a su cuenta.")
link('Foto original: captura y comprobante',photo.as_uri())
p('El texto de Messenger menciona el horario de Google Maps, pero no incluye un enlace a la ficha ni su ID. No se encontró una consulta de Epazote en los registros de Google que permita confirmar la misma visita. La relación con Maps proviene del texto de los mensajes. El botón Confirmar pago es una pista de verificación de comprobante con imagen; no demuestra que sea la búsqueda sobre validar más rápido que se recuerda.')
json_write('datos/facebook-foto-epazote-inspeccion.json',{
 'path':str(photo),'sha256':hashlib.sha256(photo.read_bytes()).hexdigest(),'inspection':'visual; 2026-10-01',
 'message_event_id':photo_event['id'],'source_path':photo_event['source_path'],'locator':photo_event['locator'],
 'amount_visible':'650.00','concept_visible':'paquete','payment_reference_visible':'7116298',
 'beneficiary_visible':'Rafael Santos','bank_accounts':'parcialmente ocultas en la imagen',
 'interpretation':'Captura de WhatsApp adjunta en Messenger. Referencia bancaria; no ID de empresa. No establece propiedad del negocio.'})
h('Coppel: una relación comprobable entre Facebook y Google Play')
p('El 03-08-2026 a las 21:31:46 se registró un clic de anuncio cuyo título/destino indica com.coppel.coppelapp. El ID de biblioteca de anuncios es 2475207562964622. La misma cadena de paquete aparece en Google Play, Analytics y Publicidad. Es una relación por paquete de aplicación, sin afirmar que el anuncio causó los usos posteriores.')
for ident in summary['coppel_event_ids']:evidence(byid[ident])
link('Aplicación Coppel en Google Play','https://play.google.com/store/apps/details?id=com.coppel.coppelapp')
link('Referencia de anuncio de Coppel','https://www.facebook.com/ads/library/?id=2475207562964622')
p('En actividad fuera de Meta también figuran Coppel (entidad 10153514100232571) y coppel.com (entidad 1444276872316871), con cuatro valores de Identificador de evento compartidos. Este cruce se documenta por separado del ID de anuncio y del paquete Android; no existe una conversión demostrada entre esos números.')
h('Qué es la carpeta files')
p('Contiene 181 archivos: 179 PNG sin extensión, un logo de Facebook llamado fb_logo.png y una imagen pequeña llamada profile_pic.jpg. Las 179 imágenes numeradas están enlazadas desde your_facebook_activity/ai/your_files.html, en la lista de archivos creados. Las 179 contienen metadatos Software de Matplotlib. La imagen 1079358437649748 se inspeccionó: es una representación de x=1. Su número identifica un archivo en el export, sin relación demostrada con las empresas.')
link('Listado original de archivos de IA',(FB/'your_facebook_activity/ai/your_files.html').as_uri())
p('Se registraron las fechas de creación que da la lista de IA. El logo y la foto se inspeccionaron y se conservan sin inventarles una fecha. El inventario incluye formato por firma binaria, tamaño, SHA-256 y referencia de origen de cada imagen numerada.')
h('Dos vías para consultar mensajes; límites de esta copia')
p('La copia local contiene 37 archivos de conversación y 1.755 mensajes fechados. Hay otros 38 bloques sin fecha: por ejemplo, foto del grupo y configuración del enlace de invitación. Se conservan fuera de la línea temporal para no asignarles horas inventadas.')
link('Índice local de tus mensajes',(FB/'your_facebook_activity/messages/your_messages.html').as_uri())
p('El archivo Conversaciones secretas indica Sí tanto para mensajes enviados como recibidos, y lista dispositivos. Es información de uso, no el contenido descifrado de todas esas conversaciones. Este export no permite concluir que estén todos tus mensajes.')
link('Metadatos locales de conversaciones secretas',(FB/'your_facebook_activity/messages/secret_conversations.html').as_uri())
p('Otra vía documentada por Meta es recuperar el historial cifrado mediante el almacenamiento seguro de Messenger, con PIN de seis dígitos o una clave conservada en Google Drive o iCloud. Esta es una explicación externa del mecanismo; no se recuperó un PIN o una clave de respaldo de Messenger en esta revisión. [F01]')
link(web[0]['title'],web[0]['url'])
p('La página de ayuda sobre descarga del historial cifrado no permitió verificar sus instrucciones. Se registró el intento fallido, sin presentar pasos no comprobados. [F04]')
h('Google: ver y administrar una empresa')
p('El 26-09-2026, después de las búsquedas VAPID, aparece la consulta perfil negocios google a las 22:29:46 y visitas a business.google.com, incluida la pantalla de creación y un registro de Perfil de Empresa en Google. Son visitas documentadas; no prueban que se haya creado o administrado una ficha.')
for ident in summary['google_business_event_ids']:evidence(byid[ident])
accountpath=GOOGLE/'Perfil\xa0de\xa0Negocio\xa0de\xa0Google/account-118064871121168977834/data.json'
account=json.loads(accountpath.read_text());accountsource=bysource[str(accountpath)]
p(f"La exportación específica del producto contiene name={account['name']}, accountName={account['accountName']} y type={account['type']}. Referencia {accountsource['code']}: data.json, /name, /accountName y /type. El número 118064871121168977834 identifica este recurso de cuenta, no una ficha individual. businessPersonalization.json está vacío. En esta carpeta no hay locations ni un ID de ficha de negocio.")
link('Cuenta exportada de Perfil de Negocio',accountpath.as_uri())
p('La documentación de Google permite encontrar la empresa en Búsqueda o Maps con la cuenta asociada. Para consultar el ID de una ficha: abrir el Perfil de Negocio → Más → Configuración del Perfil de Negocio → Configuración avanzada. Ese ID pertenece a Google; no se ha encontrado una equivalencia con los números de Facebook. [F02, F03]')
for s in web[1:3]:link(s['title'],s['url'])
p('Los 16 registros de Chat y 290 de Gmail dentro de Mi actividad son actividad del producto; esa carpeta no equivale al contenido de conversaciones o correos. Por separado se incorporaron tres conversaciones exportadas de Gemini en Workspace con preguntas, respuestas, fechas y enlaces de sus citas.')
h('VAPID y la pista de validación con imagen: hallazgos anteriores')
p('Se mantienen las búsquedas vapid y vapid web push del 26-09-2026 a las 22:28:27 y 22:28:32 y los dos artículos visitados después. Ocho observaciones de Search, Chrome y Browser History corresponden a cuatro eventos en el cruce original, conservado en datos/cruce.json.')
link('Artículo visitado: VAPID en Medium','https://medium.com/bawilabs/web-push-notifications-through-vapid-method-7d4d6927a006')
link('Artículo visitado: protocolo Web Push','https://web.dev/articles/push-notifications-web-push-protocol?hl=es-419')
p('Se recuperó una clave privada VAPID de sharing.vapid_key en Configuración.json. Se validó como EC P-256 y pertenece al componente sharing de Chrome; no se demostró que sea la clave de un servidor Web Push propio. Su valor permanece en privado/claves-recuperadas.md, privado/vapid-recuperada.json y privado/vapid-private.pem. No se encontraron contraseñas de acceso en los exportes revisados. El PDF presenta metadatos y referencias de la clave, sin copiar el valor privado.')
p('La búsqueda aproximada sobre validar con una imagen más rápido sigue sin una consulta explícita coincidente. Se conservan candidatos de identidad, mensajes de Google y Lens, y ahora la captura de comprobante de Epazote como pista relacionada. Ninguno confirma todavía el método que se recuerda.')
h('Cómo se construye y se actualiza la cronología')
p('Se conservan todas las observaciones extraídas: una visita puede aparecer en varios productos. No se eliminan registros por parecer duplicados. La igualdad de URL en fuentes Google distintas a hasta dos segundos se marca como posible misma visita. Los resúmenes y detalles de actividad fuera de Meta se relacionan por nombre, campo de identificador, tipo y minuto, sin sustituir sus tiempos originales.')
p(f"Hay {len(relations)} relaciones automáticas propuestas en datos/actividad-correlaciones.json. Cada observación tiene ID de esta versión, fecha original, precisión, fuente y localizador de registro. El catálogo permite volver al HTML/JSON/CSV original y comprobar SHA-256. Los originales fueron verificados sin modificaciones.")
p('Las horas de Facebook llevan UTC-06:00 según su encabezado. Se convierten a America/Mexico_City; para 2022 la hora local puede cambiar por el horario de verano histórico. Los registros con precisión de minuto conservan esa precisión aunque la representación ISO muestre segundos 00. Dos transacciones CSV de Google Pay no explicitan zona: se asume México y se marca la incertidumbre. No se deduce cuándo ocurrió un clic a partir de una actualización musical. Fechas de instalación, actualización, alta de dispositivo o vencimiento se etiquetan como tales, no como búsquedas ni usos de apps.')
p('Alcance: los 27 HTML de Mi actividad y el historial JSON de Chrome; fechas explícitas de JSON de otros productos y CSV con fecha reconocible; conversaciones y secciones fechadas de los 386 HTML de Facebook; detalle y resumen de actividad fuera de Meta y archivos IA. Este PDF es una reconstrucción de las copias disponibles, no una garantía de que contengan todo lo sucedido en las cuentas. No se han integrado citas de calendario como navegación ni tratado preferencias sin fecha como acciones.')
p('Los enlaces de acceso se depuran de parámetros privados en el PDF y visor; las URLs originales permanecen en privado/actividad-observaciones-originales.json. Las búsquedas y mensajes se muestran con su texto. El visor HTML funciona sin conexión y permite filtrar fecha, servicio, texto e identificador, alternar orden y abrir los archivos originales. El CSV incluye toda la cronología para consulta externa. El PDF conserva el orden global de más antiguo a más reciente.')
json_write('datos/informe-estructurado.json',parts)
md=[]
for r in parts:
    if r['type']=='heading':md.append('## '+r['text'])
    elif r['type']=='link':md.append(f"[{r['text']}]({r['url']})")
    else:
        md.append(('**'+r['event_id']+'** · ' if r['type']=='evidence' else '')+r['text'])
        if r.get('url'):md.append(f"[Abrir fuente web]({r['url']})")
report='\n\n'.join(md)+'\n'
write('hallazgos-facebook.md',report)
logpath=OUT/'registro.md';log=logpath.read_text()
block='<!-- INICIO_RESULTADOS_SESION_3 -->\n## Sesión 3: Facebook y PDF cronológico actualizado\n\n'+report+'\n<!-- FIN_RESULTADOS_SESION_3 -->'
if '<!-- INICIO_RESULTADOS_SESION_3 -->' in log:
    log=re.sub(r'<!-- INICIO_RESULTADOS_SESION_3 -->.*?<!-- FIN_RESULTADOS_SESION_3 -->',lambda _:block,log,flags=re.S)
else:log+='\n\n'+block+'\n'
write('registro.md',log)

# Visor sin dependencias ni conexiones. Todo contenido del export se inserta como texto.
payload=json.dumps({'events':events,'summary':summary,'sources':sources,'relations':relations,'businesses':businesses},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
template='''<!doctype html><html lang="es"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Historial cruzado · Google y Facebook</title>
<style>body{font:16px system-ui;margin:0;color:#172a39;background:#f5f7fa}header{background:#13364a;color:white;padding:28px max(20px,calc((100% - 1150px)/2))}h1{font-size:28px;margin:0 0 8px}main{max-width:1150px;margin:auto;padding:20px}a{color:#116592;overflow-wrap:anywhere}header a{color:#bde8ff}label{display:flex;flex-direction:column;gap:5px;font-size:13px}input,select,button{font:inherit;border:1px solid #cad3da;border-radius:6px;padding:10px;background:white}button{cursor:pointer}.filters{display:grid;grid-template-columns:2fr 1fr 1fr 1fr 1fr;gap:12px}.toolbar{display:flex;flex-wrap:wrap;align-items:center;gap:12px;margin:15px 0}.card{padding:16px 20px;background:white;border:1px solid #dce3e8;border-left:4px solid #39808b;border-radius:7px;margin:10px 0}.facebook{border-left-color:#6566aa}.stamp,.meta{font-size:13px;color:#526575}.subject{white-space:pre-wrap;overflow-wrap:anywhere;margin:10px 0}.pill{background:#eaf0f4;border-radius:20px;padding:3px 10px;font-size:12px}details{margin-top:10px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}table{border-collapse:collapse;width:100%;background:white}td,th{padding:9px;text-align:left;border-bottom:1px solid #dce3e8;font-size:13px;overflow-wrap:anywhere}.note{font-size:14px;color:#526575}@media(max-width:800px){.filters{grid-template-columns:1fr 1fr}.filters label:first-child{grid-column:1/-1}}</style>
<header><h1>Tu historial cruzado</h1><div id="scope"></div><p>Google · Chrome · Play · Messenger · actividad fuera de Meta</p><a href="historial-cruzado.pdf">PDF actualizado</a> · <a href="hallazgos-facebook.md">Hallazgos</a> · <a href="registro.md">Registro de investigación</a> · <a href="actividad-cronologica.csv">CSV completo</a></header>
<main><p class="note">Todo se consulta en este archivo local. Fechas mostradas en America/Mexico_City. Se conservan observaciones repetidas y referencias originales. Los IDs E son de esta versión. Las coincidencias automáticas proponen relaciones, sin probar causalidad.</p>
<div class="filters"><label>Buscar texto, URL, empresa, ID o referencia<input id="term" type="search" placeholder="vapid, Epazote, 107881590544962…"></label><label>Desde<input id="from" type="date"></label><label>Hasta<input id="to" type="date"></label><label>Servicio<select id="channel"><option value="">Todos</option></select></label><label>Orden<select id="order"><option value="asc">Más antiguo primero</option><option value="desc">Más reciente primero</option></select></label></div>
<div class="toolbar"><button id="vapid">VAPID</button><button id="epazote">Epazote</button><button id="coppel">Coppel</button><button id="profile">Empresa de Google</button><button id="reset">Limpiar filtros</button><span id="count"></span></div>
<details><summary>Catálogo de las 87 entidades y sus identificadores</summary><p class="note">Identificador de entidad y de eventos son campos distintos. No hubo coincidencias con esos IDs en el texto/enlaces de conversaciones. Haz clic en un número para buscarlo.</p><table><thead><tr><th>Entidad</th><th>ID en encabezado</th><th>IDs en eventos</th><th>Fuente</th></tr></thead><tbody id="businesses"></tbody></table></details>
<div class="toolbar"><button class="prev">Anterior</button><span class="page"></span><button class="next">Siguiente</button></div><div id="results"></div><div class="toolbar"><button class="prev">Anterior</button><span class="page"></span><button class="next">Siguiente</button></div><noscript>Activa JavaScript para filtrar el historial; también puedes consultar el PDF y CSV.</noscript></main>
<script id="dataset" type="application/json">__DATA__</script><script>
const D=JSON.parse(document.getElementById('dataset').textContent),$=id=>document.getElementById(id),size=100;let page=0,filtered=[];
const fold=s=>String(s||'').normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase();
const related=new Map();D.relations.forEach(r=>r.event_ids.forEach(id=>{if(!related.has(id))related.set(id,new Set());r.event_ids.filter(x=>x!==id).forEach(x=>related.get(id).add(x));}));
const indexed=D.events.map(r=>({r,text:fold([r.id,r.subject,r.url,r.channel,r.source_code,r.source_path,JSON.stringify(r.identifiers)].join(' '))}));
$('scope').textContent=D.summary.dated_observations.toLocaleString('es-MX')+' registros · '+D.summary.earliest.slice(0,10)+' → '+D.summary.latest.slice(0,10)+' · actualizado '+D.summary.generated_at_utc;
const channels=[...new Set(D.events.map(r=>r.family+' / '+r.channel))].sort();for(const c of channels){const o=document.createElement('option');o.value=c;o.textContent=c;$('channel').append(o);}
function a(label,url){const e=document.createElement('a');e.textContent=label;e.href=url;return e;}
function fileUrl(path){return 'file://'+path.split('/').map(encodeURIComponent).join('/');}
function el(tag,text,cls){const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;}
function query(t){$('term').value=t;apply();window.scrollTo({top:0,behavior:'smooth'});}
for(const b of D.businesses){const tr=el('tr');tr.append(el('td',b.name));const id=el('td'),btn=el('button',b.business_id);btn.onclick=()=>query(b.business_id);id.append(btn);tr.append(id);const nums=el('td');for(const x of b.event_identifiers){const q=el('button',x);q.onclick=()=>query(x);nums.append(q,document.createTextNode(' '));}tr.append(nums);const src=el('td');src.append(a(b.source_code,fileUrl(b.source_path)));tr.append(src);$('businesses').append(tr);}
function apply(){const term=fold($('term').value.trim()),from=$('from').value,to=$('to').value,channel=$('channel').value;filtered=indexed.filter(x=>(!term||x.text.includes(term))&&(!from||x.r.time_local.slice(0,10)>=from)&&(!to||x.r.time_local.slice(0,10)<=to)&&(!channel||x.r.family+' / '+x.r.channel===channel)).map(x=>x.r);if($('order').value==='desc')filtered.reverse();page=0;render();}
function render(){const host=$('results');host.replaceChildren();$('count').textContent=filtered.length.toLocaleString('es-MX')+' coincidencias';const pages=Math.max(1,Math.ceil(filtered.length/size));document.querySelectorAll('.page').forEach(e=>e.textContent='Página '+(page+1)+' de '+pages);document.querySelectorAll('.prev').forEach(e=>e.disabled=page===0);document.querySelectorAll('.next').forEach(e=>e.disabled=page+1>=pages);
for(const r of filtered.slice(page*size,(page+1)*size)){const c=el('article',undefined,'card '+(r.family==='Facebook'?'facebook':''));c.id=r.id;c.append(el('div',r.time_local.replace('T',' · ')+' · '+r.id,'stamp'),el('span',r.family+' / '+r.channel,'pill'),el('div',r.subject,'subject'),el('div',r.kind+' · precisión: '+r.time_precision,'meta'));if(r.url)c.append(a('Abrir enlace web',r.url));const det=el('details');det.append(el('summary','Referencia y datos de origen'));const path=el('p');path.append(a(r.source_code+' · '+r.source_path,fileUrl(r.source_path)));det.append(path,el('pre',JSON.stringify({localizador:r.locator,fecha_original:r.date_original,hora_utc:r.time_utc,identificadores:r.identifiers,zona:r.timezone_basis||'según fuente'},null,2)));if(r.footer_date_original)det.append(el('p','Pie original ambiguo: '+r.footer_date_original+'; se usó Fecha de actualización.'));for(const u of r.attachment_links||[]){if(!u)continue;const url=u.startsWith('http')?u:fileUrl('/home/deep-logic/Documentos/facebook/'+u);const p=el('p');p.append(a('Adjunto / enlace: '+u,url));det.append(p);}if(related.has(r.id)){const p=el('p','Observaciones relacionadas: ');for(const id of related.get(r.id)){const b=el('button',id);b.onclick=()=>query(id);p.append(b,document.createTextNode(' '));}det.append(p);}c.append(det);host.append(c);}if(!filtered.length)host.append(el('p','No hay registros con estos filtros.'));
}
for(const id of ['from','to','channel','order'])$(id).onchange=apply;let timer;$('term').oninput=()=>{clearTimeout(timer);timer=setTimeout(apply,180)};
for(const [id,term] of [['vapid','vapid'],['epazote','Epazote'],['coppel','Coppel'],['profile','business.google']])$(id).onclick=()=>query(term);
$('reset').onclick=()=>{for(const id of ['term','from','to','channel'])$(id).value='';$('order').value='asc';apply();};document.querySelectorAll('.prev').forEach(e=>e.onclick=()=>{if(page>0){page--;render();}});document.querySelectorAll('.next').forEach(e=>e.onclick=()=>{if((page+1)*size<filtered.length){page++;render();}});apply();
</script></html>'''
write('historial-cruzado.html',template.replace('__DATA__',payload))
print(json.dumps({'report_sections':len(parts),'timeline_events':len(events),'html_bytes':(OUT/'historial-cruzado.html').stat().st_size}))
