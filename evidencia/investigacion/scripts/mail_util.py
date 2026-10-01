"""Extrae MBOX local con páginas legibles y referencias al original íntegro."""
import email.header
import email.utils
import hashlib
import html
import json
import mailbox
import re
from datetime import timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT=Path(__file__).resolve().parents[1]
MBOX=Path('/home/deep-logic/Documentos/Todo el correo, con Spam y Papelera incluidos.mbox')

def decode_header(value):
    out=[]
    for part,charset in email.header.decode_header(value or ''):
        if isinstance(part,bytes):
            try:part=part.decode(charset or 'utf-8',errors='replace')
            except LookupError:part=part.decode('utf-8',errors='replace')
        out.append(part)
    return re.sub(r'\s+',' ',''.join(out)).strip()

class Text(HTMLParser):
    def __init__(self):super().__init__();self.parts=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ['script','style','head']:self.skip+=1
        elif not self.skip and tag in ['p','br','div','tr','li','h1','h2','h3']:self.parts.append('\n')
    def handle_endtag(self,tag):
        if tag in ['script','style','head'] and self.skip:self.skip-=1
        elif not self.skip and tag in ['p','div','tr','li']:self.parts.append('\n')
    def handle_data(self,text):
        if not self.skip:self.parts.append(text)

def body(message):
    plain=[];rendered=[];attachments=[]
    for part in message.walk():
        if part.is_multipart():continue
        data=part.get_payload(decode=True) or b''
        if part.get_content_disposition()=='attachment' or part.get_filename():
            attachments.append({'filename':decode_header(part.get_filename()),'mime':part.get_content_type(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
            continue
        if part.get_content_type() not in ['text/plain','text/html']:continue
        try:text=data.decode(part.get_content_charset() or 'utf-8',errors='replace')
        except LookupError:text=data.decode('utf-8',errors='replace')
        if part.get_content_type()=='text/plain':plain.append(text)
        else:
            parser=Text();parser.feed(text);rendered.append(''.join(parser.parts))
    return re.sub(r'\n\s*\n\s*\n','\n\n','\n\n'.join(plain or rendered)).strip(),attachments

def safe_text(text):
    # The complete mail, including codes and URLs, remains in the original MBOX.
    def historical_url(match):
        try:host=urlsplit(html.unescape(match[0])).hostname or '[dominio]'
        except ValueError:host='[dominio]'
        return '[URL histórica en '+host+'; consultar original]'
    text=re.sub(r'https?://[^\s<>]+',historical_url,text)
    text=re.sub(r'(?is)-----BEGIN[^\n]*PRIVATE KEY-----.*?-----END[^\n]*PRIVATE KEY-----','[clave privada: consultar original]',text)
    text=re.sub(r'(?i)((?:c[oó]digo(?: de (?:seguridad|verificaci[oó]n))?|code|no compartir|do not share|one.time)[\s\S]{0,160}?)(\b\d{4,8}\b)',r'\1[valor de verificación omitido]',text)
    if re.fullmatch(r'\s*\d{4,8}\s*',text):text='[asunto con código de verificación; consultar original]'
    text=re.sub(r'(?i)(?:password|passwd|contrase[nñ]a)\s*[:=]\s*\S+','[valor privado: consultar original]',text)
    return text

def extract():
    digest=hashlib.sha256(MBOX.read_bytes()).hexdigest()
    cache=ROOT/'privado/correo-mensajes-originales.json'
    if cache.exists():
        saved=json.loads(cache.read_text())
        if saved['source_sha256']==digest:return saved
    box=mailbox.mbox(str(MBOX),create=False)
    records=[];directory=ROOT/'correos';directory.mkdir(exist_ok=True);directory.chmod(0o700)
    for index,message in enumerate(box,1):
        subject=decode_header(message.get('Subject'))
        text,attachments=body(message)
        declared=message.get('Date','');parsed=None
        try:parsed=email.utils.parsedate_to_datetime(declared)
        except (ValueError,TypeError,OverflowError):pass
        if parsed and parsed.tzinfo is None:parsed=None
        identity='M'+str(index).zfill(6)
        record={'id':identity,'mbox_index':index,'message_id':message.get('Message-ID'),'date_header':declared,'time_utc':parsed.astimezone(timezone.utc).isoformat(timespec='microseconds') if parsed else None,'from':decode_header(message.get('From')),'sender_address':email.utils.parseaddr(message.get('From',''))[1],'to':decode_header(message.get('To')),'delivered_to':decode_header(message.get('Delivered-To')),'labels':decode_header(message.get('X-Gmail-Labels')),'subject':subject,'body':text,'received_headers':message.get_all('Received',[]),'attachments':attachments,'public_subject':safe_text(subject),'public_body':safe_text(text),'page':'correos/'+identity+'.html','mime_defects':[str(x) for part in message.walk() for x in part.defects]}
        records.append(record)
        esc=html.escape
        page='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="referrer" content="no-referrer"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'"><title>'+esc(identity+' · '+record['public_subject'])+'</title><style>body{max-width:960px;margin:24px auto;padding:20px;font:16px/1.6 system-ui}pre{white-space:pre-wrap;overflow-wrap:anywhere}code{overflow-wrap:anywhere}</style></head><body><h1>'+esc(record['public_subject'])+'</h1><p>'+esc(identity)+' · registro MBOX '+str(index)+'</p><p>From declarado: '+esc(record['from'])+'<br>To declarado: '+esc(record['to'])+'<br>Date: '+esc(declared)+'<br>Etiquetas: '+esc(record['labels'])+'</p><p>Vista de lectura local. El original íntegro permanece en el MBOX. Esta vista omite valores de verificación y direcciones de acceso, conserva el texto y desactiva contenido remoto. Las cabeceras no se han validado criptográficamente.</p><pre>'+esc(record['public_body'])+'</pre><h2>Adjuntos conservados en el original</h2><pre>'+esc(json.dumps(attachments,ensure_ascii=False,indent=2))+'</pre></body></html>'
        target=directory/(identity+'.html');target.write_text(page);target.chmod(0o600)
    box.close()
    result={'source_path':str(MBOX),'source_bytes':MBOX.stat().st_size,'source_sha256':digest,'messages':records}
    cache.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');cache.chmod(0o600)
    return result

def collect(api):
    if not MBOX.exists():return
    data=extract();api.register(MBOX,'Correo')
    for record in data['messages']:
        dt=__import__('datetime').datetime.fromisoformat(record['time_utc']) if record['time_utc'] else None
        api.event(MBOX,'Correo','MBOX · Cabeceras Date','fecha declarada del correo',
                  'Correo · '+record['sender_address']+' · '+record['public_subject'],dt,
                  {'mbox_message_index_1based':record['mbox_index'],'mail_id':record['id'],'message_id':record['message_id']},
                  text=record['body'],original_date=record['date_header'],
                  identifiers={'mail_id':record['id'],'sender_domain':record['sender_address'].rsplit('@',1)[-1]},
                  body_search=record['public_body'],mail_page=record['page'],
                  timezone_basis='Date de la cabecera, con zona explícita: fecha declarada por el mensaje, sin acreditar lectura, apertura de app ni validación criptográfica del remitente.')
