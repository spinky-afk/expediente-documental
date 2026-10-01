#!/usr/bin/env python3
"""PDF Unicode con Pango/Cairo nativos, sin dependencias descargadas."""
import ctypes as C
import ctypes.util
import hashlib
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, quote

OUT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((OUT/name).read_text())
def lib(name):return C.CDLL(ctypes.util.find_library(name))
CA=lib('cairo');PA=lib('pango-1.0');PC=lib('pangocairo-1.0');GO=lib('gobject-2.0')
P=C.c_void_p;I=C.c_int;D=C.c_double;S=C.c_char_p
def bind(l,name,result,*args):
    f=getattr(l,name);f.restype=result;f.argtypes=list(args);return f
surface_create=bind(CA,'cairo_pdf_surface_create',P,S,D,D)
restrict_version=bind(CA,'cairo_pdf_surface_restrict_to_version',None,P,I)
create=bind(CA,'cairo_create',P,P)
destroy=bind(CA,'cairo_destroy',None,P)
finish=bind(CA,'cairo_surface_finish',None,P)
surface_destroy=bind(CA,'cairo_surface_destroy',None,P)
surface_status=bind(CA,'cairo_surface_status',I,P)
status=bind(CA,'cairo_status',I,P)
status_string=bind(CA,'cairo_status_to_string',S,I)
rgb=bind(CA,'cairo_set_source_rgb',None,P,D,D,D)
move=bind(CA,'cairo_move_to',None,P,D,D)
rect=bind(CA,'cairo_rectangle',None,P,D,D,D,D)
fill=bind(CA,'cairo_fill',None,P)
show_page=bind(CA,'cairo_show_page',None,P)
tag_begin=bind(CA,'cairo_tag_begin',None,P,S,S)
tag_end=bind(CA,'cairo_tag_end',None,P,S)
outline=bind(CA,'cairo_pdf_surface_add_outline',I,P,I,S,S,I)
metadata=bind(CA,'cairo_pdf_surface_set_metadata',None,P,I,S)
layout_create=bind(PC,'pango_cairo_create_layout',P,P)
layout_context=bind(PA,'pango_layout_get_context',P,P)
resolution=bind(PC,'pango_cairo_context_set_resolution',None,P,D)
font_from=bind(PA,'pango_font_description_from_string',P,S)
font_free=bind(PA,'pango_font_description_free',None,P)
set_font=bind(PA,'pango_layout_set_font_description',None,P,P)
set_text=bind(PA,'pango_layout_set_text',None,P,S,I)
set_width=bind(PA,'pango_layout_set_width',None,P,I)
set_wrap=bind(PA,'pango_layout_set_wrap',None,P,I)
set_spacing=bind(PA,'pango_layout_set_spacing',None,P,I)
line_count=bind(PA,'pango_layout_get_line_count',I,P)
get_line=bind(PA,'pango_layout_get_line_readonly',P,P,I)
show_line=bind(PC,'pango_cairo_show_layout_line',None,P,P)
unref=bind(GO,'g_object_unref',None,P)
class Rectangle(C.Structure):_fields_=[('x',I),('y',I),('width',I),('height',I)]
line_extents=bind(PA,'pango_layout_line_get_extents',None,P,C.POINTER(Rectangle),C.POINTER(Rectangle))

INK=(.09,.17,.22);MUTED=(.33,.41,.46);TEAL=(.07,.39,.47);PURPLE=(.31,.28,.54)
class PDF:
    W=595.276;H=841.89;M=42;BOTTOM=799
    def __init__(self,path):
        self.path=path;self.surface=surface_create(str(path).encode(),self.W,self.H);self.ctx=create(self.surface)
        # PDF 1.4 evita índices de objetos comprimidos de 16 bits en documentos
        # con decenas de miles de anotaciones de enlace.
        restrict_version(self.surface,0)
        self.fonts={};self.page=1;self.y=48;self.label='Historial cruzado';self.lines=0;self.page_records={};self.event_pages={}
        metadata(self.surface,0,'Historial cruzado — Google y Facebook'.encode())
        metadata(self.surface,1,'Investigación local para el propietario de los datos'.encode())
        metadata(self.surface,4,b'Investigacion local: Python, Pango y Cairo')
        metadata(self.surface,5,datetime.now(timezone.utc).isoformat().encode())
        self.header()
    def font(self,size,bold=False):
        key=(size,bold)
        if key not in self.fonts:self.fonts[key]=font_from(f'Sans {"Bold " if bold else ""}{size}'.encode())
        return self.fonts[key]
    def header(self):
        rgb(self.ctx,*TEAL);rect(self.ctx,self.M,28,self.W-2*self.M,2);fill(self.ctx)
        self.fixed('INVESTIGACIÓN LOCAL  /  GOOGLE + FACEBOOK',self.M,14,7,MUTED)
    def fixed(self,text,x,y,size=7,color=MUTED):
        l=self.layout(text,size,self.W-2*self.M);line=get_line(l,0);r=Rectangle();line_extents(line,None,C.byref(r))
        rgb(self.ctx,*color);move(self.ctx,x,y-r.y/1024);show_line(self.ctx,line);unref(l)
    def layout(self,text,size,width,bold=False):
        l=layout_create(self.ctx);resolution(layout_context(l),72);set_font(l,self.font(size,bold))
        set_width(l,int(width*1024));set_wrap(l,2);set_spacing(l,0)
        # Se eliminan controles que invalidan texto; se conservan saltos y Unicode.
        text=''.join(c for c in str(text) if ord(c)>=32 or c in '\n\t')
        set_text(l,text.encode(),-1);return l
    def footer(self):
        self.fixed('1 oct 2026  ·  America/Mexico_City  ·  '+self.label[:58],self.M,815,7)
        self.fixed(str(self.page),self.W-70,815,7)
    def new_page(self,label=None):
        self.footer();show_page(self.ctx);self.page+=1;self.y=48
        if label:self.label=label
        self.header()
    def ensure(self,height):
        if self.y+height>self.BOTTOM:self.new_page()
    def text(self,text,size=9,color=INK,bold=False,gap=5,url=None,indent=0):
        l=self.layout(text,size,self.W-2*self.M-indent,bold)
        for i in range(line_count(l)):
            line=get_line(l,i);logical=Rectangle();line_extents(line,None,C.byref(logical))
            height=max(logical.height/1024,size*1.16)
            self.ensure(height+1);rgb(self.ctx,*color);x=self.M+indent
            if url:
                uri=quote(str(url),safe=':/?&=#%+@,;!$()*[]~_-').replace("'",'%27')
                attrs=f"uri='{uri}' rect=[{x:.2f} {self.y:.2f} {max(1,logical.width/1024):.2f} {height:.2f}]"
                tag_begin(self.ctx,b'Link',attrs.encode())
            move(self.ctx,x,self.y-logical.y/1024);show_line(self.ctx,line)
            if url:tag_end(self.ctx,b'Link')
            self.y+=height+1;self.lines+=1
        unref(l);self.y+=gap
    def heading(self,text,size=16,parent=0,bookmark=True):
        self.ensure(55);self.y+=8;dest=f'page={self.page} pos=[{self.M} {self.y:.2f}]'.encode()
        ident=outline(self.surface,parent,text.encode(),dest,0) if bookmark else 0
        self.text(text,size,TEAL,True,gap=9);return ident
    def link(self,label,url,size=8.5):self.text(label,size,TEAL,url=url,gap=4)
    def event(self,r,detailed=False):
        self.ensure(44);self.event_pages[r['id']]=self.page
        self.page_records.setdefault(str(self.page),[]).append(r['id'])
        stamp=r['time_local'];clock=stamp[11:19]
        if r['time_precision']=='microsegundo':clock=stamp[11:26]
        if r['time_precision']=='minuto':clock=stamp[11:16]+' (minuto)'
        color=PURPLE if r['family']=='Facebook' else TEAL
        self.text(f"{r['id']}  |  {clock}  |  {r['family']} / {r['channel']}  |  {r['kind']}",7.7,color,True,gap=1)
        self.text(re.sub(r'\s+',' ',r['subject']).strip(),8.4,gap=1)
        loc=r['locator'];key=next((f'{k}={v}' for k,v in loc.items() if 'index' in k or 'pointer' in k),'')
        pos=f"; L{loc['html_line_1based']}:C{loc['html_column_0based']}" if 'html_line_1based' in loc else ''
        self.text(f"Fuente {r['source_code']} · {key}{pos} · precisión: {r['time_precision']}",6.8,MUTED,gap=1,
                  url=Path(r['source_path']).as_uri())
        if r.get('url'):
            uri=r['url'];label=uri if len(uri)<=170 else uri[:165]+'… [enlace completo]'
            self.link(label,uri,7.2)
        if r['identifiers']:self.text('Identificadores: '+json.dumps(r['identifiers'],ensure_ascii=False),7.1,MUTED,gap=1)
        if r.get('timezone_basis'):self.text(r['timezone_basis'],7.1,MUTED,gap=1)
        if r.get('date_selection'):self.text(r['date_selection']+'; pie original: '+r['footer_date_original'],7.1,MUTED,gap=1)
        for u in r.get('attachment_links',[]):
            if not u or u==r.get('url'):continue
            uri=u if u.startswith(('http:','https:')) else (Path('/home/deep-logic/Documentos/facebook')/u).as_uri()
            self.link('Adjunto / enlace: '+(u if len(u)<170 else u[:165]+'…'),uri,7.1)
        self.y+=4
    def close(self):
        self.footer();show_page(self.ctx);finish(self.surface)
        errors=[status(self.ctx),surface_status(self.surface)]
        if any(errors):raise RuntimeError([status_string(e).decode() for e in errors])
        destroy(self.ctx);surface_destroy(self.surface)
        for f in self.fonts.values():font_free(f)


def previous_log(pdf):
    text=(OUT/'registro.md').read_text().split('<!-- INICIO_RESULTADOS_SESION_3 -->')[0]
    pdf.new_page('Registro de sesiones anteriores');pdf.heading('Registro anterior de investigación')
    pdf.text('Las instrucciones de posponer el PDF que aparecen a continuación son históricas. La sesión actual pidió crearlo y mantenerlo actualizado.',9,MUTED)
    for block in re.split(r'\n\s*\n',text):
        if block.strip().startswith('<!--'):continue
        if not block.strip():continue
        if block.startswith('#'):
            pdf.heading(re.sub(r'^#+\s*','',block.strip()),12,bookmark=False);continue
        links=re.findall(r'\[([^\]]+)\]\((https?://[^)]+)\)',block)
        plain=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',block)
        plain=plain.replace('**','').replace('`','')
        pdf.text(plain,8.5)
        for label,url in links:pdf.link(label+' · '+url,url,7.5)


def main():
    events=read('datos/actividad-cronologica.json');sm=read('datos/actividad-resumen.json')
    temp=OUT/'historial-cruzado.en-proceso.pdf';target=OUT/'historial-cruzado.pdf'
    pdf=PDF(temp)
    pdf.y=95;pdf.text('Tu historial,\nen orden cronológico',31,INK,True,gap=18)
    pdf.text('Google · Chrome · Google Play · Facebook · Messenger',13,TEAL,gap=20)
    pdf.text(f"{len(events):,} registros fechados\n{sm['source_files']} archivos consultados\n{sm['conversation_files']} conversaciones de Messenger\n87 entidades de actividad fuera de Meta",14,gap=22)
    pdf.text('Versión actualizada: 1 de octubre de 2026\nPeriodo observado: '+sm['earliest'][:10]+' → '+sm['latest'][:10]+'\nZona de visualización: America/Mexico_City',10,MUTED,gap=25)
    pdf.text('Este documento reúne hallazgos, preguntas y enlaces, cronología completa de las observaciones extraídas, catálogo de identificadores y referencias a los archivos originales. Cada observación conserva su procedencia.',11,gap=18)
    pdf.link('Abrir visor local con filtros',(OUT/'historial-cruzado.html').as_uri(),11)
    pdf.link('Abrir registro vivo de investigación',(OUT/'registro.md').as_uri(),11)
    pdf.text('Los marcadores del PDF permiten saltar entre hallazgos, meses y anexos. Las fuentes S y registros E corresponden a esta versión. Para referencias duraderas, usa la ruta y el localizador del original.',9,MUTED)
    pdf.new_page('Guía de lectura');pdf.heading('Cómo consultar el documento')
    for t in ['1. Hallazgos: relaciones comprobadas, números distintos y pistas sin confirmar.',
              '2. Cobertura: servicios y número de registros extraídos.',
              '3. Cronología: todos los registros, desde el más antiguo hasta el más reciente; agrupados por día.',
              '4. Anexos: empresas, archivos IA, coincidencias automáticas, registros sin fecha y fuentes.',
              '5. Registro anterior: preguntas, hallazgos y referencias de las primeras sesiones.']:pdf.text(t,11,gap=12)
    pdf.text('Cada entrada muestra el ID de observación, hora, servicio, tipo de dato, texto, enlace y localizador del original. La misma acción puede tener varios registros: se conservan para que puedas revisar el cruce. Las coincidencias temporales no demuestran causalidad.',10)
    pdf.text('Las preguntas y mensajes se conservan completos como texto de la observación. Algunos rótulos de URL muy largos se acortan en pantalla; el enlace clicable conserva la URL depurada completa. Los enlaces originales con parámetros de acceso se guardan en la carpeta privado. No se insertan valores de claves privadas en el PDF.',10)
    pdf.text('Las referencias a archivos locales funcionarán en los lectores que permitan abrir enlaces file. Si el lector los bloquea, el catálogo incluye sus rutas y el visor HTML ofrece la misma procedencia.',9,MUTED)
    pdf.new_page('Hallazgos')
    for part in read('datos/informe-estructurado.json'):
        if part['type']=='heading':pdf.heading(part['text'],15)
        elif part['type']=='link':pdf.link(part['text']+' · '+part['url'],part['url'])
        elif part['type']=='evidence':
            pdf.text(part['event_id']+' · '+part['text'],8.5,gap=6)
            if part.get('url'):pdf.link(part['url'],part['url'],7.5)
        else:pdf.text(part['text'],9.4,gap=8)
    pdf.new_page('Cobertura');pdf.heading('Cobertura por servicio')
    for r in sm['source_counts']:pdf.text(f"{r['family']} / {r['channel']}: {r['count']:,}",8.5,gap=3)
    pdf.new_page('Cronología');parent=pdf.heading('Cronología completa de observaciones')
    pdf.text('Orden global por instante UTC ascendente; visualización en México. Registros de una misma hora conservan sus distintas fuentes. Datos de instalación, actualización o vencimiento no se presentan como acciones de navegación.',9,MUTED)
    day=None;month=None
    for i,r in enumerate(events):
        d=r['time_local'][:10]
        if d!=day:
            pdf.ensure(80)
            if d[:7]!=month:
                month=d[:7];pdf.heading(month,15,parent=parent)
            pdf.heading(d,11,bookmark=False);day=d
        pdf.event(r)
        if (i+1)%5000==0:print(f'Cronología: {i+1}/{len(events)}; página {pdf.page}',flush=True)
    pdf.new_page('Empresas e identificadores');pdf.heading('Catálogo de entidades e identificadores')
    pdf.text('El ID en el encabezado y los IDs dentro de los eventos se muestran por separado. El sufijo de archivo no se interpreta como un ID de empresa.',9,MUTED)
    for b in read('datos/facebook-empresas-identificadores.json'):
        pdf.ensure(65);pdf.text(b['name'],10,bold=True,gap=2)
        pdf.text('Identificador de entidad: '+b['business_id']+'\nIdentificadores dentro de eventos: '+', '.join(b['event_identifiers'])+'\nSufijo de archivo: '+b['filename_suffix'],8.3,gap=2)
        pdf.link(b['source_code']+' · '+b['source_path'],Path(b['source_path']).as_uri(),7.1)
    pdf.new_page('Archivos files');pdf.heading('Inventario de la carpeta files')
    pdf.text('179 PNG de archivos creados de IA, logo de Facebook y foto de perfil. La cronología incluye las fechas de creación disponibles; no se asigna fecha a los dos recursos visuales.',9,MUTED)
    for a in read('datos/facebook-files-inventario.json'):
        reference=a['reference'];stamp=reference['time_local'] if reference else 'sin fecha documentada'
        pdf.text(f"{a['name']} · {a['format']} · {a['bytes']} bytes · {stamp}",8.3,gap=1)
        pdf.link(a['path'],Path(a['path']).as_uri(),7.2)
        pdf.text('SHA-256: '+a['sha256'],6.5,MUTED,gap=1)
        if reference:pdf.text('Origen: '+reference['reference_source']+' · '+json.dumps(reference['locator'],ensure_ascii=False),6.5,MUTED,gap=5)
    pdf.new_page('Metadatos de imágenes');pdf.heading('Fuentes de la revisión de metadatos de imágenes')
    pdf.text('Lectura de 289 imágenes sin cambios en originales. La fecha de modificación del archivo no se usa como fecha de captura o de publicación. El detalle íntegro está en privado/imagenes-metadatos.json.',9,MUTED)
    for r in read('privado/imagenes-metadatos.json'):
        pdf.ensure(50);pdf.link(r['path'],Path(r['path']).as_uri(),7.2)
        pdf.text(f"{r['format']} · {r['width']}×{r['height']} · {r['bytes']} bytes · EXIF: "+json.dumps(r['exif'],ensure_ascii=False),7.3,gap=1)
        pdf.text('Otros campos: '+', '.join(r['other_metadata'])+(' · Software='+str(r['other_metadata']['Software']) if 'Software' in r['other_metadata'] else ''),7.1,gap=1)
        pdf.text('SHA-256: '+r['sha256'],6.4,MUTED,gap=5)
    pdf.new_page('Relaciones automáticas');pdf.heading('Relaciones automáticas propuestas')
    pdf.text('Criterios: misma URL y hasta dos segundos entre fuentes Google; o igualdad de nombre, identificador de evento, tipo y minuto entre detalle y resumen de Meta. Son relaciones para revisar, no hechos nuevos añadidos al historial.',9,MUTED)
    for r in read('datos/actividad-correlaciones.json'):
        pdf.text(' ↔ '.join(r['event_ids'])+' · '+r['type']+(f" · {r['seconds']:.6f} s" if 'seconds' in r else ''),7.6,gap=4)
    pdf.new_page('Sin fecha');pdf.heading('Secciones sin fecha documentada')
    pdf.text('Estos bloques se mantienen fuera de la cronología. En su mayoría son metadatos de grupo: foto y estado del enlace de invitación.',9,MUTED)
    for r in read('privado/actividad-sin-fecha-original.json'):
        pdf.text(r['id']+' · '+r['subject'],8.5)
        pdf.text(r['source_code']+' · '+json.dumps(r['locator'],ensure_ascii=False),7.1,MUTED)
    pdf.new_page('Referencias web');pdf.heading('Referencias web consultadas durante la investigación')
    current=read('datos/fuentes-web.json')
    for r in current['consulted_sources']:
        pdf.text(r['id']+' · '+r['title'],10,bold=True);pdf.link(r['url'],r['url'],7.6)
        pdf.text(r['relationship']+' '+r['notes']+' Consulta: '+r['consulted_on'],8.5)
    for i,r in enumerate(read('datos/imagen-validacion-fuentes-web.json'),1):
        pdf.text(f'I{i:02} · '+r['role'],9,bold=True);pdf.link(r['url'],r['url'],7.6);pdf.text(r['summary'],8.5)
    for r in read('datos/facebook-google-fuentes-web.json'):
        pdf.text(r['id']+' · '+r['title'],10,bold=True);pdf.link(r['url'],r['url'],7.6)
        pdf.text(r['status']+' · '+r['relationship']+' '+r['notes']+' Consulta: '+r['consulted_on'],8.5)
    for r in read('datos/pistas-fuentes-web.json'):
        pdf.text(r['id']+' · '+r['title'],10,bold=True);pdf.link(r['url'],r['url'],7.6)
        pdf.text(r['status']+' · '+r['relationship']+' '+r['notes']+' Consulta: '+r['consulted_on'],8.5)
    pdf.heading('Consultas y accesos que no dieron evidencia',13)
    for r in current['research_search_queries']:pdf.text(json.dumps(r,ensure_ascii=False) if isinstance(r,dict) else r,8)
    for r in read('datos/pistas-consultas-web.json'):pdf.text(r,8)
    for r in current['unavailable_attempts']:pdf.link(r['url'],r['url'],7.2);pdf.text(r['status'],8)
    pdf.new_page('Catálogo local');pdf.heading('Catálogo de archivos fuente')
    pdf.text('Cada S corresponde a un archivo consultado. El contador se refiere a registros extraídos de él; cero puede indicar configuración, inventario o ausencia de fechas reconocibles. La huella permite comprobar que el original no se modificó.',9,MUTED)
    for s in read('datos/catalogo-fuentes.json'):
        pdf.ensure(52);pdf.text(f"{s['code']} · {s['family']} · {s['records']} registros · {s['bytes']} bytes",8.7,bold=True,gap=1)
        pdf.link(s['path'],Path(s['path']).as_uri(),7.2)
        pdf.text('SHA-256: '+s['sha256'],6.4,MUTED,gap=5)
        if s.get('parse_note'):pdf.text(s['parse_note'],7.3,MUTED)
    pdf.heading('Referencias adicionales: contactos vCard',13)
    for s in read('datos/numero-6850175308-evidencias.json')['sources']:
        pdf.link(s['code']+' · '+s['path'],Path(s['path']).as_uri(),7.2)
        pdf.text('SHA-256: '+s['sha256'],6.5,MUTED)
    previous_log(pdf)
    pdf.close();os.chmod(temp,0o600);temp.replace(target)
    manifest={'generated_at_utc':datetime.now(timezone.utc).isoformat(),'pdf_path':str(target),'pages':pdf.page,
              'events_rendered':len(pdf.event_pages),'expected_events':len(events),
              'event_ids_complete':set(pdf.event_pages)=={r['id'] for r in events},
              'pdf_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
              'timeline_json_sha256':hashlib.sha256((OUT/'datos/actividad-cronologica.json').read_bytes()).hexdigest(),
              'timeline_page_by_event':pdf.event_pages}
    p=OUT/'datos/pdf-manifiesto.json';p.write_text(json.dumps(manifest,ensure_ascii=False,indent=2));os.chmod(p,0o600)
    print(json.dumps({k:v for k,v in manifest.items() if k!='timeline_page_by_event'},ensure_ascii=False),flush=True)

if __name__=='__main__':main()
