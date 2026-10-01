#!/usr/bin/env python3
"""Comprueba cronología, procedencia y las dos ediciones actuales del PDF."""
import hashlib
import json
import re
import subprocess
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT.parent / 'expediente-documental/sitio'
def read(path):
    return json.loads(path.read_text())
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

events = read(ROOT / 'datos/actividad-cronologica.json')
expected = [event['id'] for event in events]
assert len(set(expected)) == len(expected)
assert [event['time_utc'] for event in events] == sorted(event['time_utc'] for event in events)
sources = read(ROOT / 'datos/catalogo-fuentes.json')
for source in sources:
    assert sha(Path(source['path'])) == source['sha256'], source['path']
for source in read(ROOT / 'datos/cuenta-takeout-local.json')['files']:
    path = Path(source['path'])
    assert sha(path) == source['sha256']
    assert 'hadilene116@gmail.com' in path.read_text()
keys = read(ROOT / 'privado/vapid-recuperada.json')
needles = [keys[key] for key in ['vapid_private_key_der_base64_original', 'vapid_private_key_raw_base64url']]
reports = []
for folder in [ROOT, SITE]:
    pdf = folder / 'historial-cruzado.pdf'
    text = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], check=True, capture_output=True).stdout.decode('utf-8')
    text = unicodedata.normalize('NFKC', text)
    ids = re.findall(r'\b(E\d{6})\s*\|', text)
    assert ids == expected, f'{pdf}: {len(ids)} / {len(expected)} registros'
    assert all(needle not in text for needle in needles)
    assert 'velez@deeplogic.com.mx' in text and 'hadilene116@gmail.com' in text
    manifest = read(folder / 'datos/pdf-manifiesto.json')
    assert sha(pdf) == manifest['pdf_sha256']
    assert manifest['events_rendered'] == len(events)
    assert manifest['timeline_json_sha256'] == sha(ROOT / 'datos/actividad-cronologica.json')
    info = subprocess.run(['pdfinfo', str(pdf)], check=True, capture_output=True).stdout.decode()
    pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1])
    assert pages == manifest['pages']
    reports.append({'pdf': str(pdf), 'pages': pages, 'timeline_records': len(ids), 'ids_exact_and_chronological': True, 'private_key_values_absent': True, 'account_scope_correction_present': True, 'sha256': manifest['pdf_sha256']})
public = [ROOT/'historial-cruzado.html', ROOT/'actividad-cronologica.csv', ROOT/'datos/actividad-cronologica.json']
assert all(not any(needle in path.read_text() for needle in needles) for path in public)
report = {'verified_at_utc': datetime.now(timezone.utc).isoformat(), 'observations': len(events), 'source_files_verified_unchanged': len(sources), 'account_provenance_files_verified': 2, 'sorted_by_utc': True, 'unique_observation_ids': True, 'pdf_editions': reports, 'site_checks': read(SITE/'verificacion-sitio.json')}
path = ROOT/'datos/verificacion-ampliacion.json'
path.write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n')
path.chmod(0o600)
print(json.dumps({k:v for k,v in report.items() if k!='site_checks'}, ensure_ascii=False))
