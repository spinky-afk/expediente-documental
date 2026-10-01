#!/usr/bin/env python3
"""Actualiza la reconstrucción de las mismas copias locales y sus entregables."""
import subprocess
import shutil
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
for executable,name in [
    (sys.executable,'integrar_actividad.py'),
    ('/usr/bin/python3','revisar_metadatos_imagenes.py'),
    (sys.executable,'preparar_informe.py'),
    (sys.executable,'ampliar_pistas.py'),
    (sys.executable,'ampliar_noche_dispositivos.py'),
    (sys.executable,'ampliar_uber.py'),
    (sys.executable,'ampliar_correo.py'),
    (sys.executable,'ampliar_bydefault.py'),
    (sys.executable,'ampliar_iphone.py'),
    (sys.executable,'ampliar_github.py'),
    (sys.executable,'generar_pdf.py'),
    (sys.executable,'construir_sitio.py'),
]:
    subprocess.run([executable,str(HERE/name)],check=True)
site=HERE.parents[1]/'expediente-documental'
subprocess.run([sys.executable,str(site/'verificar.py')],check=True)
subprocess.run([sys.executable,str(HERE/'verificar_ampliacion.py')],check=True)
shutil.copy2(HERE.parent/'datos/verificacion-ampliacion.json',site/'sitio/investigacion/datos/verificacion-ampliacion.json')
subprocess.run([sys.executable,str(HERE/'archivar_todo.py')],check=True)
print('Actualizados: historial-cruzado.pdf, historial-cruzado.html, actividad-cronologica.csv, registro.md y sitio local. No se publica en internet automáticamente.')
