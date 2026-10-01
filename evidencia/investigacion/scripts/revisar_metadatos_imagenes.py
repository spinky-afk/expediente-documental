#!/usr/bin/env python3
"""Lectura de imágenes; no escribe ni cambia originales. Ejecutar con /usr/bin/python3."""
import hashlib
import json
import os
from collections import Counter,defaultdict
from datetime import datetime,timezone
from pathlib import Path
from PIL import Image,ExifTags
OUT=Path(__file__).resolve().parents[1]
ROOT=Path('/home/deep-logic/Documentos')
def serial(v):
    if isinstance(v,bytes):return {'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()}
    if isinstance(v,dict):return {str(k):serial(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [serial(x) for x in v]
    if isinstance(v,(str,int,float,bool)) or v is None:return v
    return str(v)
records=[];errors=[];pixelgroups=defaultdict(list)
for p in sorted(ROOT.rglob('*')):
    if not p.is_file() or not (p.suffix.lower() in ('.jpg','.jpeg','.png','.webp','.gif','.heic') or p.parent.name=='files'):continue
    try:
        raw=p.read_bytes();stat=p.stat()
        with Image.open(p) as im:
            exif=im.getexif();fields={ExifTags.TAGS.get(k,str(k)):serial(v) for k,v in exif.items()}
            for key,label in [(34665,'ExifIFD'),(34853,'GPSIFD')]:
                if key in exif:
                    try:fields[label]={ExifTags.TAGS.get(k,str(k)):serial(v) for k,v in exif.get_ifd(key).items()}
                    except Exception as e:fields[label]={'error':str(e)}
            pixels=im.convert('RGBA')
            pixel_hash=hashlib.sha256(str(pixels.size).encode()+pixels.tobytes()).hexdigest()
            info={k:serial(v) for k,v in im.info.items() if k!='exif'}
            row={'path':str(p),'format':im.format,'width':im.width,'height':im.height,'bytes':len(raw),
                 'sha256':hashlib.sha256(raw).hexdigest(),'rgba_pixels_sha256':pixel_hash,
                 'filesystem_mtime_utc':datetime.fromtimestamp(stat.st_mtime,timezone.utc).isoformat(),
                 'filesystem_mtime_interpretation':'modificación de archivo; no demuestra captura o publicación',
                 'exif':fields,'other_metadata':info}
            records.append(row);pixelgroups[pixel_hash].append(row)
    except Exception as e:errors.append({'path':str(p),'error':str(e)})
groups=[{'pixels_sha256':h,'files':[r['path'] for r in rs],'different_binary_hashes':len({r['sha256'] for r in rs})>1,
         'different_exif':len({json.dumps(r['exif'],sort_keys=True) for r in rs})>1} for h,rs in pixelgroups.items() if len(rs)>1]
summary={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'root':str(ROOT),'images_read':len(records),
         'formats':dict(Counter(r['format'] for r in records)),'images_with_exif':sum(bool(r['exif']) for r in records),
         'google_images':sum('/Registro/Takeout/' in r['path'] for r in records),
         'facebook_images':sum('/facebook/' in r['path'] for r in records),
         'google_photos_directory_found':any(p.is_dir() and p.name.lower() in ('google fotos','google photos') for p in ROOT.rglob('*')),
         'google_photos_sidecars_found':[str(p) for p in ROOT.rglob('*.json') if p.name.lower().endswith(('.jpg.json','.png.json','.jpeg.json','.supplemental-metadata.json'))],
         'identical_pixel_groups':groups,'errors':errors,
         'business_association':'No demostrada por cambios de metadatos. No hay pares originales/Google Fotos documentados para comparar.',
         'originals_unchanged':all(hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256'] for r in records)}
for name,data in [('privado/imagenes-metadatos.json',records),('datos/imagenes-metadatos-resumen.json',summary)]:
 p=OUT/name;p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');os.chmod(p,0o600)
print(json.dumps({k:v for k,v in summary.items() if k!='identical_pixel_groups'},ensure_ascii=False,indent=2))
