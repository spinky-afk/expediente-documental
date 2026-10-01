#!/usr/bin/env python3
"""Actualiza la reconstrucción de las mismas copias locales y sus entregables."""
import subprocess
import sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
for executable,name in [
    (sys.executable,'integrar_actividad.py'),
    ('/usr/bin/python3','revisar_metadatos_imagenes.py'),
    (sys.executable,'preparar_informe.py'),
    (sys.executable,'ampliar_pistas.py'),
    (sys.executable,'generar_pdf.py'),
]:
    subprocess.run([executable,str(HERE/name)],check=True)
print('Actualizados: historial-cruzado.pdf, historial-cruzado.html, actividad-cronologica.csv, registro.md')
