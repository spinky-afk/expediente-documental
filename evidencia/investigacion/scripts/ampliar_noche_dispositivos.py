#!/usr/bin/env python3
"""Revisión del 20/21 de septiembre: mensajes, juegos, respaldo y dispositivos."""
import collections
import hashlib
import json
import os
import re
from datetime import datetime,timezone
from pathlib import Path
from facebook_util import Document

OUT=Path(__file__).resolve().parents[1]
GOOGLE=Path('/home/deep-logic/Documentos/Registro/Takeout')
FB=Path('/home/deep-logic/Documentos/facebook')
def read(n):return json.loads((OUT/'datos'/n).read_text())
def write(n,t):
    p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t);p.chmod(0o600)
def save(n,v):write(n,json.dumps(v,ensure_ascii=False,indent=2)+'\n')
events=read('actividad-cronologica.json');sources=read('catalogo-fuentes.json');by_path={s['path']:s for s in sources}
window=[e for e in events if '2026-09-20T18:00:00'<=e['time_local'][:19]<'2026-09-22T00:00:00']
def source(p):
    p=Path(p);return by_path.get(str(p),{'code':'anexo sin fecha','path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size})
def field(text,label):
    m=re.search(r'^'+re.escape(label)+r':\s*(.*)$',text,re.M);return m[1] if m else None

devices=[];raw_devices=[]
for p in sorted((GOOGLE/'Servicio de configuración de dispositivos Android').glob('*.html')):
    doc=Document(p.read_text());text=doc.root.clean()
    fields={k:field(text,k) for k in ['ID de Android','IMEI','Números de serie','Modelo','ID de cliente socio','Hora del registro','Hora de la primera conexión de datos','Hora de la última conexión de datos','Motivo de la última conexión de datos','Paquete de apps que activó la última conexión de datos']}
    raw_devices.append({'source':source(p),'fields':fields})
    row={'source':source(p),'android_id':fields['ID de Android'],'model':fields['Modelo'],'imei_suffix':(fields['IMEI'] or '').split(',')[0][-4:],'serial_sha256':hashlib.sha256((fields['Números de serie'] or '').encode()).hexdigest(),'imei_sha256':hashlib.sha256((fields['IMEI'] or '').split(',')[0].encode()).hexdigest(),'partner_client_id':fields['ID de cliente socio'],'registration_original':fields['Hora del registro'],'first_connection_original':fields['Hora de la primera conexión de datos'],'last_connection_original':fields['Hora de la última conexión de datos'],'last_connection_reason':fields['Motivo de la última conexión de datos'],'trigger_package':fields['Paquete de apps que activó la última conexión de datos']}
    devices.append(row)
groups=collections.defaultdict(list)
for d in devices:groups[(d['imei_sha256'],d['serial_sha256'],d['model'])].append(d['android_id'])
assert len(groups)==1 and len(devices)==5
save('privado/dispositivos-configuracion-completos.json',raw_devices)
save('datos/dispositivos-cruzados.json',{'generated_at_utc':datetime.now(timezone.utc).isoformat(),'configuration_records':devices,'hardware_groups':len(groups),'same_imei_and_serial':True,'interpretation':'Los cinco registros comparten modelo, IMEI primario y serie. Esto agrupa registros de configuración; no demuestra cinco teléfonos físicos, clonación, restablecimiento de fábrica ni la causa del cambio de ID. Las instalaciones de Play solo se pueden relacionar por atributos de modelo, fabricante y operador en este export.'})

home=[]
for p in sorted((GOOGLE/'App de Home').glob('*.json')):
    obj=json.loads(p.read_text());empty=obj=={} or all(v==[{}] for v in obj.values())
    home.append({'source':source(p),'top_level_keys':list(obj),'content_empty':empty,'structure':obj})
assert all(x['content_empty'] for x in home)
save('datos/google-home-revision.json',{'files':home,'automation_commands_recovered':0,'permissions_recovered':0,'home_members_recovered':0,'limitation':'Estructuras vacías en esta exportación. No permite afirmar que se ejecutaron automatizaciones ni que nunca existieron. No hay exportación de Apple Home disponible; el usuario la deja pendiente.'})

gamebase=GOOGLE/'Servicios de juego de Google Play'
player=gamebase/'Global/Player.html';playtime=gamebase/'Global/Playtime.html'
scorespath=FB/'your_facebook_activity/facebook_gaming/your_latest_instant_game_scores.html'
fb_names=[]
for n,row in Document(scorespath.read_text()).tables():
    name=row.get('Nombre de la app')
    if name and name not in fb_names:fb_names.append(name)
allgames=FB/'your_facebook_activity/facebook_gaming/instant_games.html'
all_names=[]
for n,row in Document(allgames.read_text()).tables():
    name=row.get('Nombre de la app')
    if name and name not in all_names:all_names.append(name)
gamefiles=[]
for p in sorted(gamebase.rglob('Data.bin')):
    original=p.read_text();data=json.loads(original) if original.startswith('{') else original
    if isinstance(data,dict) and isinstance(data.get('ALF.UserProperties'),str):data['ALF.UserProperties_decoded']=json.loads(data['ALF.UserProperties'])
    gamefiles.append({'source':source(p),'saved_game_name':p.parent.name,'data':data})
save('datos/juegos-perfiles-respaldo.json',{'google_play_player':{'source':source(player),'text':Document(player.read_text()).root.clean(),'profile_created_local':'2026-09-21T05:17:55-06:00','gamer_id':'FamousSmile6745','last_game':'Words of Wonders: Crucigrama'},'google_play_playtime':{'source':source(playtime),'text':Document(playtime.read_text()).root.clean(),'reported_duration_seconds':10,'reported_sessions':0,'first_session_local':'2026-09-21T05:17:44-06:00','last_session_local':'2026-09-21T05:18:05-06:00'},'saved_game_files':gamefiles,'facebook_three_score_entries':{'source':source(scorespath),'games':fb_names},'facebook_instant_games':{'source':source(allgames),'games':all_names},'interpretation':'Dos archivos guardados pertenecen al mismo juego com.fugo.wow. La lista de tres puntuaciones de Facebook no es el catálogo completo: instant_games.html contiene nueve nombres. No se recuperó evidencia técnica que establezca que un juego infectó dispositivos.'})

msgs=[e for e in window if e['channel']=='Messenger'];number_map={};names=[]
for e in msgs:
    path=Path(e['source_path']);doc=Document(path.read_text());pos=(e['locator']['html_line_1based'],e['locator']['html_column_0based']);node=next(n for n in doc.root.nodes() if n.pos==pos)
    numbers=collections.Counter(re.findall(r'\b\d{6,22}\b',node.clean()))
    for num in numbers:number_map.setdefault(num,[]).append(e['id'])
msg_matches={}
for num,ids in number_map.items():
    matches=[str(p.relative_to(FB)) for p in FB.rglob('*.html') if num in p.read_text()]
    msg_matches[num]={'observations':ids,'source_files_with_literal_value':matches,'appears_in_gaming_sources':any('/facebook_gaming/' in '/'+x for x in matches)}
save('datos/facebook-mensajes-evento-20-21.json',{'window_local':['2026-09-20T18:00:00-06:00','2026-09-22T00:00:00-06:00'],'messages':msgs,'numeric_matches':msg_matches,'outgoing_business_message_confirmed':False,'interpretation':'Dos representaciones en los chats SOY MASON y UN ETERNO APRENDIZ de un adjunto enviado por SOY MASON a las 14:03:05 del 21. El texto anuncia una biblioteca, no identifica un ataque ni un evento de juego. Los números repetidos no aparecen en otros HTML de Facebook fuera de estas dos conversaciones; su función exacta no se deduce del export.'})

clusters=[]
use_counts=collections.Counter(e['time_local'] for e in window if e['kind']=='uso de app')
for instant,count in use_counts.most_common(2):
    rows=[e for e in window if e['kind']=='uso de app' and e['time_local']==instant]
    clusters.append({'instant_local':instant,'observations':count,'events':[e['id'] for e in rows],'subjects':[e['subject'] for e in rows],'interpretation':'Misma hora registrada para numerosas apps. No prueba ejecución simultánea, automatización, instalación maliciosa ni quién inició una copia de seguridad.'})
focused={'generated_at_utc':datetime.now(timezone.utc).isoformat(),'timezone':'America/Mexico_City','interval_local':['2026-09-20T18:00:00-06:00','2026-09-22T00:00:00-06:00'],'dated_observations':len(window),'events':window,'app_use_clusters':clusters,'user_clues':['mensajes y un ataque respaldos automaticos','un mensaje tambien a un perfil de negocios','se relaciona con un juego','no se puede hacer un restablecimiento del celular','dispositivos cruzados','automatizacion mediante home de google y home de apple','en el perfil de juegos hay 2 o 3 juegos','mensajes de facebook sobre un evento en chat'],'claims_status':'Pistas y afirmaciones del usuario; no se consideran hechos probados por defecto.','limits':'Sin registro de error de restablecimiento, ejecución de malware o automatización Apple/Home recuperados. Actividad de Chat/Gmail no es el contenido de los mensajes. Los IDs E corresponden a esta nueva versión.'}
save('datos/noche-20-21-septiembre.json',focused)

web=[
 {'id':'N01','title':'Ficha del desarrollador: HomeKit App for Android Hints','url':'https://play.google.com/store/apps/details?id=com.snailhd.inara.app','notes':'La ficha actual del paquete encontrado en el historial lo describe como guía educativa independiente, sin afiliación con Apple. Su descripción o presencia en Play no constituye una auditoría del APK ni demuestra malware.','status':'contenido actual verificado'},
 {'id':'N02','title':'Google: respaldo y restauración de Android','url':'https://support.google.com/android/answer/2819582?hl=es-419','notes':'Android puede respaldar apps, datos, configuración y mensajes automáticamente. Al agregar la cuenta a un teléfono configurado puede recuperar datos guardados. El uso de componentes de respaldo por sí solo no prueba un ataque.','status':'contenido actual verificado'},
 {'id':'N03','title':'Google: dispositivos y sesiones de cuenta','url':'https://support.google.com/accounts/answer/3067630?hl=es-419','notes':'Un mismo dispositivo puede tener varias sesiones. Las horas incluyen comunicación en segundo plano y sincronización; no deben confundirse con una nueva autenticación exitosa o una persona usando el teléfono.','status':'contenido actual verificado'},
 {'id':'N04','title':'Google: restablecimiento de fábrica Android','url':'https://support.google.com/android/answer/6088915?hl=es-419','notes':'Referencia del procedimiento general y requisitos de credenciales. No se ejecutó un restablecimiento. Esta ayuda no identifica la causa del problema concreto referido por el usuario.','status':'página oficial consultada'},
 {'id':'N05','title':'Apple: app Home oficial','url':'https://www.apple.com/home-app/','notes':'Apple describe Home para sus dispositivos y accesorios. Es una referencia sobre el producto, sin demostrar que existan automatizaciones en una cuenta concreta del usuario.','status':'resultado oficial consultado'}]
for w in web:w.update(consulted_on='2026-10-01',relationship='Consulta técnica actual; la evidencia personal se conserva por separado en las exportaciones locales.')
save('datos/noche-dispositivos-fuentes-web.json',web)
save('datos/noche-dispositivos-consultas-web.json',{'consulted_on':'2026-10-01','queries':['site.support.google.com accounts several sessions same device factory reset device activity','site.support.google.com googlenest automations Google Home history Takeout','site.support.apple.com Home app iPhone iPad Mac Apple Home Android','site.play.google.com HomeKit App for Android Hints'],'directly_opened':[w['url'] for w in web if w['id']!='N05']})

parts=[]
def h(t):parts.append({'type':'heading','text':t})
def p(t):parts.append({'type':'paragraph','text':t})
def link(t,path):parts.append({'type':'link','text':t,'url':Path(path).as_uri()})
def evidence(e):parts.append({'type':'evidence','event_id':e['id'],'text':f"México {e['time_local']} · UTC {e['time_utc']}\n{e['channel']} · {e['subject']}\n{e['source_code']} · {json.dumps(e['locator'],ensure_ascii=False)}",'url':e.get('url')})
h('Noche del 20 y día 21: mensajes, juegos, respaldos y dispositivos')
p(f"Revisión de {len(window)} observaciones del 20-09-2026 18:00 al 22-09-2026 00:00, hora de Ciudad de México. Se incorporaron 173 fechas de configuración Android, juegos y registros de sincronización de Chrome antes omitidas; la cronología completa tiene {len(events):,} observaciones y {len(sources)} fuentes. Los IDs E se reasignaron al ordenar esta versión; las referencias duraderas son ruta, localizador y SHA-256. La versión anterior permanece en el historial Git local.")
h('El respaldo que sí aparece antes de esa noche')
p('El 20 de septiembre a las 14:02:14 hubo una pregunta de Gemini en Workspace: «Backup en enlace». La respuesta de Gemini cita Cloud Backup and Restore en Drive, ID 1iO7scCcYFZiCkEFrMaqHI2BwIAIxEy9L. Es una respuesta y referencia exportada; la exportación no incluye el contenido de la carpeta. Queda fuera del intervalo nocturno y se conserva como contexto previo.')
for e in events:
    if e['source_path'].endswith('conversation_1789934534.txt') and 'turn_last_modified' in json.dumps(e['locator']):evidence(e)
if (OUT/'datos/drive-cloud-backup-listado.json').exists():
    p('Corrección de alcance de las consultas externas: el usuario indicó que se debe consultar hadilene116@gmail.com. La comprobación posterior google_drive_get_profile identifica la conexión actual como velez@deeplogic.com.mx. Las consultas previas no verificaron la identidad en el momento de lectura; se conservan separadas y no establecen el estado del Drive de hadilene116@gmail.com ni la propiedad de los archivos. Se suspenden nuevas lecturas de archivos en esa conexión hasta autorizar la cuenta solicitada. La contraseña aportada no se transcribe al registro, al sitio ni al PDF.')
    p('Dentro de esas consultas de alcance no atribuible a la cuenta solicitada, los metadatos devuelven la carpeta Cloud Backup and Restore, creada el 20-09-2026 13:01:59.315 UTC y modificada el 27-09-2026 00:29:43.649 UTC; el listado devuelve cero archivos hijos visibles. Las tres referencias Lark Player respondieron 404. Ninguno de estos resultados permite afirmar que falten o se hayan borrado archivos de hadilene116@gmail.com, reconstruir contenido anterior o atribuir cambios a una persona.')
    link('Verificación local de la cuenta conectada y corrección de alcance',OUT/'datos/drive-identidad-consultada.json')
    p('El Takeout local sí incluye hadilene116@gmail.com en Perfil/Perfil.json y Cuenta de Google/hadilene116.SubscriberInfo.html. Estos archivos identifican el conjunto exportado y permiten continuar su análisis local. La exportación y el conector de Drive se mantienen como fuentes distintas; esta identificación no determina quién realizó cada acción.')
    link('Perfil conservado del Takeout',GOOGLE/'Perfil/Perfil.json')
    link('Información del suscriptor conservada del Takeout',GOOGLE/'Cuenta de Google/hadilene116.SubscriberInfo.html')
    link('Comprobación de procedencia del Takeout local',OUT/'datos/cuenta-takeout-local.json')
    link('Resultado local de consulta de metadatos Drive',OUT/'datos/drive-respaldos-consulta-reintento.json')
    link('Listado local de la carpeta de respaldo',OUT/'datos/drive-cloud-backup-listado.json')
h('Mensajes y el perfil de negocios que se recuerda')
for e in window:
    if e['subject']=='Has chateado con Ayuda de Google':evidence(e)
p('Hay una acción de chat con Ayuda de Google el 20 a las 19:19:57. El registro no contiene el texto de la conversación ni una empresa destinataria. A las 20:47:22 aparece una búsqueda del número 6850175308 en Google Chat; una búsqueda no establece que se haya enviado un mensaje.')
for e in window:
    if e['channel']=='Chat':evidence(e)
p('En las conversaciones exportadas solo se recuperaron dos observaciones de Messenger en esta ventana: ambas del 21 a las 14:03:05. SOY MASON figura como remitente y se comparte una publicación sobre una biblioteca masónica en los chats SOY MASON y UN ETERNO APRENDIZ. No se halló en esta ventana un mensaje saliente verificable a un perfil empresarial. La ausencia en esta copia no demuestra que nunca se enviara.')
for e in msgs:evidence(e)
p('El enlace del adjunto contiene el ID 61553075107468. El cuerpo también repite 478547315650144, 1635855486666999 y 1678524932434102. Esos valores se hallaron únicamente en las dos conversaciones dentro de los HTML revisados; no coinciden con los IDs de empresas ya catalogados ni con las fuentes de juegos. No se les asigna una función de autenticación, empresa o ataque.')
h('Los dos o tres juegos: dos listas diferentes')
p('El perfil de Juegos de Google Play es privado, con ID FamousSmile6745 y creación el 21 a las 05:17:55. La sección de último juego contiene Words of Wonders: Crucigrama. La copia del producto contiene un juego y dos archivos guardados de ese juego: ALF.FugoID y com.fugo.wow.cloudData. Son dos recursos guardados, no dos juegos distintos.')
link('Perfil original de Juegos de Google Play',player);link('Resumen original de sesión de juego',playtime)
p('Playtime indica comienzo 05:17:44, fin 05:18:05, duración declarada de 10 segundos y Number of Sessions=0. Se preservan esos valores tal como están; el intervalo entre extremos es 21 segundos, por lo que no se reemplaza la duración declarada por una duración calculada. Los metadatos guardados tienen modificación 05:18:02 y 05:18:04.')
for e in window:
    if e['channel']=='Servicios de juego de Google Play':evidence(e)
p('En Facebook, Tus puntuaciones más recientes en juegos instantáneos contiene exactamente tres nombres: Chess Club, Club de Pool: Billar 8 bolas y 8 Ball Pool. El catálogo distinto Juegos instantáneos contiene nueve nombres. Las fechas que aparecen en estas secciones son principalmente de octubre de 2025 y junio de 2026; no se recuperó una sesión de esos tres juegos del 20/21 de septiembre.')
link('Las tres puntuaciones de juegos en Facebook',scorespath);link('Catálogo completo de juegos instantáneos',allgames)
h('Respaldos, restauración y coincidencias de hora')
p('El 20 a las 23:15:33 se buscó com.google.android.apps.restore. El 21 a las 04:14:28 se visitó una referencia de Drive titulada tweakradje - Restore apps (Android Switch); a las 04:29 y 06:01 hubo más consultas sobre restauración, y a las 06:16 búsquedas tweaking restore/tweaking restore android. Son consultas y visitas, sin el contenido del archivo de Drive ni una prueba de ejecución.')
for e in window:
    if e['kind']!='uso de app' and any(t in e['subject'].lower() for t in ['com.google.android.apps.restore','tweakradje','tweaking restore','back up or restore']):evidence(e)
for c in clusters:p(f"A {c['instant_local']} hay {c['observations']} observaciones de uso de apps con la misma marca temporal. Aparecen componentes de Xiaomi/Google, apps personales y juegos. Esa coincidencia no identifica una automatización ni prueba que una persona abriera todas las apps exactamente a la vez.")
for e in window:
    if any(t in e['subject'].lower() for t in ['com.miui.backup','com.miui.cloudbackup','android switch']):evidence(e)
p('Google documenta respaldos automáticos y recuperación de apps/datos al configurar la cuenta [N02]. En los archivos revisados no hay un registro de error de restablecimiento ni una cadena técnica que atribuya el problema a un juego. El campo Device Booted señala un arranque; no prueba un restablecimiento de fábrica.')
p('Words of Wonders, Android Switch y Xiaomi Home comparten la marca lastUpdateTime 2026-09-21T12:35:14.706367Z (06:35:14.706367 México) en Installs.json, entradas 53, 136 y 466. Es una coincidencia concreta del inventario de instalaciones, sin probar una relación causal ni identificar un programa que inicie restauraciones.')
install_path=next(GOOGLE.glob('Google*Play*Store/Installs.json'))
link('Inventario original de instalaciones, entradas 53, 136 y 466',install_path)
p('El inventario también registra AirDroid Parental Control, entrada 433, con firstInstallationTime 26-09-2026 23:55:17.240431 UTC (17:55:17.240431 México), modelo 23129RA5FL. Es posterior al intervalo recordado. El título de la app y su instalación no demuestran quién la instaló, sus permisos activos ni que bloqueara un restablecimiento.')
h('Cinco IDs de Android con el mismo hardware registrado')
p('Los IDs 3644671859603123984, 3778158131092576330, 3975241346881164962, 4247182940332696163 y 4511226476644240739 coinciden en modelo 23129RA5FL, IMEI primario terminado en 0505 y número de serie. El IMEI completo y la serie quedan en el anexo privado. Esta coincidencia agrupa registros de hardware; no acredita cinco teléfonos ni clonación.')
for d in devices:
    p(d['source']['code']+' · ID '+d['android_id']+' · registro: '+str(d['registration_original'])+' · última conexión: '+str(d['last_connection_original'])+' · motivo: '+str(d['last_connection_reason']))
    link('Configuración original Android '+d['android_id'],d['source']['path'])
p('El registro 3975241346881164962 tiene conexiones correctas el 21 a las 05:14:17 y 14:00:06; el último motivo es Device Booted. El CSV de acceso contiene registros de actividad Android, Linux, Windows e iPhone. Sus tiempos son actividad/última comunicación, no se presentan como inicios de sesión exitosos de otras personas. Google explica que un dispositivo puede tener varias sesiones y actividad de sincronización en segundo plano [N03].')
for e in window:
    if e['channel']=='Configuración de dispositivos Android':evidence(e)
h('Google Home, la app de consejos HomeKit y Apple pendiente')
p('Los ocho JSON del producto App de Home contienen {} o una lista con un objeto vacío. Automations.json, ApplicationPermissions.json y HomeApp.json no aportan reglas, permisos ni miembros recuperables. No se puede reconstruir automatización doméstica de esta copia.')
for x in home:link('Original Google Home: '+Path(x['source']['path']).name,x['source']['path'])
p('El 21 a las 06:35 se buscaron apple home/apple homekit en Play. A las 06:36:04.337999 se registró la instalación de HomeKit App for Android Hints para el modelo 23129RA5FL, paquete com.snailhd.inara.app. La ficha actual del desarrollador describe una guía educativa independiente sin afiliación con Apple [N01]. Encontrar esta app no acredita la app Home oficial, acceso a una casa de Apple ni infección.')
for e in window:
    if any(t in e['subject'].lower() for t in ['homekit app','apple home']):evidence(e)
p('Apple se deja pendiente porque el usuario indica que por ahora no puede consultar sus datos. En esta fase no se ha accedido a Apple Home ni realizado cambios en sus dispositivos. Las visitas a iCloud recuperadas son actividad web, no un historial de comandos de Home.')
h('Qué sigue sin resolverse')
p('No se ha identificado el juego recordado con certeza, un evento de chat que cause cambios en dispositivos, un mensaje empresarial saliente del intervalo, la causa del problema de restablecimiento ni una ejecución de automatizaciones de Home. Las exportaciones no incluyen imágenes de disco, APK inspeccionados o el texto íntegro de Gmail/Google Chat. Se conservan pistas y límites en los anexos, sin convertir coincidencias en una atribución de ataque.')
for w in web:parts.append({'type':'link','text':w['id']+' · '+w['title'],'url':w['url']})
for item in parts:item['noche_extension']=True
structured=[p for p in read('informe-estructurado.json') if not p.get('noche_extension')];structured[3:3]=parts
save('datos/informe-estructurado.json',structured)
md=[]
for item in parts:
    if item['type']=='heading':md.append('## '+item['text'])
    elif item['type']=='link':md.append('['+item['text']+']('+item['url']+')')
    else:md.append(('**'+item['event_id']+'** · ' if item['type']=='evidence' else '')+item['text'])
report='\n\n'.join(md)+'\n';write('noche-20-21-juegos-respaldos-dispositivos.md',report)
lp=OUT/'registro.md';log=lp.read_text();block='<!-- INICIO_RESULTADOS_SESION_6 -->\n## Sesión 6: pistas del 20/21 y dispositivos\n\n'+report+'\n<!-- FIN_RESULTADOS_SESION_6 -->'
if '<!-- INICIO_RESULTADOS_SESION_6 -->' in log:log=re.sub(r'<!-- INICIO_RESULTADOS_SESION_6 -->.*?<!-- FIN_RESULTADOS_SESION_6 -->',lambda _:block,log,flags=re.S)
else:log+='\n\n'+block+'\n'
write('registro.md',log)
print(json.dumps({'window_events':len(window),'total_events':len(events),'sources':len(sources),'messages_in_window':len(msgs),'device_configuration_ids':len(devices),'matching_hardware_groups':len(groups),'facebook_latest_score_games':fb_names,'google_home_empty_files':len(home)},ensure_ascii=False))
