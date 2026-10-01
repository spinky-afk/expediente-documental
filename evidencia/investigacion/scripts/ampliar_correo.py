#!/usr/bin/env python3
"""Cruza MBOX con usos de apps, visitas y registros de Uber."""
import bisect
import collections
import csv
import json
import re
from datetime import datetime,timezone
from pathlib import Path
from mail_util import MBOX,extract

OUT=Path(__file__).resolve().parents[1]
def read(n):return json.loads((OUT/'datos'/n).read_text())
def save(n,d):
    p=OUT/n;p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');p.chmod(0o600)
data=extract();messages=data['messages'];mail_by_index={m['mbox_index']:m for m in messages}
events=read('actividad-cronologica.json');byid={e['id']:e for e in events};mail_events={e['identifiers']['mail_id']:e for e in events if e['family']=='Correo'}
uses=[e for e in events if e['family']=='Google' and e['kind']=='uso de app' and e['channel'] in ['Google Play Store','Google Analytics']]
window_uses=[e for e in uses if '2026-09-20T18:00:00'<=e['time_local'][:19]<'2026-09-22T00:00:00']
window_mail=[e for e in mail_events.values() if '2026-09-20T18:00:00'<=e['time_local'][:19]<'2026-09-22T00:00:00']
def seconds(e):return datetime.fromisoformat(e['time_utc']).timestamp()
use_times=[seconds(e) for e in uses]
near=[]
for email_event in window_mail:
    stamp=seconds(email_event);start=bisect.bisect_left(use_times,stamp-300);end=bisect.bisect_right(use_times,stamp+300)
    nearby=uses[start:end]
    near.append({'mail_event':email_event['id'],'mail_id':email_event['identifiers']['mail_id'],'mail_subject':email_event['subject'],'time_local':email_event['time_local'],'window_seconds':300,'app_usage_event_ids':[e['id'] for e in nearby],'app_usage_observations':len(nearby),'meaning':'Contexto temporal ±5 minutos, sin demostrar que un correo provocó un uso ni que todas las apps pasaron a primer plano.'})
clusters=[]
for instant,rows in __import__('itertools').groupby(window_uses,key=lambda e:e['time_local']):
    rows=list(rows)
    clusters.append({'time_local':instant,'observations':len(rows),'channels':dict(collections.Counter(e['channel'] for e in rows)),'subjects':[e['subject'] for e in rows],'event_ids':[e['id'] for e in rows]})

def refs_at(topic,instant,limit=120):
    stamp=datetime.fromisoformat(instant).timestamp()
    found=[]
    for e in events:
        if e['family'] not in ['Google','Facebook','Uber']:continue
        haystack=(e['subject']+' '+str(e.get('url',''))).casefold()
        if any(s in haystack for s in topic) and abs(seconds(e)-stamp)<=limit:found.append(e)
    return found

explicit=[]
# Exact corroboration of support: date and a distinctive common sentence.
for index in [239,320]:
    m=mail_by_index[index];email_event=mail_events[m['id']]
    candidates=[e for e in events if e['family']=='Uber' and e['channel']=='Soporte' and e['time_utc']==email_event['time_utc']]
    if candidates:explicit.append({'type':'Uber soporte y correo: misma fecha UTC; contenido compatible conservado por separado','event_ids':[email_event['id']]+[e['id'] for e in candidates],'mail_id':m['id'],'seconds':0})
for index in [267,268]:
    m=mail_by_index[index];email_event=mail_events[m['id']]
    for e in refs_at(['com.dropbox.android'],email_event['time_utc'],120):
        explicit.append({'type':'Correo Dropbox y actividad Google: mismo servicio; proximidad temporal','event_ids':[email_event['id'],e['id']],'mail_id':m['id'],'seconds_signed_activity_minus_mail':round(seconds(e)-seconds(email_event),3),'kind':e['kind']})

verification=[mail_events[m['id']] for m in messages if 'verificación de compras de google play' in m['subject'].casefold()]
game=[mail_events[m['id']] for m in messages if '8 ball pool' in m['subject'].casefold()]
device_flags=[e for e in events if e['family']=='Google' and e['channel'].startswith('Google Play Store ·') and e['time_local'][:10] in ['2026-09-20','2026-09-21']]
summary={'generated_at_utc':datetime.now(timezone.utc).isoformat(),'source_path':str(MBOX),'source_bytes':data['source_bytes'],'source_sha256':data['source_sha256'],'messages':len(messages),'dated_messages':len(mail_events),'declared_sender_domains':dict(collections.Counter(m['sender_address'].rsplit('@',1)[-1].casefold() for m in messages)),'window_mail_count':len(window_mail),'window_mail_events':[e['id'] for e in window_mail],'window_app_usage_observations':len(window_uses),'app_usage_clusters':clusters,'mail_near_app_uses':near,'specific_crosses':explicit,'google_play_purchase_verification_mail_ids':[e['identifiers']['mail_id'] for e in verification],'game_notification_mail_ids':[e['identifiers']['mail_id'] for e in game],'installation_update_events_separate':[e['id'] for e in device_flags],'limits':['Date es una cabecera declarada con zona, no un registro de lectura.','Los remitentes se describen según cabeceras sin verificación criptográfica.','Uso registrado, primer plano, instalación y actualización son conceptos distintos.','La cercanía de correo y apps no determina causalidad.','La aclaración del usuario sobre Uber es que no hubo clonación.','El MBOX original íntegro y los adjuntos internos se conservan para la subida completa.']}
save('datos/correo-cruces-play.json',summary)
public_messages=[{k:m[k] for k in ['id','mbox_index','message_id','date_header','time_utc','from','sender_address','to','delivered_to','labels','public_subject','public_body','page','attachments','mime_defects']} for m in messages]
save('datos/correo-indice.json',public_messages)
path=OUT/'datos/correo-play-20-21.csv'
with path.open('w',encoding='utf-8-sig',newline='') as f:
    fields=['id','time_local','time_utc','channel','kind','subject','url','source_code','source_path','locator']
    writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader()
    for e in window_uses:writer.writerow({k:json.dumps(e[k],ensure_ascii=False) if isinstance(e.get(k),dict) else e.get(k) for k in fields})
path.chmod(0o600)
correlations=[c for c in read('actividad-correlaciones.json') if not c.get('mail_extension')]
for c in explicit:c['mail_extension']=True
correlations.extend(explicit);save('datos/actividad-correlaciones.json',correlations)

parts=[]
def h(t):parts.append({'type':'heading','text':t})
def p(t):parts.append({'type':'paragraph','text':t})
def link(t,path):parts.append({'type':'link','text':t,'url':Path(path).as_uri()})
def evidence(e):parts.append({'type':'evidence','event_id':e['id'],'text':e['time_local']+' · UTC '+e['time_utc']+' · '+e['channel']+'\n'+e['subject']+'\n'+e['source_code']+' · '+json.dumps(e['locator'],ensure_ascii=False),'url':Path(e['source_path']).as_uri()+('#correo-'+str(e['locator']['mbox_message_index_1based']) if 'mbox_message_index_1based' in e['locator'] else '')})
def mail(index):
    m=mail_by_index[index];evidence(mail_events[m['id']]);link('Leer correo local '+m['id'],OUT/m['page'])
h('Correo local: aplicaciones, Etsy, Hermes, Clarín y Google Play')
p(f"Se incorporan {len(messages):,} mensajes del MBOX de Documentos, original de {data['source_bytes']:,} bytes y SHA-256 {data['source_sha256']}. El corpus tiene principalmente hadilene116@gmail.com en sus cabeceras de destinatario. Se conserva cada correo y sus adjuntos en el original íntegro; las páginas locales facilitan la lectura. La cronología añade Date declarado con su zona: no confunde envío con lectura o apertura de una aplicación. Los remitentes no se han validado criptográficamente.")
p('La subida completa autorizada por el usuario conserva los archivos originales y todos los datos privados del conjunto investigado en el repositorio privado. Las vistas de lectura facilitan consulta local; el original permanece disponible íntegro. Se mantiene la aclaración del usuario de que no hubo clonación de Uber y que simplemente no entendía los registros.')
link('MBOX original completo',MBOX)
h('La pista de validar con una imagen: rostro o huella en Play')
p('Dos correos de Google Play, del 12-09 a las 10:28:53 y del 26-09 a las 00:59:28 México, dicen que se actualizó la verificación de compras en Redmi 23129RA5FL para usar rostro o huella. Esta es una candidata concreta para la pista de validar con una imagen más rápido; no demuestra que sea la búsqueda recordada ni una validación mediante Google Lens. El propio correo delimita la configuración a esa cuenta y ese dispositivo.')
mail(305);mail(11)
h('Etsy el 20 por la noche: Google y correo de Etsy')
p('El 20-09 a las 21:50:33 México aparecen dos correos: Google indica que se usó Acceder con Google para Etsy y que se compartieron nombre/foto de perfil y dirección de correo; Etsy pregunta por una sesión Chrome 135 / Android 15 y menciona Pachuca como ubicación en su aviso. La ubicación es la descrita por el correo, sin identificar a una persona. Se relaciona con las visitas Etsy y el PAGE_VIEW recibido por Meta esa noche, sin equiparar los IDs empresariales de Meta a una credencial de acceso.')
mail(285);mail(202)
for e in refs_at(['etsy'],mail_events['M000202']['time_utc'],180):
    if e['family']!='Uber':evidence(e)
h('Hermes y Clarín: dos servicios y momentos distintos')
p('Hermes.com envió dos correos para finalizar creación de cuenta, a las 22:56:33 y 23:00:47 del 20-09. Son de ecommerce.hermes.com, la tienda, y piden confirmar el correo con un código; el texto dice que, si se ignora, no se crea la cuenta. No se presentan como confirmación de una cuenta terminada ni como Hermes Agent. Clarín envía una bienvenida el 21-09 a las 15:00:17 y agradece el registro. No hay en estos mensajes una cadena que convierta el número 6850175308 o un ID de Meta en mecanismo de identificación compartido entre los tres servicios.')
mail(226);mail(225);mail(138)
h('Google Play y Analytics: qué uso de apps está registrado')
p(f"En el intervalo 20-09 18:00 → 22-09 00:00 México se recuperan {len(window_uses)} observaciones de uso de apps en Google Play/Google Analytics, además de {len(device_flags)} registros de instalación o actualización separados. Se guardan todos los usos en el CSV y se agrupan por marca temporal. Un registro Se ha utilizado/Has utilizado documenta el uso registrado por ese producto; no acredita por sí solo que una persona abriera manualmente la app en primer plano.")
link('Usos de apps del 20/21 en CSV',OUT/'datos/correo-play-20-21.csv')
for c in sorted(clusters,key=lambda c:c['observations'],reverse=True)[:3]:
    p(c['time_local']+' · '+str(c['observations'])+' observaciones: '+'; '.join(c['subjects'])+'. La hora compartida no implica aperturas simultáneas.')
h('Dropbox: un cruce muy próximo con la actividad de la app')
p('El 21-09 a las 07:03:33 aparecen búsqueda/ficha de Dropbox en Play. Los avisos de correo son de 07:04:25 (Dropbox for Android) y 07:04:26 (explorador web). Google Analytics registra uso de com.dropbox.android a las 07:04:32: seis/siete segundos después de los avisos. Son representaciones coherentes por servicio y proximidad; se conservan ambas, sin atribuir la sesión a otra persona ni inferir una automatización.')
mail(268);mail(267)
for c in explicit:
    if 'Dropbox' in c['type']:
        e=byid[c['event_ids'][1]]
        if e['kind']=='uso de app':evidence(e)
mail(235)
p('A las 07:05:45 el correo de Google informa Acceder con Google para WPS Office. Ese mensaje describe una conexión de cuenta; las entradas de Play permiten revisar usos e instalaciones por separado. No se convierte automáticamente en una apertura de WPS a esa misma hora.')
h('Uber: soporte corroborado y un recibo que aclara las horas Local')
mail(239)
p('El correo de soporte Uber del 18-09 a las 06:42:14 coincide exactamente en fecha UTC con la respuesta del CSV customer_support_tickets. Se puede leer la misma respuesta en dos exportaciones. Esto mantiene la aclaración actual del usuario: no hubo clonación, el mensaje reflejaba su duda de entonces.')
mail(181)
p('El recibo Eats del 21-09 muestra pedido 12:50 p.m., entrega 1:50 p.m. y pago/monto extra 3:00 p.m.; Date del correo es 15:00:47 México. Esto corrobora la interpretación local de Request_Time_Local=12:50:08 y Final_Delivery_Time_Local=13:50:14 del CSV, pese al sufijo Z. El correo posterior es un recibo con monto extra, no necesariamente el momento de entrega. La codificación del CSV se conserva sin modificar.')
h('La pista del juego en un mensaje de Facebook')
mail(166)
p('Hay una notificación de Facebook del 24-09 a las 09:21:33: 8 Ball Pool Game te envió un mensaje y tienes 9 notificaciones más. Relaciona el nombre del juego con un aviso, pero su fecha está fuera de la noche del 20/21. El cuerpo no recupera el mensaje del juego. No se presenta como prueba de infección, un ataque o bloqueo del teléfono.')
h('Apple y Google: avisos recuperados por correo')
for index in [262,261,260]:mail(index)
p('Los tres correos Apple del 21-09 avisan de uso de iCloud en navegador. Sus cuerpos describen horas UTC distintas de Date por el tiempo de envío; se conservan ambos. Aportan avisos históricos de correo, sin consultar Apple Home o recuperar automatizaciones. Los registros iPhone del CSV Google se mantienen como actividad del dispositivo, no como prueba de identidad de quien actuó.')
for index in [173,284,158,157]:mail(index)
p('Otros avisos del 21-09 describen cambio de contraseña Google (13:45:32), borrado de grupo familiar (09:42:07) y solicitudes de ayuda para acceder (18:37:14 y 18:39:22). Los mensajes de recuperación indican revisar eduardovelez@tutanota.de después de 30 días. Son el contenido de los avisos y no identifican quién realizó las acciones. No se atribuyen automáticamente a un ataque.')
h('Cómo seguir cada cruce')
p(f"Hay {len(window_mail)} correos en la ventana del 20/21 y {len(explicit)} cruces específicos guardados, además del contexto de usos de apps a ±5 minutos. El JSON distingue relaciones por texto/fecha y simples vecindades temporales. Los valores originales y adjuntos quedan íntegros en el MBOX y en el archivo privado de investigación. Los códigos M identifican el mensaje del MBOX; los E son de esta versión de la cronología.")
link('Índice local de correo',OUT/'datos/correo-indice.json');link('Cruces de correo y apps',OUT/'datos/correo-cruces-play.json')
for item in parts:item['mail_extension']=True
structured=[p for p in read('informe-estructurado.json') if not p.get('mail_extension')];structured[3:3]=parts
save('datos/informe-estructurado.json',structured)
report='\n\n'.join(('## '+p['text']) if p['type']=='heading' else ('['+p['text']+']('+p['url']+')') if p['type']=='link' else ('**'+p['event_id']+'** · '+p['text']) if p['type']=='evidence' else p['text'] for p in parts)+'\n'
path=OUT/'correo-cruces-play.md';path.write_text(report);path.chmod(0o600)
logpath=OUT/'registro.md';log=logpath.read_text();block='<!-- INICIO_RESULTADOS_SESION_9 -->\n## Sesión 9: correo y uso de apps\n\n'+report+'\n<!-- FIN_RESULTADOS_SESION_9 -->'
if '<!-- INICIO_RESULTADOS_SESION_9 -->' in log:log=re.sub(r'<!-- INICIO_RESULTADOS_SESION_9 -->.*?<!-- FIN_RESULTADOS_SESION_9 -->',lambda _:block,log,flags=re.S)
else:log+='\n\n'+block+'\n'
logpath.write_text(log);logpath.chmod(0o600)

# Las relaciones de correo se añaden después del informe base: actualizar su visor.
timeline=OUT/'historial-cruzado.html';html=timeline.read_text()
match=re.search(r'<script id="dataset" type="application/json">(.*?)</script>',html,re.S)
payload=json.loads(match[1]);payload['relations']=correlations
serialized=json.dumps(payload,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
html=html[:match.start(1)]+serialized+html[match.end(1):]
html=html.replace('r.id,r.subject,r.url,r.channel','r.id,r.subject,r.body_search,r.url,r.channel')
timeline.write_text(html);timeline.chmod(0o600)

print(json.dumps({'messages':len(messages),'window_mail':len(window_mail),'window_usage_observations':len(window_uses),'specific_crosses':len(explicit)},ensure_ascii=False))
