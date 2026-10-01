## iPhone conectado: consulta de respaldo, Safari y Atajos

Se detectó un iPhone por USB y se leyeron ProductVersion=16.7.16 y ProductType=iPhone10,4. El dominio com.apple.mobile.backup devolvió LastCloudBackupDate=812501783, LastCloudBackupTZ=CST y Version=2.0. No devolvió WillEncrypt: no se deduce de ese silencio el estado de cifrado.

Al interpretar LastCloudBackupDate con referencia CFAbsoluteTime de Apple (2001-01-01 UTC), corresponde al 30-09-2026 16:56:23 America/Mexico_City. Es metadato registrado en el teléfono, no una copia descargada ni una comprobación de que siga disponible para restaurar. Se puede corroborar en Ajustes, nombre, iCloud, Copia de seguridad de iCloud.

Para revisar Safari en iOS 16: Safari, marcadores (libro), historial (reloj). Los atajos se consultan en la app Atajos, Todos los atajos; las automatizaciones se revisan en su pestaña correspondiente. Archivos expone documentos y ubicaciones de apps, no todo el sistema de iOS. No se extrajeron Safari o Atajos por USB en esta lectura. La documentación Apple indica que los respaldos locales cifrados pueden incluir historial web; no se creó, restauró, borró ni modificó un respaldo.

[Metadatos de la lectura USB conservados](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/iphone-usb-y-respaldo.json)

[AP01 · Apple: buscar archivos](https://support.apple.com/es-es/102570)

[AP02 · Apple: ver copias de seguridad iCloud](https://support.apple.com/es-es/guide/icloud/mm122d3ef202/icloud)

[AP03 · Apple: Safari e historial](https://support.apple.com/es-es/105082)

[AP04 · Apple: organizar Atajos](https://support.apple.com/es-us/guide/shortcuts/apd113493874/ios)

[AP05 · Apple: copias locales cifradas](https://support.apple.com/es-es/108353)

[AP06 · Apple: CFAbsoluteTime](https://developer.apple.com/documentation/corefoundation/cfabsolutetime?changes=_10_4&language=objc)

[AP07 · libimobiledevice oficial](https://github.com/libimobiledevice/libimobiledevice)
