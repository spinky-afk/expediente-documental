#!/usr/bin/env python3
"""Archivo privado y sitio portátil; nunca publica ni habilita GitHub Pages."""
import argparse
import base64
import hashlib
import html
import importlib.util
import json
import os
import re
import shutil
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

RESEARCH = Path(__file__).resolve().parents[1]
ROOT = RESEARCH.parent / 'expediente-documental'
SITE = ROOT / 'sitio'
ORIGINS = {'google': Path('/home/deep-logic/Documentos/Registro/Takeout'),
           'facebook': Path('/home/deep-logic/Documentos/facebook'),
           'uber': Path('/home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data')}
ORIGINS['mail']=Path('/home/deep-logic/Documentos/Todo el correo, con Spam y Papelera incluidos.mbox')
PRIVATE_NAMES = {'vapid-recuperada.json', 'claves-recuperadas.md', 'vapid-private.pem',
                 'clave-respaldo-github-local.txt'}
SECRET_CONFIG = ORIGINS['google'] / 'Chrome/Configuración.json'
NOW = datetime.now(timezone.utc).isoformat()

LETTER = '''Hola Rocio1 Rocio2 perdon por el acronimo no tengo mucho tiempo, Mane, Sandro, Denisse, Ahora mismo son las personas en quien mas confio, me encuentro en una situacion de vida o muerte, la persona que pense que habia conocido resulto ser parte de una organizacion criminal multinacional, que roba tarjetas de credito, clono mis datos, clono mi voz, y tienen programas para hacer prestamos en cientos de apps tienen mis comprobantes de domicilio e ingresos, tienen aplicaciones de todo tipo infectaron mis sistemas, android linux, windows, la tv, mis memorias, mis cuentas, no es que sean muy inteligentes o tal vez si, pero yo tambien lo soy, asi que ahora mismo trato de reunir la mayor evidencia que pueda. Si algo me pasara lleven toda esta documentacion con la policia cibernetica, yo estare actualizando diario o cuando pueda, si notan que ya no subo nada o me dejo de comunicar en mucho tiempo contactenme, y si ven algo extrano o que no les contesto lleven toda esta evidencia a la policia cibernetica, de momento me encuentro bien, estoy asustado pero tambien inspirado. No puedo regresar con nadie por que temo por ellos, es lo unico que puedo decir de momento. Te quiero hermano, y amigos....'''

def esc(s): return html.escape(str(s), quote=True)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')
    p.chmod(0o600)
def json_write(p, data): write(p, json.dumps(data, ensure_ascii=False, indent=2) + '\n')
def embedded(data): return json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
def read(name): return json.loads((RESEARCH / 'datos' / name).read_text())
def origin_path(p):
    p = Path(p)
    for key, root in ORIGINS.items():
        if root.is_file() and p==root:return Path(key)/p.name
        if p.is_relative_to(root): return Path(key) / p.relative_to(root)
    return None
def href(p): return '/'.join(quote(x, safe='') for x in Path(p).parts)

CSS = '''*{box-sizing:border-box}body{margin:0;background:#f3f5f8;color:#203044;font:16px/1.6 system-ui,sans-serif}header{background:#163747;color:#fff;padding:28px max(22px,calc((100% - 1120px)/2))}header a{color:#d0efff}nav{display:flex;gap:20px;flex-wrap:wrap}main{max-width:1120px;margin:auto;padding:28px 22px 50px}h1{font-size:clamp(26px,4vw,40px);line-height:1.2;margin:10px 0 20px}h2{font-size:23px;margin:30px 0 12px}a{color:#116486;overflow-wrap:anywhere}p{margin:12px 0}.note,.meta{font-size:14px;color:#546575}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:16px}.card,.panel{background:white;border:1px solid #dce2e8;border-radius:12px;padding:22px;margin:12px 0}.card h2{margin-top:0}.number{font-size:34px;color:#116486;font-weight:700}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f8fafc;padding:16px;font:13px/1.6 ui-monospace,monospace}.letter{white-space:pre-wrap;font:18px/1.8 Georgia,serif;border-left:4px solid #37899c;padding:24px}.badge{display:inline-block;background:#e7f0f5;color:#22485b;border-radius:20px;padding:3px 12px;font-size:13px}label{display:block;font-size:14px}input,select,button{font:inherit;border:1px solid #bccbd3;border-radius:7px;background:white;padding:10px}button{cursor:pointer}button:disabled{opacity:.5;cursor:default}iframe{width:100%;height:75vh;border:1px solid #bccbd3;background:white;border-radius:8px}table{width:100%;border-collapse:collapse;background:#fff}td,th{text-align:left;padding:12px;border-bottom:1px solid #dce2e8;vertical-align:top;overflow-wrap:anywhere}th{font-size:14px}.scroll{overflow:auto}.warning{background:#fff5de;padding:14px 18px;border-radius:8px}footer{max-width:1120px;margin:0 auto;padding:24px 22px;color:#546575;font-size:13px}code{overflow-wrap:anywhere}.row{display:flex;gap:14px;align-items:center;flex-wrap:wrap}summary{cursor:pointer}@media(max-width:650px){td,th{font-size:12px;padding:7px}}'''

def page(title, body, script=''):
    return f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="no-referrer"><meta name="robots" content="noindex,nofollow"><meta http-equiv="Content-Security-Policy" content="default-src 'self' data:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'"><title>{esc(title)} · Archivo documental</title><link rel="stylesheet" href="assets/sitio.css"></head><body><header><span class="badge">Archivo personal · copia local</span><h1>{esc(title)}</h1><nav><a href="index.html">Inicio</a><a href="cronologia.html">Cronología</a><a href="hallazgos.html">Hallazgos</a><a href="fuentes.html">Fuentes conservadas</a><a href="carta.html">Carta</a><a href="registro.html">Registro</a></nav></header><main>{body}</main><footer>Actualización: {esc(NOW)} · Fechas: America/Mexico_City · Los archivos permiten revisar registros; una coincidencia no prueba causalidad.</footer>{script}</body></html>'''

class OfflineHTML(HTMLParser):
    """Vista derivada sin enlaces externos; original byte a byte aparte."""
    def __init__(self, source, anchors):
        super().__init__(convert_charrefs=False)
        self.source, self.anchors = source, anchors
        self.out, self.skip = [], 0
        self.external_links = 0
    def local(self, value):
        parts = urlsplit(html.unescape(value))
        if parts.scheme or parts.netloc:
            if parts.scheme == 'data': return value
            if parts.scheme != 'file': return None
            target = Path(unquote(parts.path))
        else:
            if value.startswith('#'): return value
            candidate = unquote(parts.path)
            target = (ORIGINS['facebook'] / candidate.lstrip('/')) if candidate.startswith('/') else self.source.parent / candidate
            target = target.resolve()
            if not target.exists() and self.source.is_relative_to(ORIGINS['facebook']):
                target = (ORIGINS['facebook'] / candidate.lstrip('/')).resolve()
        rel = origin_path(target)
        if rel is None or not target.is_file() or target == SECRET_CONFIG: return None
        if target.suffix.lower() == '.html': dest = SITE / 'paginas' / rel
        elif target.suffix.lower() in {'.json', '.csv', '.txt', '.vcf'}:
            dest = SITE / 'paginas' / Path(str(rel) + '.html')
        else: dest = SITE / 'originales' / rel
        current = SITE / 'paginas' / origin_path(self.source)
        value = href(Path(os.path.relpath(dest, current.parent)))
        return value + ('#' + parts.fragment if parts.fragment else '')
    def handle_decl(self, decl): self.out.append('<!' + decl + '>')
    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'iframe', 'object'}:
            self.skip += 1
            return
        if self.skip: return
        d = dict(attrs)
        if tag in {'base', 'embed'} or (tag == 'meta' and (d.get('http-equiv', '').lower() in {'refresh', 'content-security-policy'})): return
        result = []
        for k, v in attrs:
            if k.startswith('on') or k in {'action','formaction','ping','srcset','integrity','nonce'}: continue
            if k in {'href','src','poster','background'} and v is not None:
                rewritten = self.local(v)
                if rewritten is None:
                    self.external_links += 1
                    if k == 'href': result += [('data-url-original', v), ('title', 'Dirección histórica; esta vista se consulta localmente')]
                    continue
                v = rewritten
            if k == 'style' and v: v = re.sub(r'url\([^)]*\)', 'none', v, flags=re.I)
            if k == 'target': continue
            result.append((k,v))
        line, col = self.getpos()
        if (line,col) in self.anchors:
            result = [(k,v) for k,v in result if k != 'id'] + [('id',f'pos-{line}-{col}')]
        rendered = ''.join(' '+k+(('="'+esc(v)+'"') if v is not None else '') for k,v in result)
        self.out.append('<'+tag+rendered+'>')
        if tag == 'head':
            self.out.append('<meta name="referrer" content="no-referrer"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; img-src \'self\' data:; style-src \'unsafe-inline\'; media-src \'self\'; font-src \'self\'; form-action \'none\'; frame-src \'none\'; base-uri \'none\'">')
    def handle_startendtag(self,tag,attrs): self.handle_starttag(tag,attrs)
    def handle_endtag(self,tag):
        if self.skip:
            if tag in {'script','iframe','object'}: self.skip -= 1
            return
        if tag not in {'base','embed'}: self.out.append('</'+tag+'>')
    def handle_data(self,data):
        if not self.skip: self.out.append(data)
    def handle_entityref(self,name):
        if not self.skip: self.out.append('&'+name+';')
    def handle_charref(self,name):
        if not self.skip: self.out.append('&#'+name+';')
    def handle_comment(self,data):
        if not self.skip: self.out.append('<!--'+data+'-->')

def gather_references():
    refs=[]
    for name in ['fuentes-web.json','imagen-validacion-fuentes-web.json','facebook-google-fuentes-web.json','pistas-fuentes-web.json']:
        d=read(name)
        if isinstance(d,dict): d=d.get('consulted_sources',[])
        for i,item in enumerate(d,1):
            r=dict(item);r.setdefault('id',f'I{i:02}');r.setdefault('title',r.get('role',r['url']));refs.append(r)
    if (RESEARCH/'datos/noche-dispositivos-fuentes-web.json').exists():refs.extend(read('noche-dispositivos-fuentes-web.json'))
    if (RESEARCH/'datos/sesiones-fuentes-web.json').exists():refs.extend(read('sesiones-fuentes-web.json'))
    if (RESEARCH/'datos/iphone-fuentes-web.json').exists():refs.extend(read('iphone-fuentes-web.json'))
    if (RESEARCH/'datos/bydefault-fuentes-web.json').exists():refs.extend(read('bydefault-fuentes-web.json'))
    if (RESEARCH/'datos/github-fuentes-web.json').exists():refs.extend(read('github-fuentes-web.json')['sources'][2:])
    refs.extend([
      {'id':'G01','title':'GitHub: creación de cuenta','url':'https://docs.github.com/en/account-and-profile/how-tos/account-management/creating-an-account-on-github','notes':'Una cuenta personal requiere correo verificado. No se ha creado una cuenta desde este entorno.','consulted_on':'2026-10-01'},
      {'id':'G02','title':'GitHub Pages: visibilidad y control de acceso','url':'https://docs.github.com/en/enterprise-cloud%40latest/pages/getting-started-with-github-pages/changing-the-visibility-of-your-github-pages-site','notes':'Pages privado requiere un sitio de proyecto de una organización con GitHub Enterprise Cloud; un repositorio privado por sí solo no restringe el sitio.','consulted_on':'2026-10-01'}])
    return refs

def local_url(url, source_by_path, refs):
    if str(url).startswith('file:'):
        p=Path(unquote(urlsplit(str(url)).path))
        if str(p) in source_by_path:
            fragment=urlsplit(str(url)).fragment
            return 'fuente.html?id='+source_by_path[str(p)]['code']+('&ancla='+quote(fragment) if re.fullmatch(r'(?:linea|correo)-\d+',fragment) else '')
        rel=origin_path(p)
        if rel:
            if p==SECRET_CONFIG: return 'respaldo.html'
            return href(Path('paginas')/rel)+('' if p.suffix=='.html' else '.html') if p.suffix in {'.html','.json','.csv','.txt','.vcf'} else href(Path('originales')/rel)
        if p.name=='historial-cruzado.html': return 'cronologia.html'
        if p.is_relative_to(RESEARCH):return href(Path('investigacion')/p.relative_to(RESEARCH))
        return 'registro.html'
    match=next((r for r in refs if r['url']==url),None)
    return 'referencias.html#'+quote(match['id']) if match else 'cronologia.html?buscar='+quote(str(url),safe='')

def markdown_local(text, sources, refs):
    blocks=[]
    for paragraph in re.split(r'\n\s*\n',text):
        if not paragraph.strip() or paragraph.startswith('<!--'): continue
        out=[];last=0
        for m in re.finditer(r'\[([^\]]+)\]\(([^\n]+?)\)',paragraph):
            out.append(esc(paragraph[last:m.start()]));out.append('<a href="'+esc(local_url(m[2],sources,refs))+'">'+esc(m[1])+'</a>');last=m.end()
        out.append(esc(paragraph[last:]));rendered=''.join(out)
        if paragraph.startswith('#'):
            rendered=re.sub(r'^#+\s*','',rendered);blocks.append('<h2>'+rendered+'</h2>')
        else: blocks.append('<p style="white-space:pre-wrap">'+rendered+'</p>')
    return '\n'.join(blocks)

def prepare():
    ROOT.mkdir(parents=True,exist_ok=True);ROOT.chmod(0o700)
    SITE.mkdir(parents=True,exist_ok=True);SITE.chmod(0o700)
    events=read('actividad-cronologica.json');sources=read('catalogo-fuentes.json');summary=read('actividad-resumen.json');refs=gather_references()
    source_by_path={s['path']:s for s in sources}
    anchors={}
    for e in events:
        loc=e['locator']
        if 'html_line_1based' in loc: anchors.setdefault(e['source_path'],set()).add((loc['html_line_1based'],loc['html_column_0based']))
    # The existing research log remains authoritative, including this preparation.
    block=f'''<!-- INICIO_RESULTADOS_SESION_5 -->
## Sesión 5: sitio portable y publicación pendiente

Solicitud: conservar las páginas locales de los datos, preparar GitHub y una carta personal. Cuenta indicada por el usuario: spinky-afk. La declaración del usuario no equivale a una conclusión del análisis.

Se prepara un sitio privado local con cronología, catálogo de fuentes actualizado, copias originales y vistas derivadas sin navegación externa. El usuario confirmó la cuenta spinky-afk. GitHub CLI quedó autorizado para spinky-afk. El estado remoto verificado se conserva en estado-publicacion.json.

GitHub Pages no se habilita automáticamente: la privacidad del repositorio no garantiza la privacidad de Pages. Referencia local G02 en referencias.html. Consulta del 1 de octubre de 2026.

Cuatro archivos contienen la clave VAPID; se conservan mediante respaldo cifrado y permanecen intactos en sus ubicaciones locales. El usuario autorizó posteriormente subir todos los originales y datos privados. La carpeta evidencia conserva íntegros los originales, las claves recuperadas y todo research; las vistas de lectura del sitio son derivados. La carta se guarda como testimonio solicitado, sin verificación de las acusaciones.

Actualización preparada: {NOW}. Las próximas actualizaciones requieren ejecutar el constructor; no hay una tarea automática ni vigilancia permanente.
<!-- FIN_RESULTADOS_SESION_5 -->'''
    lp=RESEARCH/'registro.md';log=lp.read_text()
    if '<!-- INICIO_RESULTADOS_SESION_5 -->' in log: log=re.sub(r'<!-- INICIO_RESULTADOS_SESION_5 -->.*?<!-- FIN_RESULTADOS_SESION_5 -->',lambda _:block,log,flags=re.S)
    else: log+='\n\n'+block+'\n'
    write(lp,log)
    # Mirror all research except plaintext recovered keys and the local rescue key.
    archive=SITE/'investigacion'
    for p in RESEARCH.rglob('*'):
        if not p.is_file() or p.name in PRIVATE_NAMES or '__pycache__' in p.parts: continue
        dest=archive/p.relative_to(RESEARCH);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);dest.chmod(0o600)
    manifest=[];removed_links=0
    for key,root in ORIGINS.items():
        for p in ([root] if root.is_file() else sorted(root.rglob('*'))):
            if not p.is_file(): continue
            rel=origin_path(p)
            row={'origin_path':str(p),'archive_path':str(Path('originales')/rel),'bytes':p.stat().st_size,'sha256':sha(p),'encrypted_only':p==SECRET_CONFIG}
            if p!=SECRET_CONFIG:
                dest=SITE/'originales'/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest);dest.chmod(0o600)
                if sha(dest)!=row['sha256']: raise ValueError('Copia original distinta: '+str(p))
                if p.suffix.lower()=='.html':
                    parser=OfflineHTML(p,anchors.get(str(p),set()));parser.feed(p.read_text(encoding='utf-8',errors='replace'));parser.close()
                    view=SITE/'paginas'/rel;write(view,''.join(parser.out));removed_links+=parser.external_links
                elif p.suffix.lower() in {'.json','.csv','.txt','.vcf'}:
                    text=p.read_text(encoding='utf-8',errors='replace')
                    content='<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="referrer" content="no-referrer"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; base-uri \'none\'; form-action \'none\'"><title>'+esc(p.name)+'</title><style>body{font:15px system-ui;margin:24px}pre{font:13px/1.5 monospace;white-space:pre-wrap;overflow-wrap:anywhere}span:target{background:#ffec9f}</style></head><body><h1>'+esc(p.name)+'</h1><p>Vista del archivo conservado. El localizador del registro aparece en el visor de fuentes.</p><pre>'+''.join('<span id="linea-'+str(i)+'">'+esc(line)+'</span>\n' for i,line in enumerate(text.splitlines(),1))+'</pre></body></html>'
                    write(SITE/'paginas'/Path(str(rel)+'.html'),content)
                elif p.suffix.lower()=='.mbox':
                    from mail_util import extract
                    maildata=extract()
                    entries=''.join('<li id="correo-'+str(m['mbox_index'])+'"><a href="../../investigacion/'+href(m['page'])+'">'+esc(m['id']+' · '+m['date_header']+' · '+m['public_subject'])+'</a></li>' for m in maildata['messages'])
                    content='<!doctype html><html lang="es"><meta charset="utf-8"><meta name="referrer" content="no-referrer"><title>Correo conservado</title><h1>Índice del MBOX conservado</h1><p>Cabeceras Date declaradas; vista de lectura derivada. El MBOX íntegro se conserva como original.</p><ol>'+entries+'</ol></html>'
                    write(SITE/'paginas'/Path(str(rel)+'.html'),content)
            manifest.append(row)
    for s in sources:
        rel=origin_path(s['path']);p=Path(s['path'])
        if p==SECRET_CONFIG: raise ValueError('Fuente fechada secreta requiere tratamiento explícito')
        if sha(SITE/'originales'/rel)!=s['sha256']: raise ValueError('Cambió una fuente: '+s['code'])
        s['original_local']=href(Path('originales')/rel)
        s['view_local']=href(Path('paginas')/rel)+('' if p.suffix.lower()=='.html' else '.html')
    json_write(SITE/'manifiesto-originales.json',manifest)
    json_write(SITE/'catalogo-fuentes-local.json',sources)
    json_write(SITE/'referencias-locales.json',refs)
    write(SITE/'assets/sitio.css',CSS)
    write(SITE/'carta-original.txt',LETTER+'\n')
    letterbody='<div class="panel"><p><strong>Testimonio personal del usuario.</strong> Se conserva el texto solicitado. Sus afirmaciones sobre delitos y compromisos técnicos no han sido verificadas por esta revisión.</p><p><a href="carta-original.txt" download>Descargar texto</a> · <a href="carta.pdf">Consultar PDF</a></p></div><div class="letter">'+esc(LETTER)+'</div>'
    write(SITE/'carta.html',page('Carta a las personas de confianza',letterbody))
    home=f'''<p>Este archivo reúne tus exportaciones, las preguntas recuperadas y la investigación realizada. Puedes seguir una observación hasta su página de origen sin depender de que Facebook o Google la sigan mostrando en internet.</p><div class="grid"><div class="card"><div class="number">{len(events):,}</div><p>Observaciones fechadas</p><a href="cronologia.html">Consultar la cronología</a></div><div class="card"><div class="number">{len(sources)}</div><p>Fuentes de la cronología</p><a href="fuentes.html">Abrir las páginas conservadas</a></div><div class="card"><div class="number">845</div><p>Archivos originales inventariados</p><a href="respaldo.html">Ver conservación y respaldo</a></div></div><h2>Seguir las pistas</h2><div class="row"><a href="cronologia.html?buscar=vapid">VAPID y Web Push</a><a href="cronologia.html?buscar=Etsy">Etsy</a><a href="cronologia.html?buscar=Clar%C3%ADn">Clarín</a><a href="cronologia.html?buscar=hermes">Hermes</a><a href="cronologia.html?buscar=TrustBuilder">Validación y TrustBuilder</a><a href="cronologia.html?buscar=6850175308">Número recordado</a></div><a href="cronologia.html?buscar=open%20by%20default">Open by default</a><a href="investigacion/bydefault-cruces.md">Pista bydefault</a><a href="investigacion/correo-cruces-play.md">Correo y apps</a><h2>Documentación</h2><div class="grid"><div class="card"><h2>Lo que se encontró</h2><p>Hallazgos, relaciones documentadas y preguntas que siguen abiertas.</p><a href="hallazgos.html">Leer los hallazgos</a></div><div class="card"><h2>Carta personal</h2><p>El mensaje que pediste conservar para Rocio1, Rocio2, Mane, Sandro y Denisse.</p><a href="carta.html">Leer la carta</a></div><div class="card"><h2>Informe completo</h2><p>Cronología, anexos y procedencia. Esta edición dirige sus enlaces a las páginas del archivo.</p><a href="historial-cruzado.pdf">Consultar el PDF</a></div></div><p class="note">Periodo: {summary['earliest'][:10]} a {summary['latest'][:10]}. Hay {summary['undated_observations']} bloques sin fecha conservados por separado. Los artículos de internet solo están guardados íntegros cuando existe una copia original; las referencias técnicas tienen fichas locales con las notas de consulta.</p><p class="warning">Publicación pendiente. Este sitio contiene información personal y se prepara para almacenamiento privado. No se ha activado GitHub Pages.</p>'''
    home=home.replace('<div class="number">845</div>', '<div class="number">'+str(len(manifest))+'</div>')
    home=home.replace('<h2>Seguir las pistas</h2>', '<h2>Seguir las pistas</h2><p><a href="cronologia.html?buscar=Uber">Uber Rider y Eats</a> · <a href="investigacion/uber-analytics-cruces.md">Informe de cruces de Uber</a></p>')
    write(SITE/'index.html',page('Archivo documental',home))
    source_rows=''.join('<tr><td>'+esc(s['code'])+'</td><td><a href="fuente.html?id='+esc(s['code'])+'">'+esc(s['path'].split('/Documentos/')[-1])+'</a></td><td>'+str(s['records'])+'</td><td><code>'+esc(s['sha256'])+'</code></td></tr>' for s in sources)
    write(SITE/'fuentes.html',page('Fuentes conservadas','<p>Las copias originales conservan sus bytes y SHA-256. Las vistas permiten consultar el mismo contenido localmente; se retiran la navegación y cargas externas. Esta diferencia se identifica en cada fuente.</p><p><a href="manifiesto-originales.json">Inventario íntegro de originales</a></p><label>Buscar fuente<input id="q" type="search" placeholder="Chrome, mensajes, Etsy…"></label><div class="scroll"><table><thead><tr><th>Código</th><th>Archivo</th><th>Registros</th><th>SHA-256 original</th></tr></thead><tbody>'+source_rows+'</tbody></table></div>','<script>document.getElementById("q").oninput=e=>{const q=e.target.value.toLocaleLowerCase();document.querySelectorAll("tbody tr").forEach(r=>r.hidden=!r.textContent.toLocaleLowerCase().includes(q));};</script>'))
    viewer='''<div id="source" class="panel"></div><p id="locator" class="note"></p><iframe id="view" title="Página conservada de la fuente" sandbox="allow-same-origin"></iframe><noscript>Consulta el catálogo de fuentes o los archivos originales.</noscript>'''
    viewerjs='''const sources=__SOURCES__;const params=new URLSearchParams(location.search);const s=sources.find(x=>x.code===params.get('id'));const box=document.getElementById('source');function node(tag,text){const e=document.createElement(tag);e.textContent=text;return e;}if(!s){box.textContent='Selecciona una fuente desde el catálogo o la cronología.';document.getElementById('view').hidden=true;}else{box.append(node('h2',s.code+' · '+s.path.split('/').pop()),node('p',s.path),node('p','SHA-256: '+s.sha256));const a=node('a','Descargar copia original sin modificar');a.href=s.original_local;a.download=s.path.split('/').pop();box.append(a,node('p','La página inferior es una vista derivada local. Conserva el contenido y los adjuntos disponibles; desactiva enlaces externos, formularios y scripts.'));let anchor=params.get('ancla')||'';if(!/^(pos-\\d+-\\d+|linea-\\d+)$/.test(anchor))anchor='';document.getElementById('view').src=s.view_local+(anchor?'#'+anchor:'');document.getElementById('locator').textContent=(params.get('evento')||'')+' · '+(params.get('localizador')||'');}'''.replace('__SOURCES__',embedded(sources))
    viewerjs=viewerjs.replace('linea-\\d+)$','linea-\\d+|correo-\\d+)$').replace("s.view_local+(anchor?'#'+anchor:'')", "(s.path.endsWith('.mbox')&&anchor.startsWith('correo-')?'investigacion/correos/M'+anchor.slice(7).padStart(6,'0')+'.html':s.view_local+(anchor?'#'+anchor:''))")
    write(SITE/'fuente.html',page('Página original conservada',viewer,'<script>'+viewerjs+'</script>'))
    parts=[]
    for r in read('informe-estructurado.json'):
        if r['type']=='heading': parts.append('<h2>'+esc(r['text'])+'</h2>')
        elif r['type']=='link': parts.append('<p><a href="'+esc(local_url(r['url'],source_by_path,refs))+'">'+esc(r['text'])+' · ficha local</a></p>')
        elif r['type']=='evidence': parts.append('<div class="panel"><a href="cronologia.html?buscar='+quote(r['event_id'])+'">'+esc(r['event_id'])+'</a><p>'+esc(r['text'])+'</p></div>')
        else: parts.append('<p>'+esc(r['text'])+'</p>')
    write(SITE/'hallazgos.html',page('Hallazgos y preguntas abiertas','<p class="note">Los enlaces abren la evidencia conservada o una ficha local de consulta técnica. Una referencia bibliográfica no significa que hayamos guardado una copia íntegra del artículo.</p>'+''.join(parts)))
    write(SITE/'registro.html',page('Registro de investigación',markdown_local(log,source_by_path,refs)))
    refbody='<p>Estas fichas conservan las notas y la procedencia de las consultas externas. No son copias completas de esas páginas y no garantizan el contenido que tenían cuando se visitaron. Las direcciones se muestran como texto, sin depender de enlaces activos.</p>'
    for r in refs:
        refbody+='<section class="panel" id="'+esc(r['id'])+'"><h2>'+esc(r['id']+' · '+r['title'])+'</h2><p>'+esc(r.get('notes',r.get('summary','')))+'<p><code>'+esc(r['url'])+'</code></p><p class="note">'+esc(r.get('relationship',r.get('role','Consulta técnica')))+' · Consultado: '+esc(r.get('consulted_on','No especificado'))+' · '+esc(r.get('status','Ver detalle de notas'))+'</p><details><summary>Ficha registrada</summary><pre>'+esc(json.dumps(r,ensure_ascii=False,indent=2))+'</pre></details></section>'
    write(SITE/'referencias.html',page('Referencias técnicas conservadas',refbody))
    # Preserve the existing mature offline timeline, replacing its navigation.
    timeline=(RESEARCH/'historial-cruzado.html').read_text()
    dataset=re.search(r'<script id="dataset" type="application/json">(.*?)</script>',timeline,re.S)
    d=json.loads(dataset[1]);d['sources']=sources
    timeline=timeline[:dataset.start(1)]+embedded(d)+timeline[dataset.end(1):]
    old="function fileUrl(path){return 'file://'+path.split('/').map(encodeURIComponent).join('/');}"
    new="function fileUrl(path){const s=D.sources.find(x=>x.path===path);if(s)return 'fuente.html?id='+encodeURIComponent(s.code);for(const [root,key] of [[\"/home/deep-logic/Documentos/facebook/\",\"facebook\"],[\"/home/deep-logic/Documentos/Registro/Takeout/\",\"google\"]]){if(path.startsWith(root)){const rel=path.slice(root.length).split('/').map(encodeURIComponent).join('/');return /\\.(html|json|csv|txt|vcf)$/i.test(path)?'paginas/'+key+'/'+rel+(path.endsWith('.html')?'':'.html'):'originales/'+key+'/'+rel;}}return 'fuentes.html';}"
    if old not in timeline: raise ValueError('Cambió el visor base; revisar adaptación')
    timeline=timeline.replace(old,new)
    timeline=timeline.replace("if(r.url)c.append(a('Abrir enlace web',r.url));", "const provenance=el('p');let anchor=r.locator.html_line_1based?'pos-'+r.locator.html_line_1based+'-'+r.locator.html_column_0based:(r.locator.csv_line_1based?'linea-'+r.locator.csv_line_1based:'');const sourceUrl=fileUrl(r.source_path)+'&evento='+r.id+'&localizador='+encodeURIComponent(JSON.stringify(r.locator))+(anchor?'&ancla='+anchor:'');provenance.append(a('Ver registro en la página local · '+r.source_code,sourceUrl));c.append(provenance);if(r.url)c.append(el('div','Dirección histórica: '+r.url,'meta'));")
    timeline=timeline.replace("(r.locator.csv_line_1based?'linea-'+r.locator.csv_line_1based:'')", "(r.locator.csv_line_1based?'linea-'+r.locator.csv_line_1based:(r.locator.mbox_message_index_1based?'correo-'+r.locator.mbox_message_index_1based:''))")
    timeline=timeline.replace('r.id,r.subject,r.url,r.channel','r.id,r.subject,r.body_search||\'\',r.url,r.channel')
    timeline=timeline.replace("const url=u.startsWith('http')?u:fileUrl('/home/deep-logic/Documentos/facebook/'+u);const p=el('p');p.append(a('Adjunto / enlace: '+u,url));det.append(p);", "const p=el('p');if(u.startsWith('http'))p.append(el('span','Dirección histórica del adjunto: '+u));else p.append(a('Abrir adjunto conservado: '+u,fileUrl('/home/deep-logic/Documentos/facebook/'+u)));det.append(p);")
    timeline=timeline.replace('href="hallazgos-facebook.md"','href="hallazgos.html"').replace('href="registro.md"','href="registro.html"').replace('href="actividad-cronologica.csv"','href="investigacion/actividad-cronologica.csv"')
    timeline=timeline.replace('<h1>Tu historial cruzado</h1>', '<nav><a href="index.html">Inicio</a> · <a href="fuentes.html">Fuentes</a> · <a href="carta.html">Carta</a></nav><h1>Tu historial cruzado</h1>')
    timeline=timeline.replace('apply();\n</script>', "const requested=new URLSearchParams(location.search).get('buscar');if(requested)$('term').value=requested;apply();\n</script>")
    timeline=timeline.replace('<meta charset="utf-8">','<meta charset="utf-8"><meta name="referrer" content="no-referrer"><meta name="robots" content="noindex,nofollow"><meta http-equiv="Content-Security-Policy" content="default-src \'self\' data:; script-src \'self\' \'unsafe-inline\'; style-src \'unsafe-inline\'; connect-src \'none\'; form-action \'none\'; base-uri \'none\'; object-src \'none\'">',1)
    write(SITE/'cronologia.html',timeline)
    # Four sensitive originals are included encrypted, with a local-only key.
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    keyfile=RESEARCH/'privado/clave-respaldo-github-local.txt'
    if keyfile.exists(): key=base64.urlsafe_b64decode(keyfile.read_text().strip())
    else:
        key=AESGCM.generate_key(bit_length=256);write(keyfile,base64.urlsafe_b64encode(key).decode()+'\n')
    sealed_paths=[RESEARCH/'privado'/n for n in ['vapid-recuperada.json','claves-recuperadas.md','vapid-private.pem']]+[SECRET_CONFIG]
    package={'version':1,'created_at_utc':NOW,'files':[{'path':str(p),'sha256':sha(p),'data_base64':base64.b64encode(p.read_bytes()).decode()} for p in sealed_paths]}
    nonce=os.urandom(12);cipher=AESGCM(key).encrypt(nonce,json.dumps(package,ensure_ascii=False).encode(),b'expediente-documental-v1')
    json_write(SITE/'respaldo-sensible-cifrado.json',{'algorithm':'AES-256-GCM','aad':'expediente-documental-v1','nonce_base64':base64.b64encode(nonce).decode(),'ciphertext_base64':base64.b64encode(cipher).decode()})
    backupbody='<p>Se inventariaron 845 originales. Hay 844 copias originales sin modificación y una copia cifrada de Chrome/Configuración.json. Las tres versiones de la clave recuperada de research también están en ese respaldo cifrado.</p><p>El respaldo cifrado usa la clave local de <code>'+esc(keyfile)+'</code>. La carpeta evidencia también conserva la clave y todos los originales, según autorización del propietario. Los archivos de origen siguen intactos. Para recuperar el respaldo usa el script incluido en la raíz del proyecto; mantén el repositorio privado.</p><p><a href="manifiesto-originales.json">Inventario y huellas originales</a> · <a href="respaldo-sensible-cifrado.json" download>Respaldo cifrado</a> · <a href="referencias.html#G02">Ficha local sobre privacidad de GitHub Pages</a></p><p>Las vistas de las páginas son derivadas: desactivan vínculos externos y agregan anclas para encontrar registros. La huella del inventario corresponde al original descargable, no a esa vista.</p>'
    backupbody=backupbody.replace('845 originales',str(len(manifest))+' originales').replace('844 copias',str(len(manifest)-1)+' copias')
    write(SITE/'respaldo.html',page('Conservación y respaldo',backupbody))
    previous_state=json.loads((ROOT/'estado-publicacion.json').read_text()) if (ROOT/'estado-publicacion.json').exists() else {}
    json_write(ROOT/'estado-publicacion.json',{**previous_state,'updated_at_utc':NOW,'preferred_account_name':'spinky-afk','account_created':True,'github_connected':previous_state.get('github_connected',False),'remote_repository':previous_state.get('remote_repository'),'repository_required_visibility':'private','site_publication':previous_state.get('site_publication','local'),'pages_enabled':False,'raw_originals':len(manifest),'plain_originals':len(manifest)-1,'encrypted_originals':1,'timeline_observations':len(events),'timeline_sources':len(sources),'known_private_key_files_encrypted':4})
    write(ROOT/'.gitignore','__pycache__/\n*.pyc\n# Autorización: todo el contenido de evidencia se conserva íntegro.\n')
    write(ROOT/'README.md','''# Archivo documental privado

Archivo preparado para la cuenta GitHub verificada `spinky-afk`. El estado de subida y el enlace remoto comprobado están en `estado-publicacion.json`.

El proyecto contiene datos personales, conversaciones, identificadores y URLs originales. La visibilidad prevista del repositorio es **privada**. No actives GitHub Pages sin verificar que el sitio tendrá control de acceso: un repositorio privado no hace privado un sitio de Pages. No hay despliegue automático.

Para consultar: abre `sitio/index.html`, o ejecuta desde esta carpeta:

```bash
python3 servir_local.py
```

Abre `http://127.0.0.1:8765`. El servidor escucha solo en tu equipo. Carta, cronología, PDF, fuentes originales y vistas derivadas están dentro de `sitio`.

El constructor está en `../vapid-webpush/scripts/construir_sitio.py`. Para actualizar después de reconstruir los datos:

```bash
python3 ../vapid-webpush/scripts/construir_sitio.py
```

El registro se conserva en research y en el sitio. Las fuentes originales incluyen SHA-256 y se comparan durante la construcción. Las vistas desactivan navegación y carga externas; no se afirma que sean byte a byte idénticas al original descargable. Las fichas de referencias externas contienen notas, no copias completas de los artículos.

La carpeta `evidencia/originales` contiene todos los originales sin excluir datos privados, incluida la configuración Chrome. `evidencia/investigacion` conserva todo research, las claves recuperadas y la clave de respaldo, según autorización del propietario. El sitio conserva adicionalmente su respaldo cifrado y vistas de lectura. Los archivos grandes usan Git LFS: descarga mediante `git clone` y `git lfs pull` para recuperar sus bytes completos. Las credenciales de la conexión GitHub están fuera del expediente.

La carta reproduce un testimonio personal solicitado. Las acusaciones no son conclusiones verificadas del análisis. No se envió a sus destinatarios.
''')
    json_write(SITE/'verificacion-construccion.json',{'created_at_utc':NOW,'source_hashes_verified':len(sources),'original_copies_verified':len(manifest)-1,'dated_events':len(events),'external_link_attributes_removed':removed_links,'private_plaintext_keys_included':False,'site_published':False})
    print(json.dumps({'site':str(SITE),'events':len(events),'sources':len(sources),'original_files':len(manifest),'external_link_attributes_removed':removed_links},ensure_ascii=False),flush=True)
    return sources,refs

def pdfs(sources,refs):
    spec=importlib.util.spec_from_file_location('pdf_local',RESEARCH/'scripts/generar_pdf.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    bypath={s['path']:s for s in sources}
    original_pdf=m.PDF
    class LocalPDF(original_pdf):
        def text(self,text,size=9,color=m.INK,bold=False,gap=5,url=None,indent=0):
            if url: url=local_url(str(url),bypath,refs)
            text=str(text).replace('Los enlaces originales con parámetros de acceso se guardan en la carpeta privado.', 'Las URLs originales se conservan en el archivo privado de investigación.')
            if text.startswith('Las referencias a archivos locales funcionarán'):
                text='Los enlaces de esta edición apuntan a páginas del archivo conservado. Mantén el PDF junto al sitio; algunos lectores de PDF restringen la apertura de referencias relativas.'
            return super().text(text,size,color,bold,gap,url,indent)
    m.PDF=LocalPDF
    m.OUT=SITE
    m.read=lambda name: json.loads((RESEARCH/name).read_text())
    write(SITE/'registro.md',(RESEARCH/'registro.md').read_text())
    (SITE/'datos').mkdir(exist_ok=True)
    shutil.copy2(RESEARCH/'datos/actividad-cronologica.json',SITE/'datos/actividad-cronologica.json')
    m.main()
    # The letter is a short standalone artifact as requested, with attribution.
    letter=m.PDF(SITE/'carta.pdf');m.metadata(letter.surface,0,'Carta personal a personas de confianza'.encode())
    letter.heading('Carta personal',24);letter.text('Texto solicitado por el usuario · 1 de octubre de 2026',10,m.MUTED)
    letter.text('Testimonio personal. Las afirmaciones sobre delitos y compromisos técnicos no se han verificado mediante esta revisión.',10,m.MUTED,gap=20)
    letter.text(LETTER,11,gap=12);letter.close();(SITE/'carta.pdf').chmod(0o600)
    # Keep the original earlier PDF in investigacion; this PDF is the local-link edition.
    json_write(SITE/'datos/pdf-edicion-local.json',{'created_at_utc':NOW,'pdf':str(SITE/'historial-cruzado.pdf'),'links':'relative local source pages and reference notes','original_research_pdf_preserved':True})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--sin-pdf',action='store_true');args=parser.parse_args()
    sources,refs=prepare()
    if not args.sin_pdf: pdfs(sources,refs)
