#!/usr/bin/env python3
"""Comprueba conservación, respaldo, enlaces y sintaxis del sitio preparado."""
import base64
import hashlib
import json
import re
import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT=Path(__file__).resolve().parent
R=ROOT.parent/'vapid-webpush'
S=ROOT/'sitio'
events=json.loads((R/'datos/actividad-cronologica.json').read_text())
sources=json.loads((S/'catalogo-fuentes-local.json').read_text())
manifest=json.loads((S/'manifiesto-originales.json').read_text())
verified=0
for item in manifest:
    if item['encrypted_only']:continue
    p=S/item['archive_path']
    assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],item['archive_path']
    assert hashlib.sha256(Path(item['origin_path']).read_bytes()).hexdigest()==item['sha256'],item['origin_path']
    verified+=1
keys=json.loads((R/'privado/vapid-recuperada.json').read_text())
needles=[keys[k].encode() for k in ['vapid_private_key_der_base64_original','vapid_private_key_raw_base64url']]
leaks=[]
for p in S.rglob('*'):
    if p.is_file():
        b=p.read_bytes()
        if any(n in b for n in needles) or b'-----BEGIN PRIVATE KEY-----' in b or b'-----BEGIN EC PRIVATE KEY-----' in b:leaks.append(str(p))
assert not leaks,leaks
key=base64.urlsafe_b64decode((R/'privado/clave-respaldo-github-local.txt').read_text().strip())
v=json.loads((S/'respaldo-sensible-cifrado.json').read_text())
restored=json.loads(AESGCM(key).decrypt(base64.b64decode(v['nonce_base64']),base64.b64decode(v['ciphertext_base64']),v['aad'].encode()))
assert len(restored['files'])==4
for item in restored['files']:
    b=base64.b64decode(item['data_base64'])
    assert hashlib.sha256(b).hexdigest()==item['sha256']
    assert hashlib.sha256(Path(item['path']).read_bytes()).hexdigest()==item['sha256']

class Links(HTMLParser):
    def __init__(self):super().__init__();self.attrs=[];self.ids=set()
    def handle_starttag(self,t,attrs):
        d=dict(attrs)
        if d.get('id'):self.ids.add(d['id'])
        for k in ['href','src','poster']:
            if d.get(k):self.attrs.append((t,k,d[k]))

external=[];missing=[];cache={};js_checked=0
for p in list((S/'paginas').rglob('*.html'))+list(S.glob('*.html'))+list((S/'investigacion/correos').glob('*.html')):
    parser=Links();text=p.read_text();parser.feed(text);cache[str(p)]=parser
    for tag,k,url in parser.attrs:
        parts=urlsplit(url)
        if parts.scheme in ['http','https','file'] or parts.netloc:external.append((str(p),url[:160]));continue
        if parts.scheme or not parts.path:continue
        target=(p.parent/unquote(parts.path)).resolve()
        if not target.exists():missing.append((str(p),url[:160]))
    if p.parent==S:
        for code in re.findall(r'<script(?:\s[^>]*)?>(.*?)</script>',text,re.S):
            if not code.strip() or code.strip().startswith('{'):continue
            with tempfile.NamedTemporaryFile(suffix='.js',mode='w',encoding='utf-8') as f:
                f.write(code);f.flush();subprocess.run(['node','--check',f.name],check=True,capture_output=True);js_checked+=1
missing_anchors=[];anchor_count=0;by_code={x['code']:x for x in sources}
for e in events:
    loc=e['locator']
    if 'html_line_1based' in loc:
        p=S/unquote(by_code[e['source_code']]['view_local']);anchor='pos-'+str(loc['html_line_1based'])+'-'+str(loc['html_column_0based']);anchor_count+=1
        if anchor not in cache[str(p)].ids:missing_anchors.append(e['id'])
    elif 'csv_line_1based' in loc:
        p=S/unquote(by_code[e['source_code']]['view_local']);anchor='linea-'+str(loc['csv_line_1based']);anchor_count+=1
        if anchor not in cache[str(p)].ids:missing_anchors.append(e['id'])
    elif 'mbox_message_index_1based' in loc:
        p=S/'investigacion/correos'/(loc['mail_id']+'.html') if 'mail_id' in loc else S/'investigacion/correos'/(e['identifiers']['mail_id']+'.html')
        anchor_count+=1
        if not p.exists():missing_anchors.append(e['id'])
pdf=(S/'historial-cruzado.pdf').read_bytes();uris=re.findall(rb'/URI\s*\((.*?)\)',pdf)
external_pdf=[u[:140].decode(errors='replace') for u in uris if u.startswith((b'https:',b'http:',b'file:'))]
report={'original_copies_verified':verified,'encrypted_files_restored_in_memory':len(restored['files']),'private_key_leaks':leaks,'external_navigation_in_site_pages':external[:20],'missing_local_links':missing[:30],'anchored_observations':anchor_count,'missing_anchors_count':len(missing_anchors),'missing_anchor_samples':missing_anchors[:10],'javascript_blocks_checked':js_checked,'pdf_link_annotations':len(uris),'pdf_external_or_machine_specific_links':external_pdf,'account':json.loads((ROOT/'estado-publicacion.json').read_text())}
(S/'verificacion-sitio.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False),flush=True)
assert not external,external[:5]
assert not missing,missing[:5]
assert not missing_anchors,missing_anchors[:5]
assert not external_pdf,external_pdf[:5]
