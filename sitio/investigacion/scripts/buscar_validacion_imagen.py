#!/usr/bin/env python3
"""Busca el recuerdo aproximado del usuario y conserva candidatos sin confirmarlos."""
import hashlib
import importlib.util
import json
import os
import re
import unicodedata
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit, urlunsplit

OUT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('extraer', OUT / 'scripts/extraer.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')


def save(name, value):
    p = OUT / name
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n' if not isinstance(value, str) else value,
                 encoding='utf-8')
    os.chmod(p, 0o600)


def public_url(s):
    if not s:
        return None
    u = urlsplit(m.canonical(s))
    if u.hostname in ('www.google.com', 'google.com') and u.path == '/search':
        from urllib.parse import urlencode
        return urlunsplit((u.scheme, u.netloc, u.path, urlencode({'q': parse_qs(u.query).get('q', [''])[0]}), ''))
    return urlunsplit((u.scheme, u.netloc, u.path, '', ''))


validate = re.compile(r'valid|verifi|comprob|captch|selfie|biometr|facial|autenti|identidad|confirm', re.I)
image = re.compile(r'imagen|image|imajen|foto|photo|picture|screenshot|captura|camera|camara|\bqr\b', re.I)
speed = re.compile(r'rapi|quick|fast|facil|simpl|agil', re.I)
corpus = {}
source_manifest = []
audit = []
combined = []
for path in sorted((m.ROOT / 'Mi actividad').glob('*/MiActividad.html')):
    rel = str(path.relative_to(m.ROOT))
    data = path.read_bytes()
    p = m.Activity(rel)
    p.feed(data.decode('utf-8'))
    corpus[rel] = p.records
    kinds = Counter(r['kind'] for r in p.records)
    query_hits = Counter()
    for r in p.records:
        if r['kind'] != 'consulta':
            continue
        s = norm(r['title_or_query'])
        has_v, has_i, has_s = bool(validate.search(s)), bool(image.search(s)), bool(speed.search(s))
        query_hits['verification_or_validation'] += has_v
        query_hits['image_or_photo'] += has_i
        query_hits['speed_or_ease'] += has_s
        if has_v and has_i:
            combined.append(r)
    audit.append({'source': rel, 'records': len(p.records), 'classification_counts': dict(kinds),
                  'query_keyword_counts': dict(query_hits)})
    source_manifest.append({'path': str(path), 'relative_path': rel, 'bytes': len(data),
                            'sha256': hashlib.sha256(data).hexdigest()})

selected = []
for rel, rows in corpus.items():
    for r in rows:
        reason = None
        if rel == 'Mi actividad/Búsqueda/MiActividad.html' and 'Hiciste una búsqueda con una imagen' in r['action']:
            reason = 'Búsqueda mediante imagen; no conserva pregunta o enlace de resultado ni identifica una validación.'
        elif rel == 'Mi actividad/Google Lens/MiActividad.html':
            reason = 'Actividad de Lens; no demuestra verificación ni rapidez.'
        elif rel == 'Mi actividad/Ayuda/MiActividad.html':
            path = urlsplit(r['url'] or '').path
            if path.endswith('/7162782'):
                reason = 'Visita sobre verificar identidad; candidata temática, sin prueba de validación con una imagen.'
            elif path.endswith('/7026266'):
                reason = 'Visita sobre confirmar acceso con mensajes de Google; candidata por tema de verificación, no por imágenes.'
        elif rel == 'Mi actividad/Chrome/MiActividad.html' and r['title_or_query'] == 'Verifica que eres tú':
            reason = 'Pantalla de verificación; ruta challenge/pwd. No identifica un procedimiento con imagen.'
        if reason:
            selected.append({**r, 'classification_note': reason})

history_path = m.ROOT / 'Chrome/Historial.json'
raw = history_path.read_bytes()
source_manifest.append({'path': str(history_path), 'relative_path': 'Chrome/Historial.json',
                        'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
history = json.loads(raw)
for i, item in enumerate(history['Browser History'], 1):
    if item['title'] == 'Verifica que eres tú':
        dt = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=int(item['time_usec']))
        selected.append({'source': 'Chrome/Historial.json', 'record_index_1based': i,
                         'json_pointer': '/Browser History/' + str(i - 1), 'kind': 'visita',
                         'title_or_query': item['title'], 'time_local': dt.astimezone(m.ZONE).isoformat(),
                         'time_utc': dt.isoformat(), 'url': item['url'], 'url_original': item['url'],
                         'classification_note': 'Corrobora la pantalla registrada en actividad Chrome, sin identificar una imagen.'})

assets = []
for p in sorted((m.ROOT / 'Mi actividad/Google Lens').glob('*.jpg')):
    assets.append({'path': str(p), 'relative_path': str(p.relative_to(m.ROOT)), 'bytes': p.stat().st_size,
                   'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                   'review': 'Inspección visual: página de lectura literaria en inglés; no contiene instrucciones de validación de cuenta, CAPTCHA ni documentos de identidad.'})

safe = []
for r in selected:
    title = r['title_or_query']
    if title.startswith('http'):
        title = public_url(title)
    safe.append({'source': r['source'], 'record_index_1based': r['record_index_1based'],
                 'html_line_1based': r.get('html_line_1based'), 'html_column_0based': r.get('html_column_0based'),
                 'json_pointer': r.get('json_pointer'), 'kind': r['kind'], 'title_or_query': title,
                 'time_local': r['time_local'], 'url_public': public_url(r.get('url')),
                 'classification_note': r['classification_note']})
safe.sort(key=lambda r: (r.get('time_local') or '', r['source']))
save('privado/imagen-validacion-evidencias-originales.json', selected)
save('datos/imagen-validacion-evidencias.json', safe)
save('datos/imagen-validacion-auditoria.json',
     {'request': 'Ahora en las busquedas busca algo sobre como se puede validar con una imagen mas rapido o algo asi',
      'activity_files_scanned': len(audit), 'activity_audit': audit,
      'explicit_search_queries_combining_validation_and_image': len(combined),
      'combined_matches': combined, 'original_source_manifest': source_manifest,
      'lens_image_assets_reviewed': assets, 'history_records_scanned': len(history['Browser History']),
      'result': 'No se identificó la consulta recordada. Se conservaron candidatos temáticos y búsquedas por imagen como pistas sin confirmar.',
      'user_followups': ['OK', 'OK'], 'clarification': 'Se preguntó qué se quería validar: identidad/cuenta, CAPTCHA o información/objetos. El usuario no especificó una opción.',
      'pdf_created': False})

web_sources = [
    {'url': 'https://support.google.com/accounts/answer/7162782?hl=es-419',
     'role': 'Página cuyo destino aparece en la actividad del 29-08-2026. Se leyó su contenido actual.',
     'summary': 'Describe verificar identidad para acciones sensibles. El texto actual menciona documentos de identidad vinculados y, en otro apartado, acelerar la confianza en métodos con llaves de acceso o seguridad. No establece un método más rápido mediante una imagen.'},
    {'url': 'https://support.google.com/accounts/answer/7026266?hl=es-419',
     'role': 'Página cuyo destino aparece en la actividad del 11-09-2026. Se leyó su contenido actual.',
     'summary': 'Describe confirmar el acceso con notificaciones en el teléfono; no es un procedimiento de validación con imágenes.'},
    {'url': 'https://support.google.com/accounts/answer/16761564',
     'role': 'Enlace seguido desde el artículo sobre verificar identidad. No se encontró como visita en Búsqueda, Chrome o Ayuda.',
     'summary': 'El acceso redirigió al índice de información general de seguridad, topic/7189123; no permitió comprobar el artículo de documento de identidad.'},
    {'url': 'https://support.google.com/accounts/answer/7684753',
     'role': 'Enlace seguido desde el apartado de acelerar la confianza. No se encontró como visita en Búsqueda, Chrome o Ayuda.',
     'summary': 'La página actual explica acelerar la confianza con una llave previamente confiable y que los mensajes al teléfono son más rápidos que introducir un código. No describe una validación con una imagen.'},
]
for s in web_sources:
    s['consulted_on'] = '2026-10-01'
save('datos/imagen-validacion-fuentes-web.json', web_sources)

block = '''
<!-- INICIO_RESULTADOS_SESION_2 -->
## Sesión 2: búsqueda aproximada sobre validar con una imagen más rápido

Solicitud: «Ahora en las busquedas busca algo sobre como se puede validar con una imagen mas rapido o algo asi».

Se examinaron los 874 registros de Búsqueda (382 consultas explícitas), 50 registros de Búsqueda de imágenes, 14 de Google Lens y 16 de Modo IA. Se amplió la revisión a los 27 archivos HTML de Mi actividad, las 1.182 entradas de Browser History y tres imágenes JPG locales asociadas a Lens. Se buscaron variantes en español e inglés: validar/verificar/comprobar, imagen/foto/captura, rápido/fácil, CAPTCHA, identidad, selfie, reconocimiento, QR y escaneo. Se normalizaron acentos y se examinaron fechas y enlaces.

**Resultado:** no se encontró una consulta explícita que combinara validación/verificación con una imagen, ni se identificó el procedimiento más rápido que recuerda el usuario. No se eligió una interpretación de «validar» sin evidencia. Los dos «OK» recibidos no especifican qué se quería validar.

### Pistas conservadas, sin confirmar

| Fecha y hora de México | Registro | Referencia |
|---|---|---|
| 29-08-2026 03:06:47 | Visita a «Verifica tu identidad cuando completes una acción sensible» | Mi actividad/Ayuda #707; [Google](https://support.google.com/accounts/answer/7162782?hl=es-419) |
| 11-09-2026 09:35:33 | Visita a «Accede a tu cuenta con los mensajes de Google» | Mi actividad/Ayuda #530; [Google](https://support.google.com/accounts/answer/7026266?hl=es-419) |
| 26-09-2026 22:33:14 | «Verifica que eres tú», ruta de contraseña challenge/pwd | Mi actividad/Chrome #8 y Browser History #44; el enlace original con parámetros se conserva en privado |
| 26-09-2026 02:04:13 | Dos registros de búsqueda con Google Lens | Mi actividad/Google Lens #1 y #2; sin pregunta ni imagen adjunta conservadas en esos registros |
| 06-08-2026 07:33:49 y 13:26:25 | Quince registros «Hiciste una búsqueda con una imagen» | Mi actividad/Búsqueda #627–641; sin consulta textual ni enlace de resultados que expliquen qué se validaba |

Las tres imágenes JPG guardadas de Lens, del 27-08-2026, se inspeccionaron visualmente: son páginas de lectura literaria en inglés. Se descartaron como evidencia de una verificación con imagen. Se conservaron sus rutas y huellas, sin transcribir el libro.

El artículo de identidad encontrado en el historial menciona actualmente documentos vinculados y un apartado para acelerar la confianza en métodos de autenticación; ese apartado remite al uso de llaves ya confiables. Esto no prueba un método más rápido con una imagen, ni que el contenido actual sea idéntico al visto en agosto. [Guía de identidad](https://support.google.com/accounts/answer/7162782?hl=es-419), [guía adicional consultada hoy](https://support.google.com/accounts/answer/7684753).

La otra visita corresponde a confirmar acceso mediante notificaciones de Google. Se mantiene como candidato temático, sin atribuirle relación con imágenes. [Guía de mensajes de Google](https://support.google.com/accounts/answer/7026266?hl=es-419).

Se siguió también el enlace al artículo de documento de identidad `answer/16761564`; redirigió a un índice general de seguridad, por lo que no se pudo comprobar su contenido. Las dos páginas derivadas de esta lectura actual no se encontraron como visitas en los historiales de Búsqueda, Chrome o Ayuda revisados.

### Evidencias y continuación

- `datos/imagen-validacion-evidencias.json`: candidatos, fechas, enlaces públicos y localizadores.
- `privado/imagen-validacion-evidencias-originales.json`: texto y enlaces originales; incluye parámetros de las pantallas de acceso.
- `datos/imagen-validacion-auditoria.json`: alcance, variantes buscadas, conteos y SHA-256 de los archivos consultados.
- `datos/imagen-validacion-fuentes-web.json`: cuatro destinos consultados hoy y su relación con las visitas históricas.
- `scripts/buscar_validacion_imagen.py`: procedimiento reproducible.

La pista permanece sin identificar. La aclaración solicitada fue si se quería validar una cuenta/identidad, un CAPTCHA o información/objetos. No se generó PDF.
<!-- FIN_RESULTADOS_SESION_2 -->
'''
path = OUT / 'registro.md'
old = path.read_text()
start = old.find('<!-- INICIO_RESULTADOS_SESION_2 -->')
end_marker = '<!-- FIN_RESULTADOS_SESION_2 -->'
if start >= 0:
    end = old.index(end_marker, start) + len(end_marker)
    old = old[:start] + block.strip() + old[end:]
else:
    old += block
save('registro.md', old)
for source in source_manifest:
    assert hashlib.sha256(Path(source['path']).read_bytes()).hexdigest() == source['sha256']
os.chmod(Path(__file__), 0o600)
print(json.dumps({'activity_files_scanned': len(audit), 'validation_and_image_queries': len(combined),
                  'candidate_observations_saved': len(selected), 'images_reviewed': len(assets),
                  'sources_unchanged': len(source_manifest), 'pdf_created': False}, ensure_ascii=False))
