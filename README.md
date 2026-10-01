# Archivo documental privado

Archivo preparado para la cuenta GitHub verificada `spinky-afk`. El estado de subida y el enlace remoto comprobado están en `estado-publicacion.json`.

El proyecto contiene datos personales, conversaciones, identificadores y URLs originales. La visibilidad prevista del repositorio es **privada**. No actives GitHub Pages sin verificar que el sitio tendrá control de acceso: un repositorio privado no hace privado un sitio de Pages. No hay despliegue automático.

Para consultar: abre `sitio/index.html`, o ejecuta desde esta carpeta:

```bash
python3 servir_local.py
```

Abre `http://127.0.0.1:8765`. El servidor escucha solo en tu equipo. Carta, cronología, PDF, fuentes originales y vistas derivadas están dentro de `sitio`.

El constructor está en `../vapid-webpush/scripts/construir_sitio.py`. Para actualizar después de reconstruir los datos:

```bash
python3 ../vapid-webpush/scripts/construir_sitio.py
```

El registro se conserva en research y en el sitio. Las fuentes originales incluyen SHA-256 y se comparan durante la construcción. Las vistas desactivan navegación y carga externas; no se afirma que sean byte a byte idénticas al original descargable. Las fichas de referencias externas contienen notas, no copias completas de los artículos.

La carpeta `evidencia/originales` contiene todos los originales sin excluir datos privados, incluida la configuración Chrome. `evidencia/investigacion` conserva todo research, las claves recuperadas y la clave de respaldo, según autorización del propietario. El sitio conserva adicionalmente su respaldo cifrado y vistas de lectura. Los archivos grandes usan Git LFS: descarga mediante `git clone` y `git lfs pull` para recuperar sus bytes completos. Las credenciales de la conexión GitHub están fuera del expediente.

La carta reproduce un testimonio personal solicitado. Las acusaciones no son conclusiones verificadas del análisis. No se envió a sus destinatarios.
