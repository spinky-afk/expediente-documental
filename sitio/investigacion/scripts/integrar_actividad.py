#!/usr/bin/env python3
"""Integra actividad local, conserva procedencia y relaciona identificadores."""
import bisect
import csv
import hashlib
import importlib.util
import json
import os
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlencode, urlsplit, urlunsplit
from zoneinfo import ZoneInfo
from facebook_util import Document, Node, facebook_date

OUT = Path(__file__).resolve().parents[1]
FB = Path('/home/deep-logic/Documentos/facebook')
spec = importlib.util.spec_from_file_location('extraer', OUT / 'scripts/extraer.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
ZONE = ZoneInfo('America/Mexico_City')
sources = {}
raw_events = []
undated = []
messages = []
businesses = []
off_events = []
page_ids = []
file_entries = []
id_occurrences = defaultdict(list)
fb_google_mentions = []


def save(name, obj):
    p = OUT / name
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n' if not isinstance(obj, str) else obj, encoding='utf-8')
    os.chmod(p, 0o600)


def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD',s.lower()) if unicodedata.category(c)!='Mn')


def register(path, family):
    path=Path(path);key=str(path)
    if key not in sources:
        data=path.read_bytes()
        sources[key]={'code':f'S{len(sources)+1:03}', 'path':key, 'family':family,
                      'sha256':hashlib.sha256(data).hexdigest(), 'bytes':len(data), 'records':0}
    return sources[key]['code']


def safe_url(s, depth=0):
    if not s:return None
    s=m.canonical(s)
    u=urlsplit(s)
    if u.scheme not in ('http','https'):
        return None
    if u.hostname in ('accounts.google.com','login.yahoo.com'):
        return urlunsplit((u.scheme,u.netloc,u.path,'',''))
    forbidden=re.compile(r'^(?:password|passwd|pass|secret|token|session_token|instance_id_token|access_token|refresh_token|id_token|code|auth|authkey|key|api_key|signature|sig|rapt|rart|TL|dsh|usg|sjid|visit_id|search_session_id|js_request_id|omec|fbclid)$',re.I)
    params=[]
    for k,values in parse_qs(u.query,keep_blank_values=True).items():
        if forbidden.match(k) or k.startswith(('utm_','gad_','gclid','gbraid','wbraid')):continue
        for v in values:
            if v.startswith(('http://','https://')):
                v=safe_url(v,depth+1) if depth<4 else urlunsplit((*urlsplit(v)[:3],'',''))
            params.append((k,v))
    return urlunsplit((u.scheme,u.netloc,u.path,urlencode(params),u.fragment))


def safe_text(s):
    s=re.sub(r'https?://[^\s<>]+',lambda x:safe_url(x.group(0)) or '[enlace en evidencia original]',s)
    s=re.sub(r'(?i)(?:vapid_private_key|private_key|password|passwd)\s*[=:]\s*["\']?[^\s,}"\']+', '[valor privado: consultar evidencia original]',s)
    return s


def event(path, family, channel, kind, subject, dt, locator, url=None, text=None,
          original_date=None, precision='segundo', identifiers=None, **extra):
    code=register(path,family)
    sources[str(path)]['records']+=1
    r={'source_code':code,'source_path':str(path),'family':family,'channel':channel,'kind':kind,
       'subject':subject,'url_original':url,'url_public':safe_url(url), 'text_original':text,
       'date_original':original_date,'time_precision':precision,'locator':locator,
       'time_utc':dt.astimezone(timezone.utc).isoformat(timespec='microseconds') if dt else None,
       'time_local':dt.astimezone(ZONE).isoformat(timespec='microseconds') if dt else None,
       'identifiers':identifiers or {}, **extra}
    if dt:raw_events.append(r)
    else:undated.append(r)
    return r


def google_kind(action):
    if action.startswith(('Buscaste','Has buscado')):return 'consulta'
    if action.startswith('Has visitado'):return 'visita'
    if action.startswith('Hiciste la petición'):return 'petición'
    if 'búsqueda con' in action:return 'búsqueda visual'
    if action.startswith(('Se ha utilizado','Has utilizado','Has usado','Usaste')):return 'uso de app'
    if action.startswith('Has visto'):return 'video visto'
    return 'actividad'


def collect_google():
    for path in sorted((m.ROOT/'Mi actividad').glob('*/MiActividad.html')):
        parser=m.Activity(str(path.relative_to(m.ROOT)));parser.feed(path.read_text())
        channel=path.parent.name
        for r in parser.records:
            dt=datetime.fromisoformat(r['time_utc']) if r['time_utc'] else None
            subject=r['title_or_query']
            if google_kind(r['action'])=='petición':
                head=r['text_original'].split(r['date_original'] or '\0',1)[0].splitlines()[1:]
                subject=re.sub(r'^Hiciste la petición\s*','','\n'.join(head)).strip()
            event(path,'Google',channel,google_kind(r['action']),subject,dt,
                  {'record_index_1based':r['record_index_1based'],'html_line_1based':r['html_line_1based'],
                   'html_column_0based':r['html_column_0based']},r.get('url_original'),r['text_original'],r['date_original'])
    path=m.ROOT/'Chrome/Historial.json'
    h=json.loads(path.read_text())
    for i,r in enumerate(h['Browser History'],1):
        dt=datetime(1970,1,1,tzinfo=timezone.utc)+timedelta(microseconds=int(r['time_usec']))
        event(path,'Google','Historial de Chrome','visita',r.get('title') or r['url'],dt,
              {'record_index_1based':i,'json_pointer':f'/Browser History/{i-1}'},r['url'],
              original_date=str(r['time_usec']),precision='microsegundo')


def row_locator(node,index,label='table_index_1based'):
    return {label:index,'html_line_1based':node.pos[0],'html_column_0based':node.pos[1]}


def collect_google_structured():
    """Fechas explícitas de Play y otros productos; no infiere usos desde inventarios."""
    stamp_re=re.compile(r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}')
    def parse_stamp(value):
        if not isinstance(value,str) or not stamp_re.match(value):return None
        try:
            dt=datetime.fromisoformat(value.replace(' UTC','+00:00').replace('Z','+00:00'))
            return dt if dt.tzinfo else None
        except ValueError:return None
    def walk(obj,path,pointer='',context='',links=None):
        links=links or []
        if isinstance(obj,dict):
            doc=obj.get('doc',{})
            title=doc.get('title') if isinstance(doc,dict) else None
            title=title or obj.get('title') or obj.get('accountName') or obj.get('prompt') or obj.get('modelName')
            if title:context=str(title)
            elif isinstance(obj.get('text'),list):
                texts=[x.get('data','') for x in obj['text'] if isinstance(x,dict)]
                if texts:context='\n'.join(texts)
            if isinstance(obj.get('citations'),list):links=[x.get('url') for x in obj['citations'] if x.get('url')]
            for k,v in obj.items():
                ptr=pointer+'/'+k.replace('~','~0').replace('/','~1')
                dt=parse_stamp(v)
                if k in ('createdTimestampUsec','userEditedTimestampUsec') and isinstance(v,int):
                    dt=datetime(1970,1,1,tzinfo=timezone.utc)+timedelta(microseconds=v)
                if dt:
                    channel=path.relative_to(m.ROOT).parts[0].replace('\xa0',' ')
                    field_kind='vencimiento registrado' if k=='expirationDate' else 'fecha de '+k
                    suffix=' · '+context if context else ''
                    event(path,'Google',channel+' · '+path.stem,field_kind,path.stem+' · '+k+suffix,dt,
                          {'json_pointer':ptr},links[0] if links else None,original_date=str(v),
                          precision='fracción de segundo' if '.' in str(v) else 'segundo',attachment_links=links)
                elif isinstance(v,(dict,list)):walk(v,path,ptr,context,links)
        elif isinstance(obj,list):
            for i,v in enumerate(obj):walk(v,path,pointer+'/'+str(i),context,links)
    for path in sorted(m.ROOT.rglob('*.json')):
        # Chrome ya tiene su extracción específica; la configuración incluye claves privadas.
        if path.relative_to(m.ROOT).parts[0]=='Chrome':continue
        register(path,'Google')
        try:obj=json.loads(path.read_text())
        except json.JSONDecodeError:
            sources[str(path)]['parse_note']='JSON vacío o no válido; sin registros cronológicos extraídos'
            continue
        walk(obj,path)
    for path in sorted((m.ROOT/'Gemini en Workspace').rglob('*.txt')):
        register(path,'Google');walk(json.loads(path.read_text()),path)
    for path in sorted(m.ROOT.rglob('*.csv')):
        if not path.read_text().strip():continue
        register(path,'Google')
        with path.open(newline='') as f:
            reader=csv.DictReader(f)
            for i,row in enumerate(reader,1):
                for key,val in row.items():
                    if not val or not isinstance(val,str):continue
                    matches=list(re.finditer(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z| UTC|[+-]\d{2}:\d{2})',val))
                    if key=='Hora' and not matches:
                        original,dt=m.html_date(val)
                        precision='segundo';basis='zona explícita en fuente'
                        if dt is None:
                            short=re.search(r'(\d{1,2})\s+([a-z]+)\s+(\d{4}),\s*(\d{1,2}):(\d{2})\s*([ap])\.?m\.?',val.replace('\u202f',' ').replace('\xa0',' '),re.I)
                            if short:
                                day,month,year,hour,minute,ap=short.groups()
                                dt=datetime(int(year),m.MONTHS[month.lower()],int(day),int(hour)%12+(12 if ap.lower()=='p' else 0),int(minute),tzinfo=ZONE)
                                precision='minuto';basis='zona asumida America/Mexico_City; CSV no la especifica'
                        if dt:
                            event(path,'Google',path.relative_to(m.ROOT).parts[0].replace('\xa0',' '),'transacción',
                                  row.get('Descripción') or path.stem,dt,{'csv_record_index_1based':i,'column':key},
                                  text=json.dumps(row,ensure_ascii=False),original_date=val,precision=precision,timezone_basis=basis)
                    for match in matches:
                        dt=parse_stamp(match.group(0))
                        if not dt:continue
                        channel=path.relative_to(m.ROOT).parts[0].replace('\xa0',' ')
                        label=row.get('Marketing Name') or row.get('Meeting Code') or path.stem
                        event(path,'Google',channel,'fecha de '+str(key),label+' · '+str(key),dt,
                              {'csv_record_index_1based':i,'column':key,'character_offset':match.start()},
                              text=json.dumps(row,ensure_ascii=False),original_date=match.group(0))


def collect_facebook():
    for path in sorted(FB.rglob('*.html')):
        register(path,'Facebook')
        rel=str(path.relative_to(FB));doc=Document(path.read_text());title=doc.title
        visible=unquote(unquote(doc.root.clean()))
        linktext=unquote(unquote('\n'.join(u for u,t,pos in doc.links)))
        for number in set(re.findall(r'(?<![A-Za-z0-9])\d{12,22}(?![A-Za-z0-9])',visible+'\n'+linktext)):
            id_occurrences[number].append({'source_path':str(path),'source_code':sources[str(path)]['code']})
        if re.search(r'google',visible+'\n'+linktext,re.I):
            snippets=[visible[max(0,x.start()-80):x.end()+160] for x in list(re.finditer('google',visible,re.I))[:12]]
            fb_google_mentions.append({'source_path':str(path),'source_code':sources[str(path)]['code'],
                                       'title':title,'snippets':snippets})
        tables=list(doc.tables())
        is_off='/your_activity_off_meta_technologies/' in '/'+rel
        is_message='/messages/inbox/' in '/'+rel
        if is_off:
            first=next((rows for node,rows in tables if 'Identificador' in rows and 'Evento' not in rows),{})
            bid=first.get('Identificador')
            if bid:
                name=title
                b={'name':name,'business_id':bid,'event_identifiers':sorted(set(t['Identificador'] for n,t in tables if 'Evento' in t and 'Identificador' in t)),
                   'filename_suffix':re.search(r'_(\d+)\.html$',path.name).group(1),
                   'source_path':str(path),'source_code':sources[str(path)]['code']}
                businesses.append(b)
            else:
                found=re.search(r'Actividad recibida de ([^\n]+)',visible)
                name=found.group(1) if found else title
            for i,(node,rows) in enumerate(tables,1):
                if not ('Evento' in rows and 'Identificador' in rows):continue
                stamp=rows.get('Recibida el','');dt=facebook_date(stamp)
                precision='segundo' if re.search(r'\d+:\d+:\d+',stamp) else 'minuto'
                item=event(path,'Facebook','Actividad fuera de Meta','evento recibido',
                    f'{name} · {rows["Evento"]} · identificador de evento {rows["Identificador"]}',dt,
                    row_locator(node,i),text=json.dumps(rows,ensure_ascii=False),original_date=stamp,precision=precision,
                    identifiers={'business_id':bid,'event_identificador':rows['Identificador']},
                    business_name=name,representation='named' if bid else 'summary',event_type=rows['Evento'])
                off_events.append(item)
            continue
        if is_message:
            suffix=path.parent.name.rsplit('_',1)[-1]
            for i,node in enumerate((n for n in doc.root.nodes('section') if n.has_class('_a6-g')),1):
                footer=next((n for n in node.children if isinstance(n,Node) and n.tag=='footer'),None)
                body=next((n for n in node.children if isinstance(n,Node) and n.has_class('_a6-p')),None)
                sender=node.find('h2');stamp=footer.clean() if footer else '';dt=facebook_date(stamp)
                bodytext=body.clean() if body else ''
                loc=row_locator(node,i,'message_index_1based')
                explicit_ids=[]
                decoded=unquote(unquote(bodytext))
                for key,number in re.findall(r'\b([a-z_]*(?:id)[a-z_]*)["\s:=]+(\d{8,22})',decoded,re.I):
                    explicit_ids.append({'field':key,'value':number})
                    if key=='page_id':page_ids.append({'thread':title,'page_id':number,'time_local':dt.isoformat() if dt else None,
                                                      'source_path':str(path),'source_code':sources[str(path)]['code'],'locator':loc,'text':bodytext})
                urls=list(dict.fromkeys([n.attrs['href'] for n in node.nodes('a') if n.attrs.get('href')]+re.findall(r'https?://[^\s<>]+',bodytext)))
                remote=next((u for u in urls if u.startswith(('http://','https://'))),None)
                item=event(path,'Facebook','Messenger','mensaje',
                    f'{title} · {sender.clean() if sender else "sin remitente"}: {bodytext or "[adjunto o mensaje sin texto]"}',
                    dt,loc,remote,bodytext,stamp,identifiers={'folder_suffix':suffix,'explicit_fields':explicit_ids},
                    thread=title,sender=sender.clean() if sender else None,attachment_links=urls)
                messages.append(item)
            continue
        if rel=='your_facebook_activity/ai/your_files.html':
            for i,(node,rows) in enumerate(tables,1):
                if 'Creado el' not in rows or 'Archivo' not in rows:continue
                dt=facebook_date(rows['Creado el']);links=[n.attrs['href'] for n in node.nodes('a') if n.attrs.get('href')]
                for target in links:
                    p=FB/target
                    item=event(path,'Facebook','Archivos de IA','archivo creado',f'Archivo de IA: {target}',dt,
                               row_locator(node,i),text=json.dumps(rows,ensure_ascii=False),original_date=rows['Creado el'],
                               identifiers={'asset_id':Path(target).name},attachment_links=[target])
                    file_entries.append({'path':str(p),'reference_source':str(path),'locator':item['locator'],
                                         'time_local':item['time_local'],'asset_id':Path(target).name})
            continue
        # Otras secciones fechadas: solo la fecha propia del pie de cada registro.
        for i,node in enumerate((n for n in doc.root.nodes('section') if n.has_class('_a6-g')),1):
            footer=next((n for n in node.children if isinstance(n,Node) and n.tag=='footer'),None)
            if footer is None:continue
            stamp=footer.clean();dt=facebook_date(stamp)
            if dt is None:continue
            heading=node.find('h2');body=next((n for n in node.children if isinstance(n,Node) and n.has_class('_a6-p')),None)
            bodytext=body.clean() if body else ''
            kind='registro';metadata={}
            if rel=='logged_information/recommendations/recent_audio_browser_clicks.html':
                # El pie incluye fechas anómalas, incluso 1902. La fecha etiquetada
                # de actualización no demuestra el momento en que se hizo clic.
                match=re.search(r'Fecha de actualización\s*\n([^\n]+)',bodytext)
                metadata={'footer_date_original':stamp,'date_selection':'Fecha de actualización; pie ambiguo conservado'}
                if match:stamp=match.group(1);dt=facebook_date(stamp);kind='actualización de registro musical'
            all_urls=list(dict.fromkeys([n.attrs['href'] for n in node.nodes('a') if n.attrs.get('href')]+re.findall(r'https?://[^\s<>]+',bodytext)))
            urls=[u for u in all_urls if u.startswith(('http://','https://'))]
            event(path,'Facebook',title or path.parent.name,kind,
                  f'{heading.clean()+": " if heading else ""}{bodytext or title}',dt,
                  row_locator(node,i,'section_index_1based'),url=urls[0] if urls else None,text=bodytext,original_date=stamp,
                  attachment_links=all_urls,**metadata)


def collect_device_and_game_records():
    """Fechas explícitas antes omitidas de HTML Android/Juegos y Chrome Device Info.

    Se llama después de Facebook para conservar los códigos S de fuentes anteriores.
    Los IDs E se vuelven a asignar al ordenar esta nueva versión.
    """
    def date(value):
        value=value.replace('\u202f',' ').replace('\xa0',' ').strip()
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}T[^ ]+(?:Z|[+-]\d{2}:\d{2})',value):
            return datetime.fromisoformat(value.replace('Z','+00:00'))
        _,dt=m.html_date(value)
        if dt:return dt
        long=re.fullmatch(r'(\d{1,2}) de ([a-záéíóú]+) de (\d{4}) a las (\d{1,2}:\d{2}:\d{2})\s*([ap])\.?\s*m\.?\s*UTC',value,re.I)
        if long:
            day,month,year,clock,ap=long.groups()
            mon={'septiembre':'sept','enero':'ene','febrero':'feb','marzo':'mar','abril':'abr','mayo':'may','junio':'jun','julio':'jul','agosto':'ago','octubre':'oct','noviembre':'nov','diciembre':'dic'}.get(month.lower(),month)
            return m.html_date(f'{day} {mon} {year}, {clock} {ap}.m. UTC')[1]
    paths=sorted((m.ROOT/'Servicio de configuración de dispositivos Android').glob('*.html'))+sorted((m.ROOT/'Servicios de juego de Google Play').rglob('*.html'))
    for path in paths:
        doc=Document(path.read_text());text=doc.root.clean();is_device=path.parent.name=='Servicio de configuración de dispositivos Android'
        channel='Configuración de dispositivos Android' if is_device else 'Servicios de juego de Google Play'
        register(path,'Google');identifiers={}
        if is_device:
            for field,key in [('ID de Android','android_configuration_id'),('Modelo','model')]:
                match=re.search(r'^'+re.escape(field)+r':\s*(.*)$',text,re.M)
                if match:identifiers[key]=match[1]
            raw=path.read_text()
            for field in ['Hora del registro','Hora de la primera conexión de datos','Hora de la última conexión de datos']:
                match=re.search(re.escape(field)+r':\s*([^<]+)(<br\s*/?>)',raw,re.I)
                if not match:continue
                dt=date(match[1])
                if not dt:continue
                # Ancla en el br que sigue al campo original, sin alterar su texto.
                off=match.start(2);line=raw.count('\n',0,off)+1;col=off-(raw.rfind('\n',0,off)+1)
                event(path,'Google',channel,'campo de dispositivo',f"{field} · Android {identifiers.get('android_configuration_id')} · modelo {identifiers.get('model')}",dt,
                      {'field':field,'html_line_1based':line,'html_column_0based':col},original_date=match[1],identifiers=identifiers)
        heading='';table_index=0
        for node in doc.root.nodes():
            if node.tag in ('h2','h3'):heading=node.clean()
            if node.tag!='table':continue
            table_index+=1;headers=[];rows=[n for n in node.children if isinstance(n,Node) and n.tag=='tr']
            for row_index,row in enumerate(rows,1):
                cells=[c for c in row.children if isinstance(c,Node) and c.tag in ('td','th')]
                if cells and all(c.tag=='th' for c in cells):headers=[c.clean() for c in cells];continue
                values=[c.clean() for c in cells]
                for ci,cell in enumerate(cells):
                    if any(True for _ in cell.nodes('table')):continue
                    dt=date(values[ci])
                    if not dt:continue
                    field=headers[ci] if ci<len(headers) else 'fecha'
                    if len(values)==2 and ci==1:field=values[0]
                    subject=f'{path.stem} · {heading} · {field}'
                    if is_device:subject=f'Conexión de configuración Android · {identifiers.get("android_configuration_id")} · {heading}'
                    elif values and ci>0:subject+=' · '+values[0]
                    event(path,'Google',channel,'conexión de configuración registrada' if is_device else 'campo de juego',subject,dt,
                          {'table_index_1based':table_index,'row_index_1based':row_index,'column':field,'html_line_1based':row.pos[0],'html_column_0based':row.pos[1]},
                          text=json.dumps(dict(zip(headers,values)) if len(headers)==len(values) else values,ensure_ascii=False),original_date=values[ci],identifiers=identifiers)
    path=m.ROOT/'Chrome/Información del dispositivo.json';obj=json.loads(path.read_text())
    for i,device in enumerate(obj.get('Device Info',[])):
        stamp=device.get('last_updated_timestamp')
        if not isinstance(stamp,int):continue
        dt=datetime(1970,1,1,tzinfo=timezone.utc)+timedelta(milliseconds=stamp)
        event(path,'Google','Chrome · información de dispositivos','actualización del registro de sincronización',f"Registro de Chrome {i+1} · {device.get('client_name','')} · {device.get('chrome_version',device.get('google_play_services_version_info',{}).get('apk_version_name',''))}",dt,
              {'json_pointer':f'/Device Info/{i}/last_updated_timestamp'},original_date=str(stamp),precision='milisegundo',
              identifiers={'model':device.get('model'),'cache_guid':device.get('cache_guid')})


def finish():
    raw_events.sort(key=lambda r:(r['time_utc'],r['source_code'],json.dumps(r['locator'],sort_keys=True)))
    for i,r in enumerate(raw_events,1):r['id']=f'E{i:06}'
    for i,r in enumerate(undated,1):r['id']=f'U{i:06}'
    assets=[];linked={r['path']:r for r in file_entries}
    for p in sorted((FB/'files').iterdir()):
        if not p.is_file():continue
        b=p.read_bytes()
        kind='PNG' if b.startswith(b'\x89PNG\r\n\x1a\n') else 'JPEG' if b.startswith(b'\xff\xd8\xff') else 'otro'
        assets.append({'path':str(p),'name':p.name,'format':kind,'bytes':len(b),
                       'sha256':hashlib.sha256(b).hexdigest(),'matplotlib_metadata':b'Matplotlib' in b,
                       'reference':linked.get(str(p))})
    target_ids={b['business_id'] for b in businesses}|{n for b in businesses for n in b['event_identifiers']}
    matches=[{'identifier':n,'occurrences':id_occurrences[n]} for n in sorted(target_ids)
             if any('/messages/' in x['source_path'] for x in id_occurrences[n])]
    shared=defaultdict(set)
    for b in businesses:
        for n in b['event_identifiers']:shared[n].add((b['name'],b['business_id']))
    shared=[{'event_identificador':n,'businesses':[{'name':name,'business_id':bid} for name,bid in sorted(names)]}
            for n,names in sorted(shared.items()) if len(names)>1]
    # Igualdad de URL y proximidad temporal: vínculo sugerido, conservando cada observación.
    google=[r for r in raw_events if r['family']=='Google' and r['url_public'] and r['kind']=='visita']
    by_url=defaultdict(list)
    for r in google:by_url[r['url_public']].append(r)
    correlations=[]
    for url,rows in by_url.items():
        for i,r in enumerate(rows):
            for s in rows[i+1:]:
                delta=(datetime.fromisoformat(s['time_utc'])-datetime.fromisoformat(r['time_utc'])).total_seconds()
                if delta>2:break
                if r['source_code']!=s['source_code']:
                    correlations.append({'type':'misma URL; diferencia de hasta 2 segundos; posible misma visita',
                                         'event_ids':[r['id'],s['id']],'seconds':delta,'url':url})
    fb_groups=defaultdict(list)
    for r in off_events:
        if not r['time_local']:continue
        k=(norm(r['business_name']),r['identifiers']['event_identificador'],r['event_type'],r['time_local'][:16])
        fb_groups[k].append(r)
    for rows in fb_groups.values():
        if len({r['representation'] for r in rows})>1:
            correlations.append({'type':'Meta: detalle y resumen del mismo nombre, evento, identificador y minuto',
                                 'event_ids':[r['id'] for r in rows]})
    package='com.coppel.coppelapp'
    coppel=[r for r in raw_events if package in (r.get('text_original') or '')+' '+(r.get('url_original') or '')+' '+r['subject']]
    epazote=[r for r in messages if 'epazote' in norm(r.get('thread','')) and any(t in norm(r['subject']) for t in ['google','confirmar pago'])]
    profile=[r for r in raw_events if r['family']=='Google' and
             (r['channel']=='Perfil de Empresa en Google' or 'business.google.' in (r.get('url_public') or '') or
              'perfil negocios google' in norm(r['subject']))]
    dated_counts=Counter((r['family'],r['channel']) for r in raw_events)
    summary={'generated_at_utc':datetime.now(timezone.utc).isoformat(),'timezone':str(ZONE),
             'dated_observations':len(raw_events),'undated_observations':len(undated),
             'earliest':raw_events[0]['time_local'],'latest':raw_events[-1]['time_local'],
             'source_files':len(sources),'source_counts':[{'family':f,'channel':c,'count':v} for (f,c),v in sorted(dated_counts.items())],
             'conversation_files':len({r['source_path'] for r in messages}),
             'conversation_distinct_titles':len({r['thread'] for r in messages}),
             'messages_dated':sum(bool(r['time_utc']) for r in messages),'message_sections_undated':sum(not r['time_utc'] for r in messages),
             'businesses':len(businesses),'business_event_id_matches_in_messages':len(matches),
             'files':len(assets),'files_linked_from_ai':sum(bool(a['reference']) for a in assets),
             'files_formats':dict(Counter(a['format'] for a in assets)),
             'correlations':len(correlations),'google_mentions_facebook':fb_google_mentions,
             'page_ids':page_ids,'coppel_event_ids':[r['id'] for r in coppel],
             'epazote_event_ids':[r['id'] for r in epazote],'google_business_event_ids':[r['id'] for r in profile]}
    save('privado/actividad-observaciones-originales.json',raw_events)
    save('privado/actividad-sin-fecha-original.json',undated)
    public=[]
    for r in raw_events:
        p={k:r[k] for k in ['id','family','channel','kind','time_utc','time_local','time_precision',
                            'date_original','source_code','source_path','locator','identifiers']}
        p.update(subject=safe_text(r['subject']),url=r['url_public'])
        for key in ['thread','sender','business_name','representation','event_type','footer_date_original','date_selection','timezone_basis']:
            if key in r:p[key]=r[key]
        # Solo vínculos a adjuntos locales o direcciones web depuradas.
        if 'attachment_links' in r:
            p['attachment_links']=[safe_url(u) if u.startswith(('http:','https:')) else u for u in r['attachment_links']
                                   if not u.startswith('fb-messenger:')]
        public.append(p)
    save('datos/actividad-cronologica.json',public)
    save('datos/actividad-resumen.json',summary)
    save('datos/catalogo-fuentes.json',list(sources.values()))
    save('datos/facebook-empresas-identificadores.json',businesses)
    save('datos/facebook-identificadores-compartidos.json',shared)
    save('datos/facebook-identificadores-en-mensajes.json',matches)
    save('datos/facebook-files-inventario.json',assets)
    save('datos/actividad-correlaciones.json',correlations)
    csvpath=OUT/'actividad-cronologica.csv'
    with csvpath.open('w',encoding='utf-8-sig',newline='') as f:
        fields=['id','time_local','time_utc','family','channel','kind','subject','url','source_code','source_path','locator','identifiers','time_precision']
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in public:w.writerow({k:json.dumps(r[k],ensure_ascii=False) if isinstance(r.get(k),dict) else r.get(k) for k in fields})
    os.chmod(csvpath,0o600)
    # Comprobación de inmutabilidad sobre las fuentes que se consultaron.
    changed=[s['path'] for s in sources.values() if hashlib.sha256(Path(s['path']).read_bytes()).hexdigest()!=s['sha256']]
    if changed:raise RuntimeError('Fuentes modificadas: '+repr(changed))
    save('datos/verificacion-integracion.json',{'sorted_by_utc':all(a['time_utc']<=b['time_utc'] for a,b in zip(public,public[1:])),
         'unique_observation_ids':len({r['id'] for r in public})==len(public),
         'original_sources_unchanged':not changed,'ai_references_resolve':all(Path(r['path']).is_file() for r in file_entries),
         'business_count':len(businesses),'dated':len(public),'undated':len(undated)})
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__=='__main__':
    collect_google()
    collect_google_structured()
    collect_facebook()
    collect_device_and_game_records()
    finish()
