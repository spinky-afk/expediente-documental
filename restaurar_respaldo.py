#!/usr/bin/env python3
"""Restaura copias, sin sobrescribir los originales, usando una clave local."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

parser=argparse.ArgumentParser()
parser.add_argument('--clave',type=Path,required=True)
parser.add_argument('--destino',type=Path,required=True)
args=parser.parse_args()
encrypted=json.loads((Path(__file__).resolve().parent/'sitio/respaldo-sensible-cifrado.json').read_text())
key=base64.urlsafe_b64decode(args.clave.read_text().strip())
data=AESGCM(key).decrypt(base64.b64decode(encrypted['nonce_base64']),base64.b64decode(encrypted['ciphertext_base64']),encrypted['aad'].encode())
package=json.loads(data)
args.destino.mkdir(parents=True,exist_ok=True);args.destino.chmod(0o700)
for index,item in enumerate(package['files'],1):
    content=base64.b64decode(item['data_base64'])
    if hashlib.sha256(content).hexdigest()!=item['sha256']: raise ValueError('Huella distinta')
    target=args.destino/(str(index)+'-'+Path(item['path']).name)
    with target.open('xb') as f: f.write(content)
    target.chmod(0o600)
print('Restauradas',len(package['files']),'copias verificadas en',args.destino)
