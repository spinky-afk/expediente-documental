# Archivo documental privado

Sitio local preparado a petición del propietario. El usuario confirmó haber creado su cuenta. No se ha publicado un repositorio. Cuenta indicada por el usuario: `spinky-afk`.

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

Cuatro archivos con una clave VAPID se incluyen cifrados con AES-256-GCM. La clave de respaldo está fuera del proyecto, en `../vapid-webpush/privado/clave-respaldo-github-local.txt`. Los originales y las claves recuperadas permanecen en sus ubicaciones previas. Mantén la clave de respaldo para poder restaurarlos; no se copia a GitHub.

La carta reproduce un testimonio personal solicitado. Las acusaciones no son conclusiones verificadas del análisis. No se envió a sus destinatarios.
