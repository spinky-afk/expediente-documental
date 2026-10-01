# Investigación local de historiales

Los archivos originales están en `/home/deep-logic/Documentos/Registro/Takeout` y `/home/deep-logic/Documentos/facebook`. Se leen sin modificarlos.

- [PDF completo](historial-cruzado.pdf): 26.871 observaciones fechadas, ordenadas por instante UTC y presentadas en America/Mexico_City; hallazgos, referencias, empresas y anexos. Versión del 1 de octubre de 2026: 2.346 páginas, aproximadamente 42,5 MB.
- [Visor local](historial-cruzado.html): consulta sin conexión con filtros por texto, número, servicio y fechas. Permite alternar el orden y consultar las referencias originales.
- [Cronología CSV](actividad-cronologica.csv): una fila por observación, con fecha, fuente y localizador.
- [Registro vivo](registro.md): primeras búsquedas VAPID, pista de validar con imagen y ampliaciones de Facebook, Google Fotos, Etsy, Clarín, Hermes y TrustBuilder.
- [Hallazgos](hallazgos-facebook.md): explicación con las referencias de esta revisión.
- [Pistas recientes](pistas-etsy-clarin-hermes-y-fotos.md): revisión específica de los datos aportados durante la integración.

Los códigos de observación y fuente corresponden a esta versión. Para referenciar algo después de añadir datos, conserva la ruta original, el localizador y su SHA-256.

La carpeta `datos` contiene las evidencias estructuradas, relaciones propuestas, inventarios, fuentes externas y verificaciones. `privado` contiene URLs originales, metadatos íntegros y la clave VAPID recuperada anteriormente. La clave privada no se inserta en el PDF, HTML, CSV o registro. Los originales no incluyen todas las acciones posibles de las cuentas y no permiten deducir un envío de mensaje o una autenticación solo a partir de una visita.

Para reconstruir los entregables de estas mismas copias locales:

```bash
python3 /home/deep-logic/ai-lab/research/vapid-webpush/scripts/actualizar.py
```

La comparación de imágenes usa Pillow del Python del sistema y la generación de PDF usa las bibliotecas nativas Pango/Cairo. No se descargan dependencias. Las notas nuevas de investigación requieren actualizar las explicaciones y fuentes de los scripts correspondientes antes de reconstruir.

La verificación del 1 de octubre confirmó que el texto del PDF conserva exactamente los 26.871 IDs de la cronología, en el mismo orden; contiene enlaces y marcadores; no expone los valores de la clave privada recuperada; y los originales consultados conservaron sus huellas. Resultados: `datos/verificacion-entregables.json` y `datos/verificacion-integracion.json`.
