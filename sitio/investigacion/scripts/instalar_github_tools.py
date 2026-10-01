#!/usr/bin/env python3
"""Instala binarios oficiales gh/git-lfs en este espacio de trabajo."""
import hashlib
import io
import json
import re
import tarfile
import urllib.request
from datetime import datetime,timezone
from pathlib import Path

BASE=Path('/home/deep-logic/ai-lab/.tools/github')
BIN=BASE/'bin'
BIN.mkdir(parents=True,exist_ok=True)
BASE.chmod(0o700)
def get(url):
    request=urllib.request.Request(url,headers={'User-Agent':'archivo-documental-local'})
    with urllib.request.urlopen(request,timeout=60) as response:return response.read()
installed=[]
for repo,tool in [('cli/cli','gh'),('git-lfs/git-lfs','git-lfs')]:
    release=json.loads(get('https://api.github.com/repos/'+repo+'/releases/latest'))
    assets=release['assets']
    if tool=='gh':
        asset=next(a for a in assets if a['name'].endswith('_linux_amd64.tar.gz'))
        checks=next(a for a in assets if a['name'].endswith('_checksums.txt'))
    else:
        asset=next(a for a in assets if re.fullmatch(r'git-lfs-linux-amd64-v[\d.]+\.tar\.gz',a['name']))
        checks=next(a for a in assets if a['name']=='sha256sums.asc')
    package=get(asset['browser_download_url'])
    digest=hashlib.sha256(package).hexdigest()
    checksum_text=get(checks['browser_download_url']).decode()
    wanted=None
    for line in checksum_text.splitlines():
        match=re.match(r'^([a-fA-F0-9]{64})\s+\*?(.+?)\s*$',line)
        if match and match[2].lstrip('./')==asset['name']:wanted=match[1].lower()
    if wanted!=digest:raise RuntimeError('Checksum no coincide: '+asset['name'])
    with tarfile.open(fileobj=io.BytesIO(package),mode='r:gz') as archive:
        member=next(m for m in archive.getmembers() if m.isfile() and Path(m.name).name==tool)
        data=archive.extractfile(member).read()
    target=BIN/tool
    target.write_bytes(data);target.chmod(0o755)
    installed.append({'tool':tool,'release':release['tag_name'],'release_url':release['html_url'],'asset_url':asset['browser_download_url'],'checksums_url':checks['browser_download_url'],'archive_sha256_verified':digest,'binary_sha256':hashlib.sha256(data).hexdigest(),'path':str(target)})
    print(json.dumps(installed[-1],ensure_ascii=False),flush=True)
p=Path(__file__).resolve().parents[1]/'datos/github-herramientas-instaladas.json'
p.write_text(json.dumps({'installed_at_utc':datetime.now(timezone.utc).isoformat(),'tools':installed},ensure_ascii=False,indent=2)+'\n');p.chmod(0o600)
