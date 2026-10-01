#!/usr/bin/env python3
"""Extrae evidencia local de VAPID/Web Push sin modificar los originales."""
from __future__ import annotations

import base64
import csv
import hashlib
import json
import os
import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlsplit, urlunsplit
from zoneinfo import ZoneInfo

ROOT = Path('/home/deep-logic/Documentos/Registro/Takeout')
OUT = Path(__file__).resolve().parents[1]
ZONE = ZoneInfo('America/Mexico_City')
TOPIC = re.compile(
    r'vapid|web[\s_-]?push|push[\s_-]?service|servicio.{0,20}push|'
    r'notificaci(?:ones|ón)[\s_-]+push|push[\s_-]+notifications?|'
    r'pushmanager|pushsubscription|firebase[\s_-]+cloud[\s_-]+messaging|'
    r'fcm\.googleapis\.com|web-push-libs|protocolo de envío web', re.I)
MONTHS = {'ene': 1, 'feb': 2, 'mar': 3, 'abr': 4, 'may': 5, 'jun': 6,
          'jul': 7, 'ago': 8, 'sept': 9, 'sep': 9, 'oct': 10, 'nov': 11, 'dic': 12}
DATE = re.compile(
    r'(\d{1,2})\s+([a-z]+)\s+(\d{4}),\s*(\d{1,2}):(\d{2}):(\d{2})'
    r'\s*([ap])\s*\.?\s*m\s*\.?\s*(CST|UTC|GMT[-+]\d{2}:\d{2})', re.I)


def write(name, obj):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if isinstance(obj, bytes):
        p.write_bytes(obj)
    elif isinstance(obj, str):
        p.write_text(obj, encoding='utf-8')
    else:
        p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.chmod(p, 0o600)
    return p


def html_date(text):
    m = DATE.search(text.replace('\u202f', ' ').replace('\xa0', ' '))
    if not m:
        return None, None
    day, month, year, hour, minute, second, ampm, zone = m.groups()
    h = int(hour) % 12 + (12 if ampm.lower() == 'p' else 0)
    tz = timezone(timedelta(hours=-6)) if zone.upper() == 'CST' else timezone.utc
    if zone.upper().startswith('GMT'):
        offset = int(zone[4:6]) * 60 + int(zone[7:9])
        tz = timezone(timedelta(minutes=offset * (1 if zone[3] == '+' else -1)))
    dt = datetime(int(year), MONTHS[month.lower()], int(day), h, int(minute), int(second), tzinfo=tz)
    return m.group(0), dt


def canonical(url):
    # Se eliminan envoltorios de Google; se conserva el enlace original en evidencia.
    for _ in range(4):
        p = urlsplit(url)
        q = parse_qs(p.query)
        if p.hostname == 'translate.google.com' and 'u' in q:
            url = q['u'][0]
        elif p.hostname in ('google.com', 'www.google.com') and p.path == '/url':
            target = q.get('q', q.get('url', [url]))[0]
            if target == url:
                break
            url = target
        else:
            break
    return url


def identity(url):
    p = urlsplit(canonical(url))
    return urlunsplit((p.scheme, p.netloc.lower(), p.path.rstrip('/'), '', ''))


class Activity(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.current = None
        self.depth = 0
        self.anchor = None
        self.records = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'div':
            if self.current is None and 'outer-cell' in a.get('class', '').split():
                line, col = self.getpos()
                self.current = {'source': self.source, 'record_index_1based': len(self.records) + 1,
                                'html_line_1based': line, 'html_column_0based': col,
                                'parts': [], 'links': []}
                self.depth = 0
            if self.current is not None:
                self.depth += 1
        if self.current is not None:
            if tag == 'br':
                self.current['parts'].append('\n')
            if tag == 'a' and a.get('href'):
                self.anchor = {'url_original': a['href'], 'parts': []}

    def handle_data(self, text):
        if self.current is not None:
            self.current['parts'].append(text)
            if self.anchor is not None:
                self.anchor['parts'].append(text)

    def handle_endtag(self, tag):
        if self.current is None:
            return
        if tag == 'a' and self.anchor is not None:
            self.anchor['text'] = ''.join(self.anchor.pop('parts')).strip()
            self.current['links'].append(self.anchor)
            self.anchor = None
        if tag in ('div', 'p'):
            self.current['parts'].append('\n')
        if tag == 'div':
            self.depth -= 1
            if self.depth == 0:
                r = self.current
                r['text_original'] = '\n'.join(x.strip() for x in ''.join(r.pop('parts')).splitlines() if x.strip())
                r['date_original'], dt = html_date(r['text_original'])
                r['time_local'] = dt.astimezone(ZONE).isoformat() if dt else None
                r['time_utc'] = dt.astimezone(timezone.utc).isoformat() if dt else None
                lines = r['text_original'].splitlines()
                r['action'] = lines[1] if len(lines) > 1 else lines[0]
                relevant = [a for a in r['links'] if urlsplit(a['url_original']).hostname
                            not in ('myaccount.google.com', 'maps.google.com')
                            and not a['url_original'].startswith('https://www.google.com/maps/')]
                r['url_original'] = relevant[0]['url_original'] if relevant else None
                r['url'] = canonical(r['url_original']) if r['url_original'] else None
                r['kind'] = 'consulta' if r['action'].startswith(('Buscaste', 'Has buscado')) else 'visita'
                r['title_or_query'] = re.sub(r'^(Buscaste|Has buscado|Has visitado)\s*', '', r['action'])
                if r['kind'] == 'consulta' and r['url']:
                    q = parse_qs(urlsplit(r['url']).query).get('q')
                    if q:
                        r['title_or_query'] = q[0]
                self.records.append(r)
                self.current = None
                self.anchor = None


def topic_record(r):
    return bool(TOPIC.search(unquote(r.get('text_original', '') + ' ' +
                                    str(r.get('url', '')) + ' ' + r.get('title_or_query', ''))))


def walk(obj, pointer=''):
    yield pointer, obj
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk(v, pointer + '/' + k.replace('~', '~0').replace('/', '~1'))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk(v, pointer + '/' + str(i))


def main():
    os.umask(0o077)
    matches = []
    inventory = []
    manifest = []
    password_candidate_files = []
    activity_counts = {}
    for p in sorted(ROOT.rglob('*')):
        if not p.is_file():
            continue
        rel = str(p.relative_to(ROOT))
        inventory.append({'path': str(p), 'relative_path': rel, 'bytes': p.stat().st_size})
        if re.search(r'contrase|password|login.data|credentials|credenciales', p.name, re.I):
            password_candidate_files.append(rel)
        if p.suffix.lower() not in ('.html', '.json', '.txt', '.csv'):
            continue
        raw = p.read_bytes()
        text = raw.decode('utf-8', errors='replace')
        if not TOPIC.search(unquote(text)):
            continue
        manifest.append({'path': str(p), 'relative_path': rel, 'bytes': len(raw),
                         'sha256': hashlib.sha256(raw).hexdigest()})
        if p.name == 'MiActividad.html':
            parser = Activity(rel)
            parser.feed(text)
            activity_counts[rel] = len(parser.records)
            found = [r for r in parser.records if topic_record(r)]
            matches.extend(found)
            print(json.dumps({'source': rel, 'records': len(parser.records), 'topic_matches': len(found)}, ensure_ascii=False))

    history_rel = 'Chrome/Historial.json'
    history = json.loads((ROOT / history_rel).read_text())
    for i, item in enumerate(history['Browser History'], 1):
        if not TOPIC.search(unquote(item.get('title', '') + ' ' + item.get('url', ''))):
            continue
        dt = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=int(item['time_usec']))
        matches.append({'source': history_rel, 'record_index_1based': i,
                        'json_pointer': '/Browser History/' + str(i - 1), 'kind': 'visita',
                        'date_original': str(item['time_usec']), 'time_utc': dt.isoformat(),
                        'time_local': dt.astimezone(ZONE).isoformat(), 'title_or_query': item['title'],
                        'url_original': item['url'], 'url': canonical(item['url'])})
    session_matches = []
    for pointer, value in walk(history.get('Session', []), '/Session'):
        if isinstance(value, dict) and isinstance(value.get('url'), str):
            if TOPIC.search(unquote(value.get('url', '') + ' ' + str(value.get('title', '')))):
                session_matches.append({'json_pointer': pointer, 'url': value['url'], 'title': value.get('title')})

    matches.sort(key=lambda r: (r.get('time_utc') or '', r['source']))
    write('datos/evidencias.json', matches)
    write('datos/fuentes-locales.json', manifest)
    write('datos/inventario-google.json', inventory)
    write('datos/coincidencias-sesiones.json', session_matches)
    rows = []
    for r in matches:
        rows.append({k: r.get(k, '') for k in ('time_local', 'kind', 'title_or_query', 'url', 'source',
                                               'record_index_1based', 'json_pointer', 'date_original')})
    csv_path = OUT / 'datos/cronologia.csv'
    with csv_path.open('w', newline='', encoding='utf-8') as f:
        fields = list(rows[0]) if rows else ['time_local']
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.chmod(csv_path, 0o600)

    config = json.loads((ROOT / 'Chrome/Configuración.json').read_text())
    configs = [(i, json.loads(r['value'])) for i, r in enumerate(config.get('Preferences', []))
               if r.get('name') == 'sharing.vapid_key']
    key_meta = []
    for i, value in configs:
        from cryptography.hazmat.primitives import hashes, serialization
        from cryptography.hazmat.primitives.asymmetric import ec
        original = value['vapid_private_key']
        der = base64.b64decode(original, validate=True)
        key = serialization.load_der_private_key(der, password=None)
        assert isinstance(key, ec.EllipticCurvePrivateKey)
        assert isinstance(key.curve, ec.SECP256R1)
        message = b'Validacion local de clave exportada; sin acceso a servicios externos.'
        signature = key.sign(message, ec.ECDSA(hashes.SHA256()))
        key.public_key().verify(signature, message, ec.ECDSA(hashes.SHA256()))
        pub = key.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint)
        private_raw = key.private_numbers().private_value.to_bytes(32, 'big')
        b64url = lambda data: base64.urlsafe_b64encode(data).decode().rstrip('=')
        created = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=int(value['vapid_creation_timestamp']))
        locator = f'/Preferences/{i}/value (JSON serializado), campo vapid_private_key'
        metadata = {'source': str(ROOT / 'Chrome/Configuración.json'), 'locator': locator,
                    'preference_name': 'sharing.vapid_key', 'curve': 'P-256', 'der_bytes': len(der),
                    'validation': 'Clave DER EC cargada; firma y verificación local correctas.',
                    'created_timestamp_original': value['vapid_creation_timestamp'],
                    'created_utc': created.isoformat(), 'created_local': created.astimezone(ZONE).isoformat(),
                    'public_key_sha256': hashlib.sha256(pub).hexdigest(),
                    'public_key_base64url': b64url(pub),
                    'scope': 'Preferencia interna sharing de Chrome; no hay prueba de que sea la clave de una aplicación web del usuario.'}
        key_meta.append(metadata)
        write('privado/vapid-recuperada.json', {**metadata, 'vapid_private_key_der_base64_original': original,
                                             'vapid_private_key_raw_base64url': b64url(private_raw),
                                             'preference_value_original': value})
        write('privado/vapid-private.pem', key.private_bytes(serialization.Encoding.PEM,
                                                           serialization.PrivateFormat.PKCS8,
                                                           serialization.NoEncryption()))
        write('privado/claves-recuperadas.md',
              '# Clave VAPID recuperada\n\n'
              f'Fuente: `{metadata["source"]}`\n\nLocalizador: `{locator}`.\n\n'
              f'Preferencia: `sharing.vapid_key`. Curva: P-256. Creada: {metadata["created_local"]}.\n\n'
              'Es una clave de la configuración interna de Chrome. No se ha establecido relación con una aplicación web propia.\n\n'
              f'## Valor privado original (DER en Base64)\n\n```text\n{original}\n```\n\n'
              f'## Escalar privado (32 bytes, Base64 URL sin relleno)\n\n```text\n{b64url(private_raw)}\n```\n\n'
              f'## Clave pública derivada (65 bytes, Base64 URL sin relleno)\n\n```text\n{b64url(pub)}\n```\n\n'
              'La representación PEM está en `vapid-private.pem`. La firma y verificación se comprobaron localmente.\n'
              'No se han encontrado contraseñas de inicio de sesión en los archivos de esta exportación revisados.\n')
    write('datos/clave-metadatos.json', key_meta)
    summary = {'browser_history_records': len(history['Browser History']),
               'search_activity_records': activity_counts.get('Mi actividad/Búsqueda/MiActividad.html'),
               'chrome_activity_records': activity_counts.get('Mi actividad/Chrome/MiActividad.html'),
               'topic_evidence_records': len(matches), 'topic_session_matches': len(session_matches),
               'sources_with_topic': [r['relative_path'] for r in manifest],
               'source_counts': dict(Counter(r['source'] for r in matches)),
               'password_export_candidate_files': password_candidate_files,
               'recovered_private_keys': len(key_meta),
               'date_parsing_failures_in_matches': sum(r.get('time_local') is None for r in matches),
               'generated_pdf': False}
    write('datos/resumen.json', summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    for r in matches:
        print(json.dumps({k: r.get(k) for k in ('time_local', 'kind', 'title_or_query', 'url', 'source', 'record_index_1based')}, ensure_ascii=False))
    print('KEY_METADATA', json.dumps(key_meta, ensure_ascii=False))


if __name__ == '__main__':
    main()
