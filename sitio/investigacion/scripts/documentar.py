#!/usr/bin/env python3
"""Documenta el cruce y conserva fuentes y límites de cada hallazgo."""
import hashlib
import json
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

OUT = Path(__file__).resolve().parents[1]


def save(name, value):
    p = OUT / name
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n' if not isinstance(value, str) else value,
                 encoding='utf-8')
    os.chmod(p, 0o600)


evidence = json.loads((OUT / 'datos/evidencias.json').read_text())
metadata = json.loads((OUT / 'datos/clave-metadatos.json').read_text())[0]
sources = json.loads((OUT / 'datos/fuentes-locales.json').read_text())
summary = json.loads((OUT / 'datos/resumen.json').read_text())
groups = defaultdict(list)
for r in evidence:
    p = urlsplit(r['url'])
    key = r['url'] if r['kind'] == 'consulta' else urlunsplit((p.scheme, p.netloc, p.path, '', ''))
    groups[key].append(r)
cross = []
for url, rows in groups.items():
    times = [datetime.fromisoformat(r['time_local']) for r in rows]
    chosen = next((r for r in rows if r['source'] == 'Chrome/Historial.json'), rows[0])
    item = {'kind': rows[0]['kind'], 'url': chosen['url'],
            'title_or_query': chosen['title_or_query'],
            'time_first_local': min(times).isoformat(), 'time_last_local': max(times).isoformat(),
            'observations': [{'source': r['source'], 'record_index_1based': r['record_index_1based'],
                              'json_pointer': r.get('json_pointer'), 'time_local': r['time_local'],
                              'url_original': r['url_original']} for r in rows]}
    if item['kind'] == 'visita':
        assert len(rows) == 3
        assert max(times).timestamp() - min(times).timestamp() < 2
        item['correlation_basis'] = 'Misma URL de destino sin envoltorios de Google ni parámetro de idioma; intervalo menor de dos segundos.'
    else:
        item['correlation_basis'] = 'Consulta explícita registrada en Mi actividad/Búsqueda; no aparece como consulta en Browser History.'
    cross.append(item)
save('datos/cruce.json', cross)

web = [
    {'id': 'W01', 'title': 'El protocolo de envío web — web.dev',
     'url': 'https://web.dev/articles/push-notifications-web-push-protocol?hl=es-419',
     'relationship': 'Visita histórica encontrada y lectura actual realizada.',
     'notes': 'Explica claves del servidor, JWT, suscripciones y cifrado. Algunos ejemplos usan encabezados y aesgcm de una versión anterior; contrastarlos con W03 y W04.'},
    {'id': 'W02', 'title': 'Web Push Notifications through VAPID method — Carlos Ribeiro, bawilabs',
     'url': 'https://medium.com/bawilabs/web-push-notifications-through-vapid-method-7d4d6927a006',
     'relationship': 'Visita histórica encontrada; se confirmó título, autor y fecha de publicación.',
     'notes': 'Publicado el 20 de noviembre de 2018. Referencia histórica del recorrido del usuario; las explicaciones técnicas de este registro se fundamentan en fuentes primarias.'},
    {'id': 'W03', 'title': 'RFC 8292 — Voluntary Application Server Identification (VAPID) for Web Push',
     'url': 'https://www.rfc-editor.org/rfc/rfc8292.html',
     'relationship': 'Referencia primaria adicional consultada durante esta investigación; no es una visita recuperada del historial.',
     'notes': 'Define identificación del servidor con JWT y ECDSA P-256/ES256, aud/exp y el esquema Authorization: vapid con parámetros t y k.'},
    {'id': 'W04', 'title': 'RFC 8291 — Message Encryption for Web Push',
     'url': 'https://www.rfc-editor.org/rfc/rfc8291.html',
     'relationship': 'Referencia primaria adicional consultada durante esta investigación.',
     'notes': 'Explica cifrado de extremo a extremo, ECDH, secreto de autenticación de suscripción y aes128gcm. Separa el cifrado de la identificación VAPID.'},
    {'id': 'W05', 'title': 'Chromium — SharingSyncPreference, versión 137.0.7151.130',
     'url': 'https://chromium.googlesource.com/chromium/src/%2B/refs/tags/137.0.7151.130/components/sharing_message/sharing_sync_preference.cc',
     'relationship': 'Código primario consultado para interpretar el campo encontrado; no procede del historial personal.',
     'notes': 'GetVapidKey decodifica vapid_private_key desde Base64; SetVapidKey guarda esa clave y vapid_creation_timestamp. El componente administra preferencias sharing, datos FCM y dispositivos sincronizados.'},
    {'id': 'W06', 'title': 'Chromium — nombre de preferencia sharing.vapid_key',
     'url': 'https://chromium.googlesource.com/chromium/src/%2B/a73140559ea8872c19acf6d190aacf1a46eef99b/chrome/common/pref_names.h',
     'relationship': 'Resultado de búsqueda primaria revisado para identificar el nombre de preferencia.',
     'notes': 'Declara kSharingVapidKey con el nombre sharing.vapid_key; la interpretación detallada se apoya en W05.'},
    {'id': 'W07', 'title': 'Chromium — SharingSyncPreference, revisión c18a333f',
     'url': 'https://chromium.googlesource.com/chromium/src/%2B/c18a333f058a6f3a60dfc635b08f29fa6b4e7f81/chrome/browser/sharing/sharing_sync_preference.cc',
     'relationship': 'Resultado de búsqueda primaria revisado; posteriormente se abrió W05.',
     'notes': 'El fragmento encontrado relaciona vapid_private_key y vapid_creation_timestamp con preferencias sharing.'},
    {'id': 'W08', 'title': 'Chromium — SharingSyncPreference, revisión cd9d08a4',
     'url': 'https://chromium.googlesource.com/chromium/src/%2B/cd9d08a4c4086bdac4d36c313e2b785776e8377d/chrome/browser/sharing/sharing_sync_preference.cc',
     'relationship': 'Resultado de búsqueda primaria revisado.',
     'notes': 'Implementación adicional de las funciones de almacenamiento de VAPID.'},
    {'id': 'W09', 'title': 'Chromium experimental — SharingSyncPreference, versión 82.0.4053.0',
     'url': 'https://chromium.googlesource.com/experimental/chromium/src/%2B/refs/tags/82.0.4053.0/chrome/browser/sharing/sharing_sync_preference.cc',
     'relationship': 'Resultado de búsqueda primaria revisado.',
     'notes': 'Referencia histórica; no se utiliza para afirmar la versión de Chrome de esta cuenta.'},
]
for source in web:
    source['consulted_on'] = '2026-10-01'
attempts = [
    'https://chromium.googlesource.com/chromium/src/+/refs/heads/main/chrome/browser/sharing/sharing_vapid_key_manager.cc',
    'https://chromium.googlesource.com/chromium/src/+/refs/heads/main/chrome/browser/sharing/sharing_sync_preference.cc',
    'https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/sharing_message/sharing_vapid_key_manager.h',
    'https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/sharing_message/sharing_sync_preference.cc',
    'https://chromium.googlesource.com/chromium/src/+/refs/heads/main/components/sharing_message/sharing_vapid_key_manager.cc',
    'https://chromium.googlesource.com/chromium/src/+/refs/tags/137.0.7151.130/components/sharing_message/sharing_vapid_key_manager.h',
    'https://chromium.googlesource.com/chromium/src/+/refs/tags/137.0.7151.130/components/sharing_message/sharing_vapid_key_manager.cc',
    'https://chromium.googlesource.com/chromium/src/+/refs/tags/137.0.7151.130/base/json/values_util.cc',
]
queries = [
    'site:chromium.googlesource.com "sharing.vapid_key"',
    'site:chromium.googlesource.com "vapid_private_key" sharing',
    'site:chromium.googlesource.com/chromium/src "vapid_private_key"',
    'site:chromium.googlesource.com/chromium/src "SharingVapidKeyManager"',
    'site:chromium.googlesource.com/chromium/src "kVapidCreationTimestamp"',
]
save('datos/fuentes-web.json', {'consulted_sources': web, 'research_search_queries': queries,
                               'unavailable_attempts': [{'url': u, 'status': 'La herramienta web no pudo acceder; no se usa como evidencia.'} for u in attempts]})

lines = ['\n<!-- INICIO_RESULTADOS_SESION_1 -->\n', '## Hallazgos y cruce verificado\n',
         f'Se inventariaron {len(json.loads((OUT / "datos/inventario-google.json").read_text()))} archivos Google. '
         'La búsqueda textual se amplió a notificaciones push, PushSubscription, PushManager y Firebase Cloud Messaging. '
         'El tema aparece en cuatro fuentes Google: los dos archivos de actividad, Historial.json y Configuración.json.\n',
         f'Se revisaron {summary["search_activity_records"]} registros de Búsqueda, '
         f'{summary["chrome_activity_records"]} registros de actividad Chrome y '
         f'{summary["browser_history_records"]} entradas de Browser History. '
         'Resultado: dos consultas explícitas y dos destinos visitados, con ocho observaciones. '
         'No hubo coincidencias en la sección Session.\n',
         'Todos los horarios de la tabla son del **26 de septiembre de 2026**, America/Mexico_City (UTC−06:00).\n',
         '| Hora | Acción y enlace | Evidencia |\n|---|---|---|']
for item in cross:
    t = datetime.fromisoformat(item['time_first_local']).strftime('%H:%M:%S')
    refs = '; '.join(f'{r["source"]} #{r["record_index_1based"]}' for r in item['observations'])
    label = item['title_or_query'].replace('|', '—')
    lines.append(f'| {t} | {item["kind"]}: [{label}]({item["url"]}) | {refs} |')
lines += [
    '\nEl clic hacia la traducción de Medium quedó registrado a las 22:28:39 y la visita de Chrome a las 22:28:40.163036. '
    'El clic hacia web.dev quedó registrado a las 22:28:55 y la visita de Chrome a las 22:28:56.599891. '
    'La coincidencia de destino y ese intervalo respaldan el cruce; los registros prueban búsquedas y visitas, sin demostrar que se leyera todo el contenido.\n',
    'Las expresiones «vapid» y «vapid web push» son las consultas exactas recuperadas; no se encontraron preguntas más extensas sobre este tema. '
    'Los enlaces originales de Google Translate y las redirecciones de Google se conservan en `datos/evidencias.json`, junto con el texto original y la ubicación del registro.\n',
    '## Clave recuperada y contraseñas\n',
    f'- Fuente: `{metadata["source"]}`.\n- Localizador: `{metadata["locator"]}`.\n'
    '- Preferencia: `sharing.vapid_key`; campo: `vapid_private_key`.\n'
    '- El valor es una clave privada EC P-256, DER codificado en Base64 (138 bytes). La carga y una firma/verificación local fueron correctas.\n'
    f'- Fecha guardada de creación: `{metadata["created_local"]}`; UTC: `{metadata["created_utc"]}`.\n'
    '- Conversión de la fecha: microsegundos desde 1601-01-01 UTC, formato interno de tiempo de Chromium. Se preserva también el número original.\n'
    f'- Huella SHA-256 de la clave pública: `{metadata["public_key_sha256"]}`.\n',
    'La ubicación de la clave y el componente de Chromium que administra esta preferencia la vinculan con el sistema interno de compartir de Chrome. '
    '[Código de Chromium consultado](https://chromium.googlesource.com/chromium/src/%2B/refs/tags/137.0.7151.130/components/sharing_message/sharing_sync_preference.cc). '
    'La exportación no permite identificarla como una clave de un servicio Web Push propio, y no aporta su endpoint de suscripción, claves p256dh/auth ni el servidor de una aplicación propia. '
    'Su fecha de creación antecede a las búsquedas; no hay evidencia de que esas consultas la generaran.\n',
    'El valor completo y las representaciones derivadas están en [claves-recuperadas.md](privado/claves-recuperadas.md), '
    '[vapid-recuperada.json](privado/vapid-recuperada.json) y [vapid-private.pem](privado/vapid-private.pem). '
    'Estos archivos tienen permisos 0600 y el directorio, 0700.\n',
    'No se encontró un archivo de exportación de contraseñas en el inventario Google. '
    'Los historiales revisados no contienen valores de contraseñas de inicio de sesión recuperables. '
    'El campo `password_state` de Session contiene estados (`HAS_PASSWORD_FIELD`, `NO_PASSWORD_FIELD`, `PASSWORD_STATE_UNKNOWN`); esos estados no guardan la contraseña introducida. '
    'No se realizaron inicios de sesión ni cambios de cuenta.\n',
    '## Segunda carpeta\n',
    'En Facebook no se encontraron menciones explícitas de VAPID/Web Push. La búsqueda ampliada encontró cinco archivos con etiquetas genéricas de notificaciones push '
    '(configuración, índice y estadísticas). Se documentan sus rutas, huellas y contextos limitados en `datos/facebook-notificaciones-genericas.json`; no prueban una suscripción Web Push ni aportan claves VAPID.\n',
    '## Lectura para aprender\n',
    'VAPID identifica al servidor de aplicaciones ante el servicio push mediante un JWT firmado con su clave privada P-256; la clave pública permite verificarlo. '
    '[RFC 8292](https://www.rfc-editor.org/rfc/rfc8292.html). '
    'La suscripción aporta un destino (`endpoint`) y material `p256dh`/`auth` para el cifrado del mensaje. '
    '[RFC 8291](https://www.rfc-editor.org/rfc/rfc8291.html).\n',
    'Para estudiar a partir de tus visitas, empieza por [web.dev](https://web.dev/articles/push-notifications-web-push-protocol?hl=es-419) '
    'y conserva [el artículo de Medium](https://medium.com/bawilabs/web-push-notifications-through-vapid-method-7d4d6927a006) como referencia de tu recorrido. '
    'Los ejemplos de web.dev muestran `Authorization: WebPush`, `Crypto-Key` y `aesgcm`; para una implementación, contrastar el esquema `vapid` de RFC 8292 '
    'y `aes128gcm` de RFC 8291.\n',
    'Preguntas propuestas para estudiar (no son consultas recuperadas del historial):\n\n'
    '1. ¿Qué relación hay entre Web Push, el servicio push y el service worker?\n'
    '2. ¿Para qué se usan la clave pública y la clave privada VAPID?\n'
    '3. ¿Qué representan endpoint, p256dh y auth en una suscripción?\n'
    '4. ¿Cómo se identifica al servidor y cómo se cifra un mensaje?\n'
    '5. ¿Cómo distinguir una clave interna de Chrome de una clave de una aplicación propia?\n',
    '## Fuentes locales y trazabilidad\n',
    'Los números de registro son de base uno; los índices en los localizadores JSON son de base cero. '
    'En HTML se guarda además la línea y columna del comienzo de cada celda de actividad. '
    'Los originales no se modificaron.\n']
for i, s in enumerate(sources, 1):
    lines.append(f'- L{i:02}: `{s["path"]}` ({s["bytes"]} bytes). SHA-256: `{s["sha256"]}`.')
lines += ['\n## Fuentes web consultadas\n']
for s in web:
    lines.append(f'- {s["id"]}: [{s["title"]}]({s["url"]}). Consultada: {s["consulted_on"]}. {s["relationship"]} {s["notes"]}')
lines += ['\nLas cinco búsquedas externas y los ocho intentos de acceso sin resultado útil se conservan en `datos/fuentes-web.json`. '
          'Los enlaces añadidos para verificar conceptos se distinguen de los dos artículos encontrados en tu historial.\n',
          '## Archivos de trabajo y continuación\n',
          '- `datos/evidencias.json`: ocho observaciones, texto original, fechas, URLs originales y localizadores.\n'
          '- `datos/cruce.json`: cuatro eventos con sus referencias y criterio de correlación.\n'
          '- `datos/cronologia.csv`: cronología para consultar en una hoja de cálculo.\n'
          '- `datos/fuentes-locales.json` y `datos/fuentes-web.json`: referencias y procedencia.\n'
          '- `datos/clave-metadatos.json`: descripción verificable de la clave, sin su valor privado.\n'
          '- `datos/inventario-google.json`: rutas y tamaños del conjunto Google.\n'
          '- `privado/`: valor completo de la clave recuperada y sus representaciones.\n'
          '- `scripts/extraer.py` y `scripts/documentar.py`: procedimientos reproducibles de extracción y documentación.\n',
          'En las siguientes intervenciones se añadirán aquí nuevos hallazgos, consultas y referencias. '
          'El PDF sigue pendiente para cuando el usuario indique que terminó la conversación.\n',
          '<!-- FIN_RESULTADOS_SESION_1 -->\n']
block = '\n'.join(lines)
p = OUT / 'registro.md'
old = p.read_text()
start = old.find('<!-- INICIO_RESULTADOS_SESION_1 -->')
end_marker = '<!-- FIN_RESULTADOS_SESION_1 -->'
if start >= 0:
    end = old.index(end_marker, start) + len(end_marker)
    old = old[:start] + block.strip() + old[end:]
else:
    old += block
save('registro.md', old)

for s in sources:
    assert hashlib.sha256(Path(s['path']).read_bytes()).hexdigest() == s['sha256']
for p in OUT.rglob('*'):
    if p.is_file():
        os.chmod(p, 0o600)
assert not list(OUT.rglob('*.pdf'))
print(json.dumps({'crossed_events': len(cross), 'evidence_records': len(evidence),
                  'original_sources_unchanged': len(sources), 'recovered_key_files_private': True,
                  'registro': str(OUT / 'registro.md'), 'pdf_created': False}, ensure_ascii=False))
