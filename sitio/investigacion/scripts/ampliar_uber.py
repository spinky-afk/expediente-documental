#!/usr/bin/env python3
"""Cruza exportaciones Uber, Google y Facebook con evidencia y límites explícitos."""
import collections
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from uber_util import ROOT, rows, ZONE

OUT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((OUT/'datos'/name).read_text())
def save(name,value):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n');p.chmod(0o600)
events=read('actividad-cronologica.json');sources=read('catalogo-fuentes.json');byid={e['id']:e for e in events};by_path={s['path']:s for s in sources}
analytic={p:[e for e in events if e['family']=='Uber' and e['channel']==p+' · Analytics'] for p in ['Rider','Eats']}
links=[c for c in read('actividad-correlaciones.json') if c['type'].startswith('Uber:')]
inventory=[];statistics={};device_records=[]
for path in sorted(ROOT.rglob('*')):
    if not path.is_file():continue
    item={'path':str(path),'relative_path':str(path.relative_to(ROOT)),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_code':by_path[str(path)]['code']}
    if path.suffix=='.csv':item['rows']=sum(1 for _ in rows(path))
    inventory.append(item)
for product,name in [('Rider','Rider/rider_app_analytics-0.csv'),('Eats','Eats/eats_app_analytics-0.csv')]:
    data=list(rows(ROOT/name));records=analytic[product]
    window=[e for e in records if '2026-09-20T18:00:00'<=e['time_local'][:19]<'2026-09-22T00:00:00']
    groups=collections.defaultdict(list)
    for row,loc in data:
        groups[row.get('Device ID','[no exportado]')].append((row,loc))
    statistics[product]={'rows':len(data),'events':len(records),'first_utc':min(e['time_utc'] for e in records),'last_utc':max(e['time_utc'] for e in records),'first_local':min(e['time_local'] for e in records),'last_local':max(e['time_local'] for e in records),'event_types':dict(collections.Counter(row['Analytics Event Type'] for row,_ in data)),'models':dict(collections.Counter(row['Device Model'].casefold() for row,_ in data)),'window_events':len(window),'gps_epoch_rows':sum(row['GPS Time (UTC)'].startswith('1970-01-01') for row,_ in data)}
    for identity,group in groups.items():
        device_records.append({'product':product,'device_id':identity,'rows':len(group),'model_variants':sorted({row['Device Model'] for row,_ in group}),'os':sorted({row['Device OS']+'/'+row['Device OS Version'] for row,_ in group}),'first_event_utc_original':min(row['Event Time (UTC)'] for row,_ in group),'last_event_utc_original':max(row['Event Time (UTC)'] for row,_ in group),'distinct_ip_values':len({row.get('IP Address','') for row,_ in group}) if product=='Rider' else None,'source_path':str(ROOT/name),'example_locator':group[0][1]})

companies=[b for b in read('facebook-empresas-identificadores.json') if 'uber' in b['name'].casefold()]
target_ids=sorted({b['business_id'] for b in companies}|{i for b in companies for i in b['event_identifiers']})
literal_id_matches=[]
for item in inventory:
    text=Path(item['path']).read_text()
    for identity in target_ids:
        if re.search(r'(?<!\d)'+re.escape(identity)+r'(?!\d)',text):literal_id_matches.append({'id':identity,'path':item['path']})

# Exact IP strings relate networks only. The complete values remain in the local originals.
rider_ips=sorted({row['IP Address'] for row,_ in rows(ROOT/'Rider/rider_app_analytics-0.csv') if row['IP Address']})
ip_matches=[]
for ip in rider_ips:
    pattern=re.compile(r'(?<![\d.])'+re.escape(ip)+r'(?![\d.])')
    matches=[]
    for s in sources:
        if s['family']=='Uber' or 'messages/' in s['path']:continue
        if pattern.search(Path(s['path']).read_text(errors='replace')):matches.append({'source_code':s['code'],'path':s['path']})
    if matches:
        ip_matches.append({'ip_prefix':ip.rsplit('.',1)[0]+'.*','ip_sha256':hashlib.sha256(ip.encode()).hexdigest(),'sources':matches,'meaning':'Igualdad de una dirección de red en las copias, no identificación de persona o dispositivo físico.'})

order_rows=list(rows(ROOT/'Eats/user_orders-0.csv'))
order_groups=collections.defaultdict(list)
for row,loc in order_rows:order_groups[(row['Request_Time_Local'],row['Restaurant_Name'])].append((row,loc))
orders=[{'request_local_original':stamp,'restaurant':restaurant,'rows':len(group),'delivery_local_original':group[0][0]['Final_Delivery_Time_Local'],'status':group[0][0]['Order_Status'],'source_path':str(ROOT/'Eats/user_orders-0.csv'),'locators':[loc for _,loc in group],'grouping':'Agrupación analítica por hora de solicitud y restaurante; no es un ID de pedido exportado.'} for (stamp,restaurant),group in sorted(order_groups.items())]
focused=[e for e in events if e['family']=='Uber' and e['channel'] in ['Soporte','Métodos de pago'] and e['time_local'].startswith('2026-09-18')]
packet={'generated_at_utc':datetime.now(timezone.utc).isoformat(),'root':str(ROOT),'inventory':inventory,'statistics':statistics,'device_records':device_records,'cross_correlations':links,'facebook_companies':companies,'literal_facebook_ids_in_uber_export':literal_id_matches,'network_ip_matches':ip_matches,'orders_grouped':orders,'september_18_security_records':focused,'limits':['Sin ID común entre eventos Facebook/Google y filas Analytics de Uber.','Google Analytics de Mi actividad no equivale a un panel administrado por el usuario.','Pedidos Local con sufijo Z tienen conflicto de codificación; zona México interpretada y marcada como hipótesis.','Campos Time y Signup Date sin zona permanecen fuera de la cronología confirmada.','Dos Device ID de Rider con el mismo modelo no acreditan dos teléfonos o clonación.','No hay eventos Rider exportados para la noche del 20/21.','CUSTOM no describe por sí solo una acción concreta.','La respuesta de soporte afirma un restablecimiento de contraseña; no identifica accesos maliciosos, responsables o malware.']}
clarification=read('uber-aclaracion-usuario.json') if (OUT/'datos/uber-aclaracion-usuario.json').exists() else None
if clarification:packet['user_clarification']=clarification
save('datos/uber-analytics-cruces.json',packet)

parts=[]
def h(t):parts.append({'type':'heading','text':t})
def p(t):parts.append({'type':'paragraph','text':t})
def link(t,path):parts.append({'type':'link','text':t,'url':Path(path).as_uri()})
def evidence(e):parts.append({'type':'evidence','event_id':e['id'],'text':e['time_local']+' · UTC '+e['time_utc']+' · '+e['channel']+'\n'+e['subject']+'\n'+e['source_code']+' · '+e['source_path']+' · '+json.dumps(e['locator'],ensure_ascii=False),'url':Path(e['source_path']).as_uri()+('#linea-'+str(e['locator']['csv_line_1based']) if 'csv_line_1based' in e['locator'] else '')})
h('Uber Rider y Eats: cruces de Analytics, Facebook y soporte')
if clarification:
    p('Aclaración posterior del usuario, 01-10-2026: «no no lo clonaron simplemente no entendia». El usuario aclara que no hubo clonación de la cuenta Uber y que su consulta reflejaba que no entendía los datos. Se mantiene el mensaje histórico a soporte como parte del historial, acompañado de esta aclaración actual. El propósito de estos cruces es entender los registros y su funcionamiento.')
    link('Aclaración del usuario conservada localmente',OUT/'datos/uber-aclaracion-usuario.json')
p(f"Se incorporan 12 archivos de la carpeta {ROOT.parent}, situada junto a Facebook en Documentos. Los 696 archivos originales de Facebook no cambiaron respecto al inventario anterior. La nueva cronología reúne {len(events):,} observaciones fechadas y {len(sources)} fuentes; las referencias E pertenecen a esta edición. Los originales de Uber se preservan con SHA-256 y vistas locales.")
p('user_profile-0.csv y driver_profile-0.csv contienen hadilene116@gmail.com. El perfil de usuario indica User Type=Partner; el de conductor indica Driver Profile=UberEats, Is Partner=Yes y Lifetime Completed Trips=0. Es lo que declara la exportación; no acredita entregas realizadas, quién creó el perfil o una relación criminal. Las fechas Signup Date no tienen zona y no se colocan como instantes confirmados.')
for name in ['Account and Profile/user_profile-0.csv','Account and Profile/driver_profile-0.csv']:link('Perfil original '+name,ROOT/name)
h('Los dos Analytics de Uber y el producto Google Analytics')
for product,s in statistics.items():
    p(f"Uber {product}: {s['rows']:,} filas, de {s['first_local']} a {s['last_local']}, hora México. Tipos literales: {json.dumps(s['event_types'],ensure_ascii=False)}. El modelo normalizado es 23129ra5fl con Android 15. La exportación no incluye nombres específicos de acciones para CUSTOM, ni destinatarios de mensajes en estos Analytics.")
    link('Analytics original '+product,ROOT/(product+'/'+('rider' if product=='Rider' else 'eats')+'_app_analytics-0.csv'))
p('Mi actividad de Google contiene 866 observaciones del producto Google Analytics; 14 mencionan uso de Uber Eats y una visita a un sitio de Uber. Estos registros no son un informe de una propiedad de Analytics administrada por el usuario. Se cruzan con el CSV de Uber por producto y hora, conservando ambos registros y su precisión. Los eventos Uber se presentan de forma compacta en el PDF; los dispositivos y campos completos están en el visor y en cada fila original.')
h('Coincidencias de Google Analytics y Uber Eats')
ga=[c for c in links if byid[c['event_ids'][0]]['channel']=='Google Analytics']
p(f"Las {len(ga)} observaciones de uso de Uber Eats en Google Analytics tienen filas del mismo producto en una ventana de ±60 segundos. Se muestra la fila más próxima; el conteo de candidatos de la ventana queda en el JSON. La cercanía no identifica un evento único: puede haber cientos de filas en dos minutos y no hay un ID común exportado.")
for c in ga:
    a,b=[byid[identity] for identity in c['event_ids']]
    p(f"Cruce {a['id']} ↔ {b['id']}: diferencia Uber menos Google = {c['seconds_signed_uber_minus_other']:+.3f} segundos; {c['uber_rows_in_60_second_window']} filas candidatas en ±60 s.")
    evidence(a);evidence(b)
h('Facebook: tres identidades diferentes y dos horas coincidentes')
for b in companies:p(b['name']+' · ID de encabezado '+b['business_id']+' · Identificador dentro de eventos '+', '.join(b['event_identifiers'])+' · '+b['source_code'])
p('Estos seis valores de Facebook no aparecen literalmente en los 12 archivos de Uber. El identificador dentro de eventos se repite en distintos eventos de cada servicio; no se interpreta como número único de cada acción o credencial. El CSV de Analytics no aporta un identificador que permita equipararlos. El sufijo numérico del archivo de Facebook se mantiene separado.')
meta=[c for c in links if byid[c['event_ids'][0]]['channel']=='Actividad fuera de Meta']
p(f"Hay {len(meta)} candidatos temporales Facebook↔Uber, que representan dos horas de Eats repetidas en las vistas resumen/detalle. El 02-09 a las 12:39 Facebook registra ACTIVATE_APP y la fila Uber más próxima es CUSTOM a las 12:38:59.950 (−0,050 s). A las 13:23 Facebook registra CUSTOM y la fila Uber más próxima es IMPRESSION a las 13:23:25.202 (+25,202 s). Los tipos no se equiparan. Las horas Facebook son de actividad recibida, no un reloj confirmado del clic en Uber.")
for c in meta:
    for identity in c['event_ids']:evidence(byid[identity])
p('El mismo 02-09 a las 13:23 hay CUSTOM para Uber Rider en Facebook, pero no se recuperaron filas Rider próximas a esa hora. El pedido Little Caesars tiene Request_Time_Local=12:39:45 y Final_Delivery_Time_Local=13:23:22. Estas horas son compatibles con el grupo de Eats bajo la interpretación de zona Local, no una prueba de que un evento concreto represente esa entrega.')
h('La noche del 20 y el día 21')
p(f"Del 20-09 18:00 al 22-09 00:00 México hay {statistics['Eats']['window_events']:,} filas Eats y {statistics['Rider']['window_events']} Rider. El último registro Rider exportado es {statistics['Rider']['last_local']}; su ausencia en esa noche no demuestra que la app no se utilizara. El 20 a las 16:48:56 hay uso Eats en Google y la fila Uber más próxima está a +1,141 s, antes del intervalo nocturno.")
p('El 21 a las 12:49:03 Google Analytics registra uso Eats; Uber tiene CUSTOM a las 12:49:03.193. El pedido Little Caesars figura solicitado a las 12:50:08 y entregado a las 13:50:14, según sus columnas Local. Es una secuencia relacionada por producto y tiempos compatibles; la zona de pedidos sigue marcada como hipótesis por el sufijo Z contradictorio. No identifica una automatización Home, un ataque o un mensaje Facebook saliente.')
for e in events:
    if e['family']=='Uber' and e['channel']=='Eats · Pedidos' and e['time_local'].startswith('2026-09-21'):evidence(e)
h('18 de septiembre: consulta histórica a soporte y respuesta de Uber')
p('A las 05:50:32 México figura Deleted At en un método VISA/Banco Azteca. A las 06:10:32 hay un registro Creator=User que afirma «Creo que mi cuenta fue clonada y me llegan solicitudes de acceso». A las 06:42:14 Creator=Uber responde que restableció la contraseña como medida de seguridad. Se documentan la eliminación registrada, el reporte y la respuesta, sin concluir quién eliminó el método, que se confirmara clonación o que ese episodio sea el del 20/21.')
if clarification:p('La sospecha escrita entonces no describe la explicación actual del usuario: posteriormente aclaró que no hubo clonación y que simplemente no entendía lo observado. La respuesta de soporte sobre restablecer la contraseña se conserva como respuesta, sin convertirla en confirmación de aquella sospecha.')
for e in focused:evidence(e)
h('Dispositivos e IP: relaciones y límites')
for d in device_records:
    p(f"{d['product']} · Device ID {d['device_id']} · {d['rows']:,} filas · UTC original {d['first_event_utc_original']} → {d['last_event_utc_original']} · modelo {', '.join(d['model_variants'])}. Los Device ID de Rider cubren periodos distintos con el mismo modelo; no se equiparan a IMEI, Android ID o número de serie.")
p('El modelo coincide, sin distinguir mayúsculas, con las configuraciones Android del Takeout y los agentes de Facebook antes revisados. Rider no exporta IMEI/serie y Eats no exporta Device ID; este puente compara modelo/SO y no acredita una identidad física única. Las coincidencias literales de IP se guardan con referencias y prefijos en el JSON; relacionan una red, no una persona ni autoría de acciones.')
p(f"GPS Time muestra 1970-01-01 en {statistics['Rider']['gps_epoch_rows']} filas Rider y {statistics['Eats']['gps_epoch_rows']} Eats. Es una marca que se conserva como auxiliar; no se usa para afirmar actividad en 1970 ni para inventar una posición. La cronología de Analytics usa Event Time (UTC).")
h('Pedidos, viajes y mensajes sin zona')
p(f"user_orders contiene {len(order_rows)} filas de artículos, agrupables en {len(orders)} combinaciones de solicitud/restaurante; no se presentan como {len(order_rows)} pedidos diferentes. Rider tiene dos viajes: uno rider_canceled y otro completed. Se usan sus campos UTC explícitos. Los seis registros communications_sent tienen Time sin zona y dos medios repetidos, intercom_text/push; se preservan íntegros entre los anexos sin zona confirmada y no se tratan como seis conversaciones distintas.")
p('Los nombres Local de los pedidos contradicen su sufijo Z. Se interpretó el reloj como México y se marcó la hipótesis en cada entrada, apoyándose en los pares local/UTC de Rider (seis horas) y la hora del pedido KFC del texto de soporte. Esta interpretación debe revisarse si Uber proporciona el diccionario de datos. Los perfiles y comunicaciones sin zona no reciben una hora inventada. El readme exportado solo muestra Loading; no aporta ese diccionario en contenido estático.')
for name in ['Eats/user_orders-0.csv','Rider/rider_lifetime_trips-0.csv','Account and Profile/communications_sent-0.csv','Account and Profile/payment_methods-0.csv']:link('Fuente original '+name,ROOT/name)
link('Paquete local de cruces, filas, estadísticas y límites',OUT/'datos/uber-analytics-cruces.json')
for item in parts:item['uber_extension']=True
structured=[item for item in read('informe-estructurado.json') if not item.get('uber_extension')];structured[3:3]=parts
save('datos/informe-estructurado.json',structured)
md=[]
for item in parts:
    if item['type']=='heading':md.append('## '+item['text'])
    elif item['type']=='link':md.append('['+item['text']+']('+item['url']+')')
    else:md.append(('**'+item['event_id']+'** · ' if item['type']=='evidence' else '')+item['text'])
report='\n\n'.join(md)+'\n';path=OUT/'uber-analytics-cruces.md';path.write_text(report);path.chmod(0o600)
logpath=OUT/'registro.md';log=logpath.read_text();block='<!-- INICIO_RESULTADOS_SESION_8 -->\n## Sesión 8: Uber y cruces de Analytics\n\n'+report+'\n<!-- FIN_RESULTADOS_SESION_8 -->'
if '<!-- INICIO_RESULTADOS_SESION_8 -->' in log:log=re.sub(r'<!-- INICIO_RESULTADOS_SESION_8 -->.*?<!-- FIN_RESULTADOS_SESION_8 -->',lambda _:block,log,flags=re.S)
else:log+='\n\n'+block+'\n'
logpath.write_text(log);logpath.chmod(0o600)
print(json.dumps({'uber_events':sum(e['family']=='Uber' for e in events),'analytic_rows':sum(s['rows'] for s in statistics.values()),'google_analytics_matches':len(ga),'all_temporal_candidates':len(links),'meta_candidates_including_duplicate_views':len(meta),'ids_literal_matches':len(literal_id_matches),'ip_strings_with_matches':len(ip_matches)},ensure_ascii=False))
