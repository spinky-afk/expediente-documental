#!/usr/bin/env python3
"""Añade las pistas sobre metadatos y la secuencia Etsy–Clarín–Hermes."""
import json
import hashlib
import os
import re
from pathlib import Path
from datetime import datetime,timezone
OUT=Path(__file__).resolve().parents[1]
def read(n):return json.loads((OUT/n).read_text())
def write(n,t):
    p=OUT/n;p.write_text(t);os.chmod(p,0o600)
def save(n,j):write(n,json.dumps(j,ensure_ascii=False,indent=2)+'\n')
events=read('datos/actividad-cronologica.json');raw=read('privado/actividad-observaciones-originales.json')
businesses=read('datos/facebook-empresas-identificadores.json')
etsy=next(b for b in businesses if b['name']=='etsy.com');clarin=next(b for b in businesses if b['name']=='clarin.com')
etsy_events=[r for r in events if 'etsy.com' in r['subject']+' '+(r.get('url') or '') or r.get('business_name')=='etsy.com']
related=[r for r in events if r['time_local'].startswith(('2026-09-20','2026-09-21')) and re.search(r'clar[ií]n|herm[eèé]s|inwebo|trustbuilder|6850175308|g\.co/sc|portal\.nousresearch',r['subject']+' '+(r.get('url') or ''),re.I)]
authenticator=[r for r in events if re.search(r'inwebo|trustbuilder',r['subject']+' '+(r.get('url') or ''),re.I)]
numbers=sorted(set([etsy['business_id'],clarin['business_id'],etsy['filename_suffix']]+etsy['event_identifiers']+clarin['event_identifiers']))
matches={n:{'google_observations':[r['id'] for r in raw if r['family']=='Google' and n in json.dumps(r,ensure_ascii=False)],
            'messenger_observations':[r['id'] for r in raw if r['channel']=='Messenger' and n in json.dumps(r,ensure_ascii=False)]} for n in numbers}
focused=sorted({r['id']:r for r in etsy_events+related}.values(),key=lambda r:r['time_utc'])
number_events=[r for r in events if '6850175308' in json.dumps(r,ensure_ascii=False)]
contacts=[];extra_sources=[]
for path in Path('/home/deep-logic/Documentos/Registro/Takeout/Contactos').rglob('*.vcf'):
    data=path.read_bytes();text=data.decode();unfolded=re.sub(r'\r?\n[ \t]','',text)
    if '6850175308' not in unfolded:continue
    code='V'+str(len(extra_sources)+1).zfill(2)
    extra_sources.append({'code':code,'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)})
    for i,block in enumerate(unfolded.split('BEGIN:VCARD')[1:],1):
        if '6850175308' not in block:continue
        fields=[line for line in block.splitlines() if line.startswith(('FN:','N:','TEL','EMAIL'))]
        contacts.append({'source_code':code,'source_path':str(path),'vcard_index_1based':i,'fields':fields})
save('datos/numero-6850175308-evidencias.json',{'events':number_events,'contacts':contacts,'sources':extra_sources,
 'interpretation':'Número buscado antes de Etsy; también guardado como TEL y presente como userId en URLs de Xiaomi. Sin equivalencia demostrada con IDs empresariales de Etsy o Clarín.'})
save('datos/etsy-clarin-hermes-cruce.json',{'created_at_utc':datetime.now(timezone.utc).isoformat(),
 'user_clues':['21 de septiembre, etsi','se envió algo al número de la empresa','ese dato sirve para identificarse con clarin y posteriormente hermes y la cuenta'],
 'matched_name':'etsy.com','etsy':etsy,'clarin':clarin,'number_matches':matches,
 'same_filename_suffix':etsy['filename_suffix']==clarin['filename_suffix'],
 'events':focused,'authenticator_events':authenticator,
 'preceding_number':'6850175308','preceding_number_events':[r['id'] for r in number_events],
 'conclusion':'La secuencia de visitas es comprobable. No se demuestra que un identificador de Etsy autentique en Clarín, Hermès, Hermes Agent o Google.',
 'date_explanation':'20 de septiembre 21:13:29 UTC-06:00 corresponde a 21 de septiembre 03:13:29 UTC.',
 'direction_of_meta_activity':'El export dice actividad recibida por Meta desde etsy.com; no muestra el contenido de un mensaje enviado por el usuario a Etsy.',
 'google_literal_number_search':'Sin coincidencias de estos números en los archivos originales del Takeout, verificado con rg.',
 'limitations':'Sin registros de solicitudes HTTP POST, cookies de sesión ni contenido de Gmail/Chat para probar un alta o inicio de sesión.'})
web=[
 {'id':'P01','title':'Google Fotos: metadatos al exportar',
  'url':'https://support.google.com/photos/answer/3024190?hl=es',
  'status':'contenido verificado','relationship':'Consulta actual; no visita recuperada del historial.',
  'notes':'Distingue la fecha de archivo que puede asignar el sistema al descargar, metadatos originales insertados y datos adicionales en un JSON secundario.'},
 {'id':'P02','title':'Google: medios de una ubicación de Perfil de Negocio',
  'url':'https://developers.google.com/my-business/reference/rest/v4/accounts.locations.media',
  'status':'contenido verificado','relationship':'Consulta actual de API oficial; no prueba una vinculación particular del usuario.',
  'notes':'El recurso MediaItem tiene un nombre con accountId, locationId y mediaKey; la asociación de medios a una ubicación se representa explícitamente.'},
 {'id':'P03','title':'Meta: información de actividad compartida por apps y sitios',
  'url':'https://about.fb.com/news/2019/08/off-facebook-activity/',
  'status':'contenido verificado','relationship':'Consulta actual para interpretar actividad fuera de Meta.',
  'notes':'Los sitios y apps envían información de interacción a Meta mediante herramientas empresariales, que puede asociarse a una cuenta para publicidad. No equivale al texto de un mensaje al comercio.'},
 {'id':'P04','title':'Hermes Agent: pasarela de mensajería y autorizaciones',
  'url':'https://hermes-agent.nousresearch.com/docs/user-guide/messaging',
  'status':'contenido verificado','relationship':'El destino sí aparece en el historial del 20-09-2026 21:44:31; se leyó el contenido actual.',
  'notes':'La pasarela utiliza listas de usuarios autorizados o emparejamiento. Los IDs se interpretan dentro de cada plataforma, sin una equivalencia documentada con IDs de Etsy o Clarín.'},
 {'id':'P05','title':'TrustBuilder Authenticator móvil: QR y activación',
  'url':'https://docs.trustbuilder.com/mfa/trustbuilder-authenticator-mobile-app',
  'status':'contenido verificado','relationship':'Referencia adicional actual; la aplicación y myinwebo.com sí figuran en el historial.',
  'notes':'Permite autenticación mediante QR, notificación u OTP según configuración; para añadir una cuenta requiere un código o QR de activación válido.'},
 {'id':'P06','title':'TrustBuilder: parámetros de la autenticación con QR',
  'url':'https://docs.trustbuilder.com/mfa/web-sdk-qr-code-authentication',
  'status':'contenido verificado','relationship':'Referencia adicional actual; no visita recuperada del historial.',
  'notes':'El SDK usa sessionId, login y serviceId. Son parámetros propios del servicio de autenticación; no se ha encontrado un serviceId del usuario en esta exportación.'},
 {'id':'P07','title':'Google Fotos: información IPTC/IA',
  'url':'https://support.google.com/photos/answer/15532903?hl=en',
  'status':'resultado de búsqueda oficial revisado; apertura en español fallida',
  'relationship':'Consulta adicional; no usada para confirmar asociaciones a negocios.',
  'notes':'El resultado oficial menciona información IPTC editable. La apertura de la variante española devolvió error.'},
 {'id':'P08','title':'Meta: ayuda sobre actividad fuera de Meta',
  'url':'https://www.facebook.com/help/2207256696182627',
  'status':'redirección a inicio de sesión; sin contenido verificado',
  'relationship':'Intento actual; la interpretación se apoya en P03.',
  'notes':'No se usa como evidencia del funcionamiento interno de los identificadores.'},
]
for s in web:s['consulted_on']='2026-10-01'
save('datos/pistas-fuentes-web.json',web)
save('datos/pistas-consultas-web.json',[
 'site.support.google.com/accounts/answer/3024190 photos original metadata additional JSON',
 'site.support.google.com/photos download photo metadata timestamp operating system',
 'site.support.google.com/business photos videos metadata business profile',
 'TrustBuilder Authenticator activation code QR site:trustbuilder.com',
 'activation code QR inwebo site:docs.inwebo.com',
 'TrustBuilder Authenticator com.inwebo.near.prod site:play.google.com'])
new=[]
def h(t):new.append({'type':'heading','text':t})
def p(t):new.append({'type':'paragraph','text':t})
def link(t,url):new.append({'type':'link','text':t,'url':url})
def ev(r):
    new.append({'type':'evidence','event_id':r['id'],'text':f"México {r['time_local']} · UTC {r['time_utc']}\n{r['channel']} · {r['subject']}\n{r['source_code']} · {json.dumps(r['locator'],ensure_ascii=False)}",'url':r.get('url')})
h('Pista del 21 de septiembre: Etsy, Clarín, Hermès y Hermes Agent')
p('Se buscó ETSI/Etsy y Clarín/Hermes con variantes de acentos en los archivos HTML, JSON, CSV y TXT originales. La coincidencia relacionada con esa noche es Etsy (etsy.com). En México el recorrido es del 20 de septiembre, aproximadamente 21:13–23:12; en UTC corresponde al 21. Ejemplo: 20-09 21:13:29 UTC-06 equivale a 21-09 03:13:29 UTC. Se muestran ambas horas para que puedas comparar con tus recuerdos.')
h('Los números de Etsy y Clarín, con su campo exacto')
p('Etsy: Identificador en encabezado = 1594897960568214. Identificadores dentro de eventos = 114623403312281 y 297472060462208. Número de producto visitado en la URL /listing/ = 4303042674. Referencia de entidad: '+etsy['source_code']+'; encabezado de etsycom_105529809654844415.html.')
link('Archivo original: etsy.com',Path(etsy['source_path']).as_uri())
p('Clarín: Identificador en encabezado = 1563990080334439. Identificador dentro de eventos = 455329408009530. Referencia: '+clarin['source_code']+'; encabezado de clarincom_105529809654844415.html.')
link('Archivo original: clarin.com',Path(clarin['source_path']).as_uri())
p('Coincidencia comprobada: los dos nombres de archivo terminan en 105529809654844415. Sus campos de Identificador de entidad y de eventos son diferentes. El export no explica el significado del sufijo; se conserva como un sufijo compartido de archivo. La igualdad no permite concluir que sea un código de acceso, un identificador de persona compartido ni una cuenta unificada.')
h('Número buscado justo antes de Etsy: 6850175308')
p('A las 21:12:50 del 20 de septiembre (03:12:50 UTC del día 21) aparece la consulta 6850175308; 39 segundos después está la visita a Etsy. Referencia Búsqueda #170. También se buscó ese número en Google Chat a las 20:47:22 (Chat #1): ese registro es una búsqueda, no un mensaje enviado. Se había consultado repetidamente el 14 y 15 de septiembre y el día 20 a las 16:11:03.')
for r in number_events:ev(r)
p('El 25 de septiembre aparece el mismo número en el parámetro userId=6850175308 de URLs de account.xiaomi.com. En los contactos figura TEL;TYPE=CELL:+526850175308. Estas son dos representaciones literales distintas; el export no verifica que sea un teléfono activo ni que las fichas identifiquen a un mismo titular. No coincide con los campos Identificador de entidad o de evento de Etsy/Clarín.')
for c in contacts:
    p(f"{c['source_code']} · tarjeta vCard #{c['vcard_index_1based']} · "+' ; '.join(c['fields']))
    link('Contacto original',Path(c['source_path']).as_uri())
p('La interpretación de que este número permite identificarse en Etsy, Clarín o Hermes queda sin comprobar. No se encontró el número en los archivos originales de Facebook. Las URLs de Xiaomi dan una referencia de cuenta mucho más explícita que la proximidad temporal con una visita a Etsy, sin demostrar un inicio de sesión exitoso.')
h('Qué se envió y qué se recibió')
p('El archivo de Etsy enumera nueve registros de actividad recibida con tipos PAGE_VIEW y VIEW_CONTENT, todos del 20 de septiembre. Un resumen reproduce los mismos nueve registros. A las 21:13 aparecen ambos tipos, y a las 21:50 otra PAGE_VIEW. El texto del export dice Recibida el y pertenece a actividad fuera de Meta: no contiene un mensaje enviado a Etsy, su texto, destinatario ni adjunto.')
p('Según Meta, esta sección recoge información que sitios y apps comparten con Meta, susceptible de asociarse a una cuenta para publicidad. Eso respalda la interpretación de un envío de actividad del sitio hacia Meta, sin demostrar que el usuario haya enviado manualmente algo al número de la empresa. [P03]')
link(web[2]['title'],web[2]['url'])
p('Las visitas a Clarín del 20 de septiembre sí aparecen en Google Analytics y Publicidad. En el detalle fuera de Meta de clarin.com, los eventos conservados son del 8 y 28 de agosto; no hay allí un evento del 20/21 de septiembre que una numéricamente Etsy con Clarín.')
h('Secuencia recuperada: visitas, consultas y páginas de cuenta')
anchor_times={'21:12:50','21:13:29','21:13:36','21:18:59','21:32:10','21:36:31','21:40:31','21:42:20','21:44:31','21:47:08',
              '21:48:56','21:49:27','22:56:36','22:58:55','22:59:59','23:01:38','23:07:02','23:36:40'}
selected=[r for r in focused if r['family']=='Google' and r['time_local'].startswith('2026-09-20') and r['time_local'][11:19] in anchor_times]
for r in selected:ev(r)
for r in focused:
    if 'portal.nousresearch.com' in r['subject']+' '+(r.get('url') or ''):ev(r)
p('La visita a postlogin.clarin.com/post-login y las rutas de Hermès /login/ y /account/create/ son hechos del historial. El historial no guarda los formularios enviados ni una confirmación de inicio de sesión o alta, por lo que no prueba qué credencial se introdujo o si funcionó. Tampoco se demuestra que Etsy haya entregado una credencial para esos sitios.')
p('Hermès de hermes.com es la tienda; Hermes Agent de hermes-agent.nousresearch.com es un proyecto de agente de IA. En el historial aparecen ambos. La documentación de mensajería de Hermes Agent fue visitada traducida a las 21:44:31. Su documentación actual usa autorización por usuarios/plataforma o emparejamiento; no describe que un ID empresarial de Etsy o Clarín dé acceso. [P04]')
link(web[3]['title'],web[3]['url'])
p('Ninguno de los seis números empresariales/de evento/sufijo enumerados aparece literalmente en los archivos de Google Takeout. Tampoco aparecen en el texto ni enlaces de los mensajes de Messenger. La hipótesis del usuario de identificarse con el mismo dato queda abierta, pendiente de precisar el número y la cuenta; no se convierte en conclusión. La secuencia cronológica se conserva como relación de navegación, no de autenticación.')
h('Pista adicional para validar con una imagen: inWebo / TrustBuilder')
p('La misma noche hubo búsquedas inwebo authenticator, acceso a myinwebo.com y una primera instalación de TrustBuilder Authenticator a las 21:48:56.266751. El registro de uso de Google Play es de las 23:36:40. Esta es una nueva pista concreta para la consulta anterior sobre validar con una imagen, aunque no se encontró la frase exacta ni un QR de activación personal.')
for r in authenticator:ev(r)
p('La documentación del fabricante describe autenticación mediante QR y activación con código o QR válido. Otra página distingue los parámetros sessionId, login y serviceId de la sesión de autenticación. No se recuperó ese serviceId personal ni se demostró una equivalencia con los números de Etsy. No se ha identificado el método como más rápido en tu caso. [P05, P06]')
for w in web[4:6]:link(w['title'],w['url'])
h('Google Fotos: metadatos diferentes y posible cuenta de negocios')
meta=read('datos/imagenes-metadatos-resumen.json')
p(f"En /home/deep-logic/Documentos se leyeron los metadatos de {meta['images_read']} imágenes: {meta['google_images']} de Takeout y {meta['facebook_images']} de Facebook. No se encontró una carpeta Google Fotos/Google Photos ni archivos JSON complementarios de fotos. Solo una imagen tiene un campo EXIF: Orientation=1 en un sticker. Las demás pueden conservar otros campos de PNG/JPEG, como Software o perfiles de color. Se verificó que no se modificaron los originales.")
p('Se encontraron 57 grupos de imágenes con píxeles idénticos; en todos sus archivos el SHA-256 binario también coincide. En esta copia no se encontró un par con los mismos píxeles y bytes/metadatos distintos. Esto no descarta diferencias en fotos que no estén incluidas aquí. Los archivos de la muestra no permiten comparar un original con su descarga de Google Fotos.')
p('Google distingue tres capas: fecha del archivo que puede cambiar al descargar; metadatos originales dentro de la imagen; información adicional de Google Fotos exportada en JSON. Una diferencia entre esas capas no demuestra por sí sola una vinculación a un negocio. [P01]')
link(web[0]['title'],web[0]['url'])
p('Como ejemplo de evidencia explícita de vinculación, la API de Perfil de Negocio representa medios mediante accounts/{accountId}/locations/{locationId}/media/{mediaKey}. Una ruta de ese tipo, un registro de publicación o el enlace verificable a la misma imagen en una ficha ayudaría a comprobar la asociación. No se encontró esa relación para las imágenes revisadas. La forma de ese recurso no garantiza que aparezca en EXIF o en un export de Google Fotos. [P02]')
link(web[1]['title'],web[1]['url'])
p('La hipótesis de vincular fotos mediante metadatos queda registrada como no comprobada. La comparación futura requiere las dos versiones concretas y sus JSON complementarios, si existen. No se atribuye a negocios el nombre Software=Matplotlib de los archivos IA de Facebook ni un horario de descarga.')
parts=read('datos/informe-estructurado.json')
# Permite ejecutar otra vez sin duplicar el añadido.
parts=[r for r in parts if not r.get('pistas_extension')]
for r in new:r['pistas_extension']=True
parts[3:3]=new;save('datos/informe-estructurado.json',parts)
def markdown(rows):
    blocks=[]
    for r in rows:
        if r['type']=='heading':blocks.append('## '+r['text'])
        elif r['type']=='link':blocks.append(f"[{r['text']}]({r['url']})")
        else:
            blocks.append(('**'+r['event_id']+'** · ' if r['type']=='evidence' else '')+r['text'])
            if r.get('url'):blocks.append(f"[Abrir enlace]({r['url']})")
    return '\n\n'.join(blocks)+'\n'
write('pistas-etsy-clarin-hermes-y-fotos.md',markdown(new))
write('hallazgos-facebook.md',markdown(parts))
log=(OUT/'registro.md').read_text();block='<!-- INICIO_RESULTADOS_SESION_4 -->\n## Sesión 4: pistas aportadas durante la integración\n\n'+markdown(new)+'\n<!-- FIN_RESULTADOS_SESION_4 -->'
if '<!-- INICIO_RESULTADOS_SESION_4 -->' in log:log=re.sub(r'<!-- INICIO_RESULTADOS_SESION_4 -->.*?<!-- FIN_RESULTADOS_SESION_4 -->',lambda _:block,log,flags=re.S)
else:log+='\n\n'+block+'\n'
write('registro.md',log)
print(json.dumps({'focused_events':len(focused),'etsy_observations':len(etsy_events),'new_report_blocks':len(new)},ensure_ascii=False))
