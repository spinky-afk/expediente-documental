# Investigación local de historiales

Los archivos originales están en `/home/deep-logic/Documentos/Registro/Takeout` y `/home/deep-logic/Documentos/facebook`. Se leen sin modificarlos.

- [PDF completo](historial-cruzado.pdf): 27.044 observaciones fechadas y 495 fuentes, ordenadas por instante UTC y presentadas en America/Mexico_City; hallazgos, referencias, empresas y anexos. La cantidad de páginas y huella de esta edición figuran en `datos/pdf-manifiesto.json`.
- [Visor local](historial-cruzado.html): consulta sin conexión con filtros por texto, número, servicio y fechas. Permite alternar el orden y consultar las referencias originales.
- [Cronología CSV](actividad-cronologica.csv): una fila por observación, con fecha, fuente y localizador.
- [Registro vivo](registro.md): primeras búsquedas VAPID, pista de validar con imagen y ampliaciones de Facebook, Google Fotos, Etsy, Clarín, Hermes y TrustBuilder.
- [Hallazgos](hallazgos-facebook.md): explicación con las referencias de esta revisión.
- [Pistas recientes](pistas-etsy-clarin-hermes-y-fotos.md): revisión específica de los datos aportados durante la integración.
- [Noche del 20/21, juegos y dispositivos](noche-20-21-juegos-respaldos-dispositivos.md): 784 observaciones del intervalo, mensajes, respaldos, configuraciones y límites de lo recuperado.

**Cuentas de Google:** la comprobación del conector identifica `velez@deeplogic.com.mx`; el usuario solicitó consultar `hadilene116@gmail.com`. El perfil y la información del suscriptor del Takeout local sí incluyen la cuenta solicitada: `datos/cuenta-takeout-local.json` conserva las rutas y huellas de esa comprobación. Las consultas anteriores de Drive no verificaron la identidad durante la lectura y no se atribuyen a la cuenta solicitada. Se conservan como consultas separadas, sin deducir propiedad, eliminación o ausencia de datos en la otra cuenta. Antes de consultar ese Drive hace falta conectarlo mediante Google y volver a comprobar el perfil. La contraseña indicada en la conversación no se transcribe a estos entregables. Véase `datos/drive-identidad-consultada.json`.

Los códigos de observación y fuente corresponden a esta versión. Para referenciar algo después de añadir datos, conserva la ruta original, el localizador y su SHA-256.

La carpeta `datos` contiene las evidencias estructuradas, relaciones propuestas, inventarios, fuentes externas y verificaciones. `privado` contiene URLs originales, metadatos íntegros y la clave VAPID recuperada anteriormente. La clave privada no se inserta en el PDF, HTML, CSV o registro. Los originales no incluyen todas las acciones posibles de las cuentas y no permiten deducir un envío de mensaje o una autenticación solo a partir de una visita.

Para reconstruir los entregables de estas mismas copias locales:

```bash
python3 /home/deep-logic/ai-lab/research/vapid-webpush/scripts/actualizar.py
```

La comparación de imágenes usa Pillow del Python del sistema y la generación de PDF usa las bibliotecas nativas Pango/Cairo. No se descargan dependencias. Las notas nuevas de investigación requieren actualizar las explicaciones y fuentes de los scripts correspondientes antes de reconstruir.

La edición previa del 1 de octubre verificó 26.871 IDs. Esta ampliación añade 173 observaciones de configuración Android, juegos y sincronización Chrome. La comprobación de la edición actual se conserva separadamente en `datos/verificacion-ampliacion.json`; los controles anteriores siguen disponibles para identificar su alcance histórico.

El [sitio portátil](../expediente-documental/sitio/index.html) reúne las páginas de los datos, una cronología con enlaces internos, las fichas de referencias técnicas y la carta solicitada como testimonio personal. La edición del PDF del sitio conserva los 27.044 registros y sus enlaces apuntan al archivo local. Hay 844 copias originales idénticas y un original de Chrome con clave privada conservado mediante respaldo cifrado. Las tres versiones de la clave recuperada también están cifradas en ese respaldo. La clave de recuperación permanece en `privado/clave-respaldo-github-local.txt`, fuera del proyecto preparado para GitHub.

La cuenta indicada por el usuario es `spinky-afk`. Se preparó un repositorio Git local en `../expediente-documental`; todavía no hay repositorio remoto ni sitio publicado. La visibilidad prevista es privada. GitHub Pages no se activa automáticamente. El comando de actualización anterior también reconstruye el sitio local; requiere mantener los datos originales disponibles. La carta no se envió a sus destinatarios.
