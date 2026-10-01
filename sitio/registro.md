# Registro de investigación: VAPID y Web Push

Creado: 2026-10-01. Zona horaria de presentación: America/Mexico_City.

## Encargo

Cruzar el historial de búsquedas de Google con el historial de Chrome de las carpetas en `/home/deep-logic/Documentos`; recuperar preguntas, fechas, fuentes, enlaces y posibles credenciales relacionadas con VAPID/Web Push. Mantener este registro durante la conversación. Generar el PDF únicamente cuando el usuario lo pida al final.

## Alcance y fuentes iniciales

- Carpeta Google: `/home/deep-logic/Documentos/Registro/Takeout`.
- Segunda carpeta: `/home/deep-logic/Documentos/facebook`.
- Historial Chrome: `Chrome/Historial.json`.
- Consultas Google: `Mi actividad/Búsqueda/MiActividad.html`.
- Actividad Chrome: `Mi actividad/Chrome/MiActividad.html`.
- Configuración Chrome: `Chrome/Configuración.json`.

Se leerán los originales sin modificarlos. Se conservarán localizadores por archivo y número de registro, fechas originales y normalizadas, y huellas SHA-256 de las fuentes usadas. Las credenciales que aparezcan se guardarán en `privado/`, separado del registro de lectura.

## Sesión 1

- El usuario confirmó la ruta `/home/deep-logic/Documentos`.
- Se localizaron 1.182 registros en la sección `Browser History` del historial Chrome y seis registros en `Session`.
- La búsqueda textual inicial encontró coincidencias de VAPID/Web Push en los cuatro archivos Google enumerados arriba.
- No se ha generado ningún PDF.

<!-- INICIO_RESULTADOS_SESION_1 -->

## Hallazgos y cruce verificado

Se inventariaron 149 archivos Google. La búsqueda textual se amplió a notificaciones push, PushSubscription, PushManager y Firebase Cloud Messaging. El tema aparece en cuatro fuentes Google: los dos archivos de actividad, Historial.json y Configuración.json.

Se revisaron 874 registros de Búsqueda, 359 registros de actividad Chrome y 1182 entradas de Browser History. Resultado: dos consultas explícitas y dos destinos visitados, con ocho observaciones. No hubo coincidencias en la sección Session.

Todos los horarios de la tabla son del **26 de septiembre de 2026**, America/Mexico_City (UTC−06:00).

| Hora | Acción y enlace | Evidencia |
|---|---|---|
| 22:28:27 | consulta: [vapid](https://www.google.com/search?q=vapid) | Mi actividad/Búsqueda/MiActividad.html #8 |
| 22:28:32 | consulta: [vapid web push](https://www.google.com/search?q=vapid+web+push) | Mi actividad/Búsqueda/MiActividad.html #7 |
| 22:28:39 | visita: [Notificaciones push web mediante el método VAPID — por Carlos Ribeiro — bawilabs — Medium](https://medium.com/bawilabs/web-push-notifications-through-vapid-method-7d4d6927a006) | Mi actividad/Búsqueda/MiActividad.html #6; Mi actividad/Chrome/MiActividad.html #20; Chrome/Historial.json #65 |
| 22:28:55 | visita: [El protocolo de envío web  —  Articles  —  web.dev](https://web.dev/articles/push-notifications-web-push-protocol?hl=es-419) | Mi actividad/Búsqueda/MiActividad.html #5; Mi actividad/Chrome/MiActividad.html #19; Chrome/Historial.json #64 |

El clic hacia la traducción de Medium quedó registrado a las 22:28:39 y la visita de Chrome a las 22:28:40.163036. El clic hacia web.dev quedó registrado a las 22:28:55 y la visita de Chrome a las 22:28:56.599891. La coincidencia de destino y ese intervalo respaldan el cruce; los registros prueban búsquedas y visitas, sin demostrar que se leyera todo el contenido.

Las expresiones «vapid» y «vapid web push» son las consultas exactas recuperadas; no se encontraron preguntas más extensas sobre este tema. Los enlaces originales de Google Translate y las redirecciones de Google se conservan en `datos/evidencias.json`, junto con el texto original y la ubicación del registro.

## Clave recuperada y contraseñas

- Fuente: `/home/deep-logic/Documentos/Registro/Takeout/Chrome/Configuración.json`.
- Localizador: `/Preferences/2/value (JSON serializado), campo vapid_private_key`.
- Preferencia: `sharing.vapid_key`; campo: `vapid_private_key`.
- El valor es una clave privada EC P-256, DER codificado en Base64 (138 bytes). La carga y una firma/verificación local fueron correctas.
- Fecha guardada de creación: `2025-11-22T16:39:12.095937-06:00`; UTC: `2025-11-22T22:39:12.095937+00:00`.
- Conversión de la fecha: microsegundos desde 1601-01-01 UTC, formato interno de tiempo de Chromium. Se preserva también el número original.
- Huella SHA-256 de la clave pública: `76d04a8ddf4840f26ebd22b9022affc7436cc90860b0a8abed805420d94289eb`.

La ubicación de la clave y el componente de Chromium que administra esta preferencia la vinculan con el sistema interno de compartir de Chrome. [Código de Chromium consultado](https://chromium.googlesource.com/chromium/src/%2B/refs/tags/137.0.7151.130/components/sharing_message/sharing_sync_preference.cc). La exportación no permite identificarla como una clave de un servicio Web Push propio, y no aporta su endpoint de suscripción, claves p256dh/auth ni el servidor de una aplicación propia. Su fecha de creación antecede a las búsquedas; no hay evidencia de que esas consultas la generaran.

El valor completo y las representaciones derivadas están en [claves-recuperadas.md](privado/claves-recuperadas.md), [vapid-recuperada.json](privado/vapid-recuperada.json) y [vapid-private.pem](privado/vapid-private.pem). Estos archivos tienen permisos 0600 y el directorio, 0700.

No se encontró un archivo de exportación de contraseñas en el inventario Google. Los historiales revisados no contienen valores de contraseñas de inicio de sesión recuperables. El campo `password_state` de Session contiene estados (`HAS_PASSWORD_FIELD`, `NO_PASSWORD_FIELD`, `PASSWORD_STATE_UNKNOWN`); esos estados no guardan la contraseña introducida. No se realizaron inicios de sesión ni cambios de cuenta.

## Segunda carpeta

En Facebook no se encontraron menciones explícitas de VAPID/Web Push. La búsqueda ampliada encontró cinco archivos con etiquetas genéricas de notificaciones push (configuración, índice y estadísticas). Se documentan sus rutas, huellas y contextos limitados en `datos/facebook-notificaciones-genericas.json`; no prueban una suscripción Web Push ni aportan claves VAPID.

## Lectura para aprender

VAPID identifica al servidor de aplicaciones ante el servicio push mediante un JWT firmado con su clave privada P-256; la clave pública permite verificarlo. [RFC 8292](https://www.rfc-editor.org/rfc/rfc8292.html). La suscripción aporta un destino (`endpoint`) y material `p256dh`/`auth` para el cifrado del mensaje. [RFC 8291](https://www.rfc-editor.org/rfc/rfc8291.html).

Para estudiar a partir de tus visitas, empieza por [web.dev](https://web.dev/articles/push-notifications-web-push-protocol?hl=es-419) y conserva [el artículo de Medium](https://medium.com/bawilabs/web-push-notifications-through-vapid-method-7d4d6927a006) como referencia de tu recorrido. Los ejemplos de web.dev muestran `Authorization: WebPush`, `Crypto-Key` y `aesgcm`; para una implementación, contrastar el esquema `vapid` de RFC 8292 y `aes128gcm` de RFC 8291.

Preguntas propuestas para estudiar (no son consultas recuperadas del historial):

1. ¿Qué relación hay entre Web Push, el servicio push y el service worker?
2. ¿Para qué se usan la clave pública y la clave privada VAPID?
3. ¿Qué representan endpoint, p256dh y auth en una suscripción?
4. ¿Cómo se identifica al servidor y cómo se cifra un mensaje?
5. ¿Cómo distinguir una clave interna de Chrome de una clave de una aplicación propia?

## Fuentes locales y trazabilidad

Los números de registro son de base uno; los índices en los localizadores JSON son de base cero. En HTML se guarda además la línea y columna del comienzo de cada celda de actividad. Los originales no se modificaron.

- L01: `/home/deep-logic/Documentos/Registro/Takeout/Chrome/Configuración.json` (4316 bytes). SHA-256: `3a6721130533dcc32dd90690298d29f1f1ce987401c498e23b35f146aa1042fd`.
- L02: `/home/deep-logic/Documentos/Registro/Takeout/Chrome/Historial.json` (1192672 bytes). SHA-256: `b919cb5217d871480ef9dd3b76ce093f60e028cc14cc756b57a404dafac3b38f`.
- L03: `/home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Búsqueda/MiActividad.html` (1132089 bytes). SHA-256: `32c36ffc2742ba5c873784cf597e9a1ac56b518caf948df35b92c316792a5cbc`.
- L04: `/home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Chrome/MiActividad.html` (532082 bytes). SHA-256: `5052f54fdd5cb57d369b1fe1f246a82735e22f404470256644223cd697023bb2`.

## Fuentes web consultadas

- W01: [El protocolo de envío web — web.dev](https://web.dev/articles/push-notifications-web-push-protocol?hl=es-419). Consultada: 2026-10-01. Visita histórica encontrada y lectura actual realizada. Explica claves del servidor, JWT, suscripciones y cifrado. Algunos ejemplos usan encabezados y aesgcm de una versión anterior; contrastarlos con W03 y W04.
- W02: [Web Push Notifications through VAPID method — Carlos Ribeiro, bawilabs](https://medium.com/bawilabs/web-push-notifications-through-vapid-method-7d4d6927a006). Consultada: 2026-10-01. Visita histórica encontrada; se confirmó título, autor y fecha de publicación. Publicado el 20 de noviembre de 2018. Referencia histórica del recorrido del usuario; las explicaciones técnicas de este registro se fundamentan en fuentes primarias.
- W03: [RFC 8292 — Voluntary Application Server Identification (VAPID) for Web Push](https://www.rfc-editor.org/rfc/rfc8292.html). Consultada: 2026-10-01. Referencia primaria adicional consultada durante esta investigación; no es una visita recuperada del historial. Define identificación del servidor con JWT y ECDSA P-256/ES256, aud/exp y el esquema Authorization: vapid con parámetros t y k.
- W04: [RFC 8291 — Message Encryption for Web Push](https://www.rfc-editor.org/rfc/rfc8291.html). Consultada: 2026-10-01. Referencia primaria adicional consultada durante esta investigación. Explica cifrado de extremo a extremo, ECDH, secreto de autenticación de suscripción y aes128gcm. Separa el cifrado de la identificación VAPID.
- W05: [Chromium — SharingSyncPreference, versión 137.0.7151.130](https://chromium.googlesource.com/chromium/src/%2B/refs/tags/137.0.7151.130/components/sharing_message/sharing_sync_preference.cc). Consultada: 2026-10-01. Código primario consultado para interpretar el campo encontrado; no procede del historial personal. GetVapidKey decodifica vapid_private_key desde Base64; SetVapidKey guarda esa clave y vapid_creation_timestamp. El componente administra preferencias sharing, datos FCM y dispositivos sincronizados.
- W06: [Chromium — nombre de preferencia sharing.vapid_key](https://chromium.googlesource.com/chromium/src/%2B/a73140559ea8872c19acf6d190aacf1a46eef99b/chrome/common/pref_names.h). Consultada: 2026-10-01. Resultado de búsqueda primaria revisado para identificar el nombre de preferencia. Declara kSharingVapidKey con el nombre sharing.vapid_key; la interpretación detallada se apoya en W05.
- W07: [Chromium — SharingSyncPreference, revisión c18a333f](https://chromium.googlesource.com/chromium/src/%2B/c18a333f058a6f3a60dfc635b08f29fa6b4e7f81/chrome/browser/sharing/sharing_sync_preference.cc). Consultada: 2026-10-01. Resultado de búsqueda primaria revisado; posteriormente se abrió W05. El fragmento encontrado relaciona vapid_private_key y vapid_creation_timestamp con preferencias sharing.
- W08: [Chromium — SharingSyncPreference, revisión cd9d08a4](https://chromium.googlesource.com/chromium/src/%2B/cd9d08a4c4086bdac4d36c313e2b785776e8377d/chrome/browser/sharing/sharing_sync_preference.cc). Consultada: 2026-10-01. Resultado de búsqueda primaria revisado. Implementación adicional de las funciones de almacenamiento de VAPID.
- W09: [Chromium experimental — SharingSyncPreference, versión 82.0.4053.0](https://chromium.googlesource.com/experimental/chromium/src/%2B/refs/tags/82.0.4053.0/chrome/browser/sharing/sharing_sync_preference.cc). Consultada: 2026-10-01. Resultado de búsqueda primaria revisado. Referencia histórica; no se utiliza para afirmar la versión de Chrome de esta cuenta.

Las cinco búsquedas externas y los ocho intentos de acceso sin resultado útil se conservan en `datos/fuentes-web.json`. Los enlaces añadidos para verificar conceptos se distinguen de los dos artículos encontrados en tu historial.

## Archivos de trabajo y continuación

- `datos/evidencias.json`: ocho observaciones, texto original, fechas, URLs originales y localizadores.
- `datos/cruce.json`: cuatro eventos con sus referencias y criterio de correlación.
- `datos/cronologia.csv`: cronología para consultar en una hoja de cálculo.
- `datos/fuentes-locales.json` y `datos/fuentes-web.json`: referencias y procedencia.
- `datos/clave-metadatos.json`: descripción verificable de la clave, sin su valor privado.
- `datos/inventario-google.json`: rutas y tamaños del conjunto Google.
- `privado/`: valor completo de la clave recuperada y sus representaciones.
- `scripts/extraer.py` y `scripts/documentar.py`: procedimientos reproducibles de extracción y documentación.

En las siguientes intervenciones se añadirán aquí nuevos hallazgos, consultas y referencias. El PDF sigue pendiente para cuando el usuario indique que terminó la conversación.

<!-- FIN_RESULTADOS_SESION_1 -->

<!-- INICIO_RESULTADOS_SESION_2 -->
## Sesión 2: búsqueda aproximada sobre validar con una imagen más rápido

Solicitud: «Ahora en las busquedas busca algo sobre como se puede validar con una imagen mas rapido o algo asi».

Se examinaron los 874 registros de Búsqueda (382 consultas explícitas), 50 registros de Búsqueda de imágenes, 14 de Google Lens y 16 de Modo IA. Se amplió la revisión a los 27 archivos HTML de Mi actividad, las 1.182 entradas de Browser History y tres imágenes JPG locales asociadas a Lens. Se buscaron variantes en español e inglés: validar/verificar/comprobar, imagen/foto/captura, rápido/fácil, CAPTCHA, identidad, selfie, reconocimiento, QR y escaneo. Se normalizaron acentos y se examinaron fechas y enlaces.

**Resultado:** no se encontró una consulta explícita que combinara validación/verificación con una imagen, ni se identificó el procedimiento más rápido que recuerda el usuario. No se eligió una interpretación de «validar» sin evidencia. Los dos «OK» recibidos no especifican qué se quería validar.

### Pistas conservadas, sin confirmar

| Fecha y hora de México | Registro | Referencia |
|---|---|---|
| 29-08-2026 03:06:47 | Visita a «Verifica tu identidad cuando completes una acción sensible» | Mi actividad/Ayuda #707; [Google](https://support.google.com/accounts/answer/7162782?hl=es-419) |
| 11-09-2026 09:35:33 | Visita a «Accede a tu cuenta con los mensajes de Google» | Mi actividad/Ayuda #530; [Google](https://support.google.com/accounts/answer/7026266?hl=es-419) |
| 26-09-2026 22:33:14 | «Verifica que eres tú», ruta de contraseña challenge/pwd | Mi actividad/Chrome #8 y Browser History #44; el enlace original con parámetros se conserva en privado |
| 26-09-2026 02:04:13 | Dos registros de búsqueda con Google Lens | Mi actividad/Google Lens #1 y #2; sin pregunta ni imagen adjunta conservadas en esos registros |
| 06-08-2026 07:33:49 y 13:26:25 | Quince registros «Hiciste una búsqueda con una imagen» | Mi actividad/Búsqueda #627–641; sin consulta textual ni enlace de resultados que expliquen qué se validaba |

Las tres imágenes JPG guardadas de Lens, del 27-08-2026, se inspeccionaron visualmente: son páginas de lectura literaria en inglés. Se descartaron como evidencia de una verificación con imagen. Se conservaron sus rutas y huellas, sin transcribir el libro.

El artículo de identidad encontrado en el historial menciona actualmente documentos vinculados y un apartado para acelerar la confianza en métodos de autenticación; ese apartado remite al uso de llaves ya confiables. Esto no prueba un método más rápido con una imagen, ni que el contenido actual sea idéntico al visto en agosto. [Guía de identidad](https://support.google.com/accounts/answer/7162782?hl=es-419), [guía adicional consultada hoy](https://support.google.com/accounts/answer/7684753).

La otra visita corresponde a confirmar acceso mediante notificaciones de Google. Se mantiene como candidato temático, sin atribuirle relación con imágenes. [Guía de mensajes de Google](https://support.google.com/accounts/answer/7026266?hl=es-419).

Se siguió también el enlace al artículo de documento de identidad `answer/16761564`; redirigió a un índice general de seguridad, por lo que no se pudo comprobar su contenido. Las dos páginas derivadas de esta lectura actual no se encontraron como visitas en los historiales de Búsqueda, Chrome o Ayuda revisados.

### Evidencias y continuación

- `datos/imagen-validacion-evidencias.json`: candidatos, fechas, enlaces públicos y localizadores.
- `privado/imagen-validacion-evidencias-originales.json`: texto y enlaces originales; incluye parámetros de las pantallas de acceso.
- `datos/imagen-validacion-auditoria.json`: alcance, variantes buscadas, conteos y SHA-256 de los archivos consultados.
- `datos/imagen-validacion-fuentes-web.json`: cuatro destinos consultados hoy y su relación con las visitas históricas.
- `scripts/buscar_validacion_imagen.py`: procedimiento reproducible.

La pista permanece sin identificar. La aclaración solicitada fue si se quería validar una cuenta/identidad, un CAPTCHA o información/objetos. No se generó PDF.
<!-- FIN_RESULTADOS_SESION_2 -->


<!-- INICIO_RESULTADOS_SESION_3 -->
## Sesión 3: Facebook y PDF cronológico actualizado

## Hallazgos: Facebook, Google y números de identificación

Actualizado el 1 de octubre de 2026. La solicitud actual autoriza crear y actualizar el PDF desde ahora. Las indicaciones anteriores de esperar al final se conservan como historial de la investigación.

La cronología integra 26,871 observaciones fechadas de 482 archivos consultados, de 2022-08-15 a 2026-09-27. Google y Facebook se ordenan conjuntamente por instante UTC y se muestran en America/Mexico_City. Hay 38 secciones sin fecha, conservadas por separado.

## Qué significan los números

Se encontró una relación explícita entre una página y su conversación: Epazote Tulancingo. El catálogo contiene 87 entidades de actividad fuera de Meta. Ninguno de sus identificadores de empresa o de evento aparece en el texto ni en los enlaces de las conversaciones exportadas. Este resultado no cubre reconocimiento automático del texto de todas las fotos o videos ni mensajes ausentes de la exportación.

Los campos con nombre Identificador se conservan con su contexto: uno identifica la entidad en el encabezado del archivo y otro aparece dentro del bloque de eventos. No se ha demostrado que este último identifique de manera única un evento: se repite entre fechas y entre entidades. Tampoco se ha demostrado que el Identificador de entidad sea un Meta Business Manager ID.

Epazote Tulancingo: page_id=107881590544962. Aparece en el parámetro extra_params de un enlace interno de Messenger del 28-08-2026 a las 17:29:03, en el mensaje de sistema 'Empezaste a seguir'. No prueba que alguien escribiera o enviara ese número manualmente. Referencia: S438, mensaje #14, línea 13, columna 5030.

[Conversación original de Epazote Tulancingo](file:///home/deep-logic/Documentos/facebook/your_facebook_activity/messages/inbox/epazotetulancingo_1514670583749704/message_1.html)

La carpeta epazotetulancingo_1514670583749704 tiene otro número: 1514670583749704. Se conserva como sufijo de carpeta/conversación, sin equipararlo al page_id. Ninguno de los dos coincide con los identificadores de las 87 entidades revisadas.

Ejemplo ChatGPT: Identificador de entidad 6558176734212414; Identificador dentro de eventos 562278416645613; sufijo de archivo 105529809654844465. Son tres campos distintos. El sufijo de archivo se repite en otros archivos y no se usa para identificar una empresa.

## Relaciones entre entidades de actividad fuera de Meta

Hay ocho valores del campo Identificador de evento compartidos por más de una entidad. Esto es una coincidencia literal documentada, no una prueba de que los nombres correspondan a una misma empresa o de que hayan intercambiado mensajes contigo.

Evento 169883356982592 → Coppel [entidad 10153514100232571]; coppel.com [entidad 1444276872316871].

Evento 265290261046250 → caliente.mx [entidad 1519403778150555]; eshkol.one [entidad 9546301038777891].

Evento 287682846389126 → Coppel [entidad 10153514100232571]; coppel.com [entidad 1444276872316871].

Evento 337522080014293 → att.com.mx [entidad 1273743596085463]; e-planning.net [entidad 1943983615628893].

Evento 524032566269295 → Different Technologies [entidad 949230206018406]; bancoplata.mx [entidad 33769818155997760].

Evento 5435870899848740 → Coppel [entidad 10153514100232571]; coppel.com [entidad 1444276872316871].

Evento 597615686992125 → TikTok - Videos, Shop & LIVE [entidad 695086290555235]; TikTok - Videos, Shop & LIVE [entidad 703679579689017].

Evento 678263238969275 → Coppel [entidad 10153514100232571]; coppel.com [entidad 1444276872316871].

## Epazote: Messenger, una captura de WhatsApp y Google Maps

**E019319** · 2026-08-27T21:25:17.000000-06:00 · Messenger · Epazote Tulancingo · Adilenee Razo: En su página de Google maps dice que el día de hoy está cerrado
S438 · message_index_1based=45; línea 13, columna 16063

**E019331** · 2026-08-27T21:50:40.000000-06:00 · Messenger · Epazote Tulancingo · Adilenee Razo: Toca "Confirmar pago" para verificar el comprobante y avisar a Epazote Tulancingo que realizaste el pago. Confirmar pago
S438 · message_index_1based=36; línea 13, columna 12726

**E019344** · 2026-08-27T21:57:22.000000-06:00 · Messenger · Epazote Tulancingo · Adilenee Razo: Lo que pasa es sé no hizo tarde y queríamos avisar que llegaríamos a las 9 pero decía que cerraban a esa hora y después ví en Google maps que era a las 10 y como ya se realizó el pago pues para que la reservación sea para el día de mañana
S438 · message_index_1based=23; línea 13, columna 8117

Se inspeccionó visualmente la foto adjunta enviada el 27-08-2026 a las 21:50:38 (E019330; S438 · message_index_1based=37; línea 13, columna 13153). Es una captura de una conversación de WhatsApp con 'Epazote / Restaurante Epazote', que incluye un comprobante por $650.00, concepto 'paquete', referencia 7116298, beneficiario visible Rafael Santos y cuentas bancarias parcialmente ocultas. La referencia 7116298 es bancaria, no un identificador de empresa de Facebook o de Google. No se atribuye al beneficiario la propiedad legal del restaurante. La captura no proporciona un historial completo de WhatsApp ni un enlace a su cuenta.

[Foto original: captura y comprobante](file:///home/deep-logic/Documentos/facebook/your_facebook_activity/messages/inbox/epazotetulancingo_1514670583749704/photos/1395635869197307.jpg)

El texto de Messenger menciona el horario de Google Maps, pero no incluye un enlace a la ficha ni su ID. No se encontró una consulta de Epazote en los registros de Google que permita confirmar la misma visita. La relación con Maps proviene del texto de los mensajes. El botón Confirmar pago es una pista de verificación de comprobante con imagen; no demuestra que sea la búsqueda sobre validar más rápido que se recuerda.

## Coppel: una relación comprobable entre Facebook y Google Play

El 03-08-2026 a las 21:31:46 se registró un clic de anuncio cuyo título/destino indica com.coppel.coppelapp. El ID de biblioteca de anuncios es 2475207562964622. La misma cadena de paquete aparece en Google Play, Analytics y Publicidad. Es una relación por paquete de aplicación, sin afirmar que el anuncio causó los usos posteriores.

**E016950** · 2026-08-03T21:31:46.000000-06:00 · Anunciantes con los que interactuaste · Acción
Clic
Título
http://play.google.com/store/apps/details?id=com.coppel.coppelapp
URL pública de la biblioteca de anuncios
https://www.facebook.com/ads/library/?id=2475207562964622
URL
https://www.facebook.com/tiendascoppel/posts/pfbid02zQM9YcGqykwunYPveL647kTsmMunxFa79qzhtE4oLGJQWHMFAKJRWX5gMRyZk9S8l
S101 · section_index_1based=13; línea 13, columna 7125

[Abrir fuente web](https://www.facebook.com/ads/library/?id=2475207562964622)

**E017165** · 2026-08-04T18:33:20.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=4272; línea 33, columna 4245057

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E017507** · 2026-08-08T04:13:20.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=4055; línea 33, columna 4029793

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E017653** · 2026-08-08T20:36:40.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=4008; línea 33, columna 3982952

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E018106** · 2026-08-16T02:46:40.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=3835; línea 33, columna 3811772

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E018122** · 2026-08-16T10:16:40.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=3815; línea 33, columna 3791749

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E021395** · 2026-09-08T23:26:45.000000-06:00 · Google Analytics · Has utilizado Coppel: compras en línea
S012 · record_index_1based=290; línea 33, columna 313990

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E021396** · 2026-09-08T23:26:45.000000-06:00 · Publicidad · Has utilizado Coppel: compras en línea
S024 · record_index_1based=245; línea 33, columna 289523

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E021434** · 2026-09-09T02:36:40.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=2466; línea 33, columna 2452497

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

[Aplicación Coppel en Google Play](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

[Referencia de anuncio de Coppel](https://www.facebook.com/ads/library/?id=2475207562964622)

En actividad fuera de Meta también figuran Coppel (entidad 10153514100232571) y coppel.com (entidad 1444276872316871), con cuatro valores de Identificador de evento compartidos. Este cruce se documenta por separado del ID de anuncio y del paquete Android; no existe una conversión demostrada entre esos números.

## Qué es la carpeta files

Contiene 181 archivos: 179 PNG sin extensión, un logo de Facebook llamado fb_logo.png y una imagen pequeña llamada profile_pic.jpg. Las 179 imágenes numeradas están enlazadas desde your_facebook_activity/ai/your_files.html, en la lista de archivos creados. Las 179 contienen metadatos Software de Matplotlib. La imagen 1079358437649748 se inspeccionó: es una representación de x=1. Su número identifica un archivo en el export, sin relación demostrada con las empresas.

[Listado original de archivos de IA](file:///home/deep-logic/Documentos/facebook/your_facebook_activity/ai/your_files.html)

Se registraron las fechas de creación que da la lista de IA. El logo y la foto se inspeccionaron y se conservan sin inventarles una fecha. El inventario incluye formato por firma binaria, tamaño, SHA-256 y referencia de origen de cada imagen numerada.

## Dos vías para consultar mensajes; límites de esta copia

La copia local contiene 37 archivos de conversación y 1.755 mensajes fechados. Hay otros 38 bloques sin fecha: por ejemplo, foto del grupo y configuración del enlace de invitación. Se conservan fuera de la línea temporal para no asignarles horas inventadas.

[Índice local de tus mensajes](file:///home/deep-logic/Documentos/facebook/your_facebook_activity/messages/your_messages.html)

El archivo Conversaciones secretas indica Sí tanto para mensajes enviados como recibidos, y lista dispositivos. Es información de uso, no el contenido descifrado de todas esas conversaciones. Este export no permite concluir que estén todos tus mensajes.

[Metadatos locales de conversaciones secretas](file:///home/deep-logic/Documentos/facebook/your_facebook_activity/messages/secret_conversations.html)

Otra vía documentada por Meta es recuperar el historial cifrado mediante el almacenamiento seguro de Messenger, con PIN de seis dígitos o una clave conservada en Google Drive o iCloud. Esta es una explicación externa del mecanismo; no se recuperó un PIN o una clave de respaldo de Messenger en esta revisión. [F01]

[Meta: historial cifrado y almacenamiento seguro de Messenger](https://about.fb.com/news/2024/03/end-to-end-encryption-on-messenger-explained/)

La página de ayuda sobre descarga del historial cifrado no permitió verificar sus instrucciones. Se registró el intento fallido, sin presentar pasos no comprobados. [F04]

## Google: ver y administrar una empresa

El 26-09-2026, después de las búsquedas VAPID, aparece la consulta perfil negocios google a las 22:29:46 y visitas a business.google.com, incluida la pantalla de creación y un registro de Perfil de Empresa en Google. Son visitas documentadas; no prueban que se haya creado o administrado una ficha.

**E026747** · 2026-09-26T22:29:46.000000-06:00 · Búsqueda · perfil negocios google
S004 · record_index_1based=4; línea 33, columna 3190

[Abrir fuente web](https://www.google.com/search?q=perfil+negocios+google)

**E026748** · 2026-09-26T22:29:51.142605-06:00 · Historial de Chrome · Muestra tu empresa en Google: Perfil de Negocio de Google
S028 · record_index_1based=63

[Abrir fuente web](https://business.google.com/es-all/business-profile/)

**E026749** · 2026-09-26T22:30:02.753842-06:00 · Historial de Chrome · Muestra tu empresa en Google: Perfil de Negocio de Google
S028 · record_index_1based=62

[Abrir fuente web](https://business.google.com/es-all/business-profile/)

**E026750** · 2026-09-26T22:30:06.000000-06:00 · Chrome · Haz que tu empresa aparezca en Google
S008 · record_index_1based=18; línea 33, columna 14195

[Abrir fuente web](https://business.google.com/create/new?gmbsrc=all-es-419-z-z-z-gmb-s-z-u~bgcmhp-hom_hr-u&hl=es-419&skipLandingPage=&skipPagesList=1&cbl=hr&cbp=hom&cbt=now&service=ome&original_intent=GMB)

**E026751** · 2026-09-26T22:30:06.453130-06:00 · Historial de Chrome · Haz que tu empresa aparezca en Google
S028 · record_index_1based=61

[Abrir fuente web](https://business.google.com/create/new?gmbsrc=all-es-419-z-z-z-gmb-s-z-u~bgcmhp-hom_hr-u&hl=es-419&skipLandingPage=&skipPagesList=1&cbl=hr&cbp=hom&cbt=now&service=ome&original_intent=GMB)

**E026752** · 2026-09-26T22:30:07.000000-06:00 · Perfil de Empresa en Google · Viste Registro
S022 · record_index_1based=1; línea 33, columna 43

[Abrir fuente web](https://business.google.com/)

**E026753** · 2026-09-26T22:30:12.000000-06:00 · Búsqueda · Muestra tu empresa en Google: Perfil de Negocio de Google
S004 · record_index_1based=3; línea 33, columna 2166

[Abrir fuente web](https://business.google.com/es-all/business-profile/)

**E026754** · 2026-09-26T22:30:12.000000-06:00 · Chrome · Muestra tu empresa en Google: Perfil de Negocio de Google
S008 · record_index_1based=17; línea 33, columna 13496

[Abrir fuente web](https://business.google.com/es-all/business-profile/)

**E026755** · 2026-09-26T22:30:12.887103-06:00 · Historial de Chrome · Muestra tu empresa en Google: Perfil de Negocio de Google
S028 · record_index_1based=60

[Abrir fuente web](https://business.google.com/es-all/business-profile/)

La exportación específica del producto contiene name=accounts/118064871121168977834, accountName=Adilene Hernández Razo y type=PERSONAL. Referencia S076: data.json, /name, /accountName y /type. El número 118064871121168977834 identifica este recurso de cuenta, no una ficha individual. businessPersonalization.json está vacío. En esta carpeta no hay locations ni un ID de ficha de negocio.

[Cuenta exportada de Perfil de Negocio](file:///home/deep-logic/Documentos/Registro/Takeout/Perfil%C2%A0de%C2%A0Negocio%C2%A0de%C2%A0Google/account-118064871121168977834/data.json)

La documentación de Google permite encontrar la empresa en Búsqueda o Maps con la cuenta asociada. Para consultar el ID de una ficha: abrir el Perfil de Negocio → Más → Configuración del Perfil de Negocio → Configuración avanzada. Ese ID pertenece a Google; no se ha encontrado una equivalencia con los números de Facebook. [F02, F03]

[Google: configuración avanzada e ID del Perfil de Negocio](https://support.google.com/business/answer/10737668?hl=es-419)

[Google: encontrar una empresa en Búsqueda y Maps](https://support.google.com/business/answer/145585?hl=es-419)

Los 16 registros de Chat y 290 de Gmail dentro de Mi actividad son actividad del producto; esa carpeta no equivale al contenido de conversaciones o correos. Por separado se incorporaron tres conversaciones exportadas de Gemini en Workspace con preguntas, respuestas, fechas y enlaces de sus citas.

## VAPID y la pista de validación con imagen: hallazgos anteriores

Se mantienen las búsquedas vapid y vapid web push del 26-09-2026 a las 22:28:27 y 22:28:32 y los dos artículos visitados después. Ocho observaciones de Search, Chrome y Browser History corresponden a cuatro eventos en el cruce original, conservado en datos/cruce.json.

[Artículo visitado: VAPID en Medium](https://medium.com/bawilabs/web-push-notifications-through-vapid-method-7d4d6927a006)

[Artículo visitado: protocolo Web Push](https://web.dev/articles/push-notifications-web-push-protocol?hl=es-419)

Se recuperó una clave privada VAPID de sharing.vapid_key en Configuración.json. Se validó como EC P-256 y pertenece al componente sharing de Chrome; no se demostró que sea la clave de un servidor Web Push propio. Su valor permanece en privado/claves-recuperadas.md, privado/vapid-recuperada.json y privado/vapid-private.pem. No se encontraron contraseñas de acceso en los exportes revisados. El PDF presenta metadatos y referencias de la clave, sin copiar el valor privado.

La búsqueda aproximada sobre validar con una imagen más rápido sigue sin una consulta explícita coincidente. Se conservan candidatos de identidad, mensajes de Google y Lens, y ahora la captura de comprobante de Epazote como pista relacionada. Ninguno confirma todavía el método que se recuerda.

## Cómo se construye y se actualiza la cronología

Se conservan todas las observaciones extraídas: una visita puede aparecer en varios productos. No se eliminan registros por parecer duplicados. La igualdad de URL en fuentes Google distintas a hasta dos segundos se marca como posible misma visita. Los resúmenes y detalles de actividad fuera de Meta se relacionan por nombre, campo de identificador, tipo y minuto, sin sustituir sus tiempos originales.

Hay 684 relaciones automáticas propuestas en datos/actividad-correlaciones.json. Cada observación tiene ID de esta versión, fecha original, precisión, fuente y localizador de registro. El catálogo permite volver al HTML/JSON/CSV original y comprobar SHA-256. Los originales fueron verificados sin modificaciones.

Las horas de Facebook llevan UTC-06:00 según su encabezado. Se convierten a America/Mexico_City; para 2022 la hora local puede cambiar por el horario de verano histórico. Los registros con precisión de minuto conservan esa precisión aunque la representación ISO muestre segundos 00. Dos transacciones CSV de Google Pay no explicitan zona: se asume México y se marca la incertidumbre. No se deduce cuándo ocurrió un clic a partir de una actualización musical. Fechas de instalación, actualización, alta de dispositivo o vencimiento se etiquetan como tales, no como búsquedas ni usos de apps.

Alcance: los 27 HTML de Mi actividad y el historial JSON de Chrome; fechas explícitas de JSON de otros productos y CSV con fecha reconocible; conversaciones y secciones fechadas de los 386 HTML de Facebook; detalle y resumen de actividad fuera de Meta y archivos IA. Este PDF es una reconstrucción de las copias disponibles, no una garantía de que contengan todo lo sucedido en las cuentas. No se han integrado citas de calendario como navegación ni tratado preferencias sin fecha como acciones.

Los enlaces de acceso se depuran de parámetros privados en el PDF y visor; las URLs originales permanecen en privado/actividad-observaciones-originales.json. Las búsquedas y mensajes se muestran con su texto. El visor HTML funciona sin conexión y permite filtrar fecha, servicio, texto e identificador, alternar orden y abrir los archivos originales. El CSV incluye toda la cronología para consulta externa. El PDF conserva el orden global de más antiguo a más reciente.

<!-- FIN_RESULTADOS_SESION_3 -->


<!-- INICIO_RESULTADOS_SESION_4 -->
## Sesión 4: pistas aportadas durante la integración

## Pista del 21 de septiembre: Etsy, Clarín, Hermès y Hermes Agent

Se buscó ETSI/Etsy y Clarín/Hermes con variantes de acentos en los archivos HTML, JSON, CSV y TXT originales. La coincidencia relacionada con esa noche es Etsy (etsy.com). En México el recorrido es del 20 de septiembre, aproximadamente 21:13–23:12; en UTC corresponde al 21. Ejemplo: 20-09 21:13:29 UTC-06 equivale a 21-09 03:13:29 UTC. Se muestran ambas horas para que puedas comparar con tus recuerdos.

## Los números de Etsy y Clarín, con su campo exacto

Etsy: Identificador en encabezado = 1594897960568214. Identificadores dentro de eventos = 114623403312281 y 297472060462208. Número de producto visitado en la URL /listing/ = 4303042674. Referencia de entidad: S229; encabezado de etsycom_105529809654844415.html.

[Archivo original: etsy.com](file:///home/deep-logic/Documentos/facebook/apps_and_websites_off_of_facebook/your_activity_off_meta_technologies/etsycom_105529809654844415.html)

Clarín: Identificador en encabezado = 1563990080334439. Identificador dentro de eventos = 455329408009530. Referencia: S214; encabezado de clarincom_105529809654844415.html.

[Archivo original: clarin.com](file:///home/deep-logic/Documentos/facebook/apps_and_websites_off_of_facebook/your_activity_off_meta_technologies/clarincom_105529809654844415.html)

Coincidencia comprobada: los dos nombres de archivo terminan en 105529809654844415. Sus campos de Identificador de entidad y de eventos son diferentes. El export no explica el significado del sufijo; se conserva como un sufijo compartido de archivo. La igualdad no permite concluir que sea un código de acceso, un identificador de persona compartido ni una cuenta unificada.

## Número buscado justo antes de Etsy: 6850175308

A las 21:12:50 del 20 de septiembre (03:12:50 UTC del día 21) aparece la consulta 6850175308; 39 segundos después está la visita a Etsy. Referencia Búsqueda #170. También se buscó ese número en Google Chat a las 20:47:22 (Chat #1): ese registro es una búsqueda, no un mensaje enviado. Se había consultado repetidamente el 14 y 15 de septiembre y el día 20 a las 16:11:03.

**E023172** · México 2026-09-14T11:00:51.000000-06:00 · UTC 2026-09-14T17:00:51.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 311, "html_line_1based": 34, "html_column_0based": 297861}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E023182** · México 2026-09-14T12:17:55.000000-06:00 · UTC 2026-09-14T18:17:55.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 310, "html_line_1based": 34, "html_column_0based": 296699}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E023230** · México 2026-09-14T20:13:32.000000-06:00 · UTC 2026-09-15T02:13:32.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 307, "html_line_1based": 34, "html_column_0based": 293182}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E023275** · México 2026-09-14T22:12:26.000000-06:00 · UTC 2026-09-15T04:12:26.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 293, "html_line_1based": 34, "html_column_0based": 276638}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E023311** · México 2026-09-14T23:04:27.000000-06:00 · UTC 2026-09-15T05:04:27.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 292, "html_line_1based": 34, "html_column_0based": 275476}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E023338** · México 2026-09-15T01:29:15.000000-06:00 · UTC 2026-09-15T07:29:15.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 290, "html_line_1based": 34, "html_column_0based": 273107}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E023476** · México 2026-09-15T11:18:48.000000-06:00 · UTC 2026-09-15T17:18:48.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 274, "html_line_1based": 34, "html_column_0based": 254324}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E023488** · México 2026-09-15T11:51:34.000000-06:00 · UTC 2026-09-15T17:51:34.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 270, "html_line_1based": 34, "html_column_0based": 249664}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E024466** · México 2026-09-20T16:11:03.000000-06:00 · UTC 2026-09-20T22:11:03.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 177, "html_line_1based": 34, "html_column_0based": 145791}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E024553** · México 2026-09-20T20:47:22.000000-06:00 · UTC 2026-09-21T02:47:22.000000+00:00
Chat · 6850175308
S007 · {"record_index_1based": 1, "html_line_1based": 33, "html_column_0based": 43}

[Abrir enlace](https://mail.google.com/chat/#search/6850175308)

**E024567** · México 2026-09-20T21:12:50.000000-06:00 · UTC 2026-09-21T03:12:50.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 170, "html_line_1based": 34, "html_column_0based": 137950}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E025875** · México 2026-09-25T15:24:48.502037-06:00 · UTC 2026-09-25T21:24:48.502037+00:00
Historial de Chrome · Xiaomi Account
S028 · {"record_index_1based": 146, "json_pointer": "/Browser History/145"}

[Abrir enlace](https://account.xiaomi.com/fe/service/account?cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&userId=6850175308)

**E025876** · México 2026-09-25T15:24:49.124575-06:00 · UTC 2026-09-25T21:24:49.124575+00:00
Historial de Chrome · Xiaomi Account
S028 · {"record_index_1based": 145, "json_pointer": "/Browser History/144"}

[Abrir enlace](https://account.xiaomi.com/fe/service/account?cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&userId=6850175308&_locale=en_US)

**E025879** · México 2026-09-25T15:25:33.256443-06:00 · UTC 2026-09-25T21:25:33.256443+00:00
Historial de Chrome · Xiaomi Account
S028 · {"record_index_1based": 142, "json_pointer": "/Browser History/141"}

[Abrir enlace](https://account.xiaomi.com/auth/jump?target=https%3A%2F%2Faccount.xiaomi.com%2Ffe%2Fservice%2Faccount%2Fprivacy%3FcUserId%3DwAb6f4ntA20ZEJ6WDRaIbXk_M8I%26userId%3D6850175308%26_locale%3Den_US&cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&userId=6850175308)

**E025880** · México 2026-09-25T15:25:33.788076-06:00 · UTC 2026-09-25T21:25:33.788076+00:00
Historial de Chrome · Xiaomi Account
S028 · {"record_index_1based": 141, "json_pointer": "/Browser History/140"}

[Abrir enlace](https://account.xiaomi.com/fe/service/account/privacy?cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&_locale=en_US&userId=6850175308)

**E025881** · México 2026-09-25T15:25:38.000000-06:00 · UTC 2026-09-25T21:25:38.000000+00:00
Chrome · Xiaomi Account
S008 · {"record_index_1based": 53, "html_line_1based": 33, "html_column_0based": 53412}

[Abrir enlace](https://account.xiaomi.com/fe/service/account/privacy/application?cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&_locale=en_US&userId=6850175308)

**E025882** · México 2026-09-25T15:25:38.671916-06:00 · UTC 2026-09-25T21:25:38.671916+00:00
Historial de Chrome · Xiaomi Account
S028 · {"record_index_1based": 140, "json_pointer": "/Browser History/139"}

[Abrir enlace](https://account.xiaomi.com/fe/service/account/privacy/application?cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&_locale=en_US&userId=6850175308)

El 25 de septiembre aparece el mismo número en el parámetro userId=6850175308 de URLs de account.xiaomi.com. En los contactos figura TEL;TYPE=CELL:+526850175308. Estas son dos representaciones literales distintas; el export no verifica que sea un teléfono activo ni que las fichas identifiquen a un mismo titular. No coincide con los campos Identificador de entidad o de evento de Etsy/Clarín.

V01 · tarjeta vCard #46 · FN:Amante Adilene ; N:;Amante Adilene;;; ; TEL;TYPE=CELL:+526850175308

[Contacto original](file:///home/deep-logic/Documentos/Registro/Takeout/Contactos/Mis%20contactos/Mis%20contactos.vcf)

V02 · tarjeta vCard #50 · FN:Amante Adilene ; N:;Amante Adilene;;; ; TEL;TYPE=CELL:+526850175308

[Contacto original](file:///home/deep-logic/Documentos/Registro/Takeout/Contactos/Todos%20los%20contactos/Todos%20los%20contactos.vcf)

V02 · tarjeta vCard #51 · FN:Amante Adilene Tu Juras ; N:;Amante Adilene Tu Juras;;; ; TEL;TYPE=CELL:+526850175308

[Contacto original](file:///home/deep-logic/Documentos/Registro/Takeout/Contactos/Todos%20los%20contactos/Todos%20los%20contactos.vcf)

La interpretación de que este número permite identificarse en Etsy, Clarín o Hermes queda sin comprobar. No se encontró el número en los archivos originales de Facebook. Las URLs de Xiaomi dan una referencia de cuenta mucho más explícita que la proximidad temporal con una visita a Etsy, sin demostrar un inicio de sesión exitoso.

## Qué se envió y qué se recibió

El archivo de Etsy enumera nueve registros de actividad recibida con tipos PAGE_VIEW y VIEW_CONTENT, todos del 20 de septiembre. Un resumen reproduce los mismos nueve registros. A las 21:13 aparecen ambos tipos, y a las 21:50 otra PAGE_VIEW. El texto del export dice Recibida el y pertenece a actividad fuera de Meta: no contiene un mensaje enviado a Etsy, su texto, destinatario ni adjunto.

Según Meta, esta sección recoge información que sitios y apps comparten con Meta, susceptible de asociarse a una cuenta para publicidad. Eso respalda la interpretación de un envío de actividad del sitio hacia Meta, sin demostrar que el usuario haya enviado manualmente algo al número de la empresa. [P03]

[Meta: información de actividad compartida por apps y sitios](https://about.fb.com/news/2019/08/off-facebook-activity/)

Las visitas a Clarín del 20 de septiembre sí aparecen en Google Analytics y Publicidad. En el detalle fuera de Meta de clarin.com, los eventos conservados son del 8 y 28 de agosto; no hay allí un evento del 20/21 de septiembre que una numéricamente Etsy con Clarín.

## Secuencia recuperada: visitas, consultas y páginas de cuenta

**E024567** · México 2026-09-20T21:12:50.000000-06:00 · UTC 2026-09-21T03:12:50.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 170, "html_line_1based": 34, "html_column_0based": 137950}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E024572** · México 2026-09-20T21:13:29.000000-06:00 · UTC 2026-09-21T03:13:29.000000+00:00
Búsqueda · Pendiente de sol en oro macizo, piercing para labio en oro macizo ...
S004 · {"record_index_1based": 169, "html_line_1based": 34, "html_column_0based": 136819}

[Abrir enlace](https://www.etsy.com/es/listing/4303042674/pendiente-de-sol-en-oro-macizo-piercing)

**E024573** · México 2026-09-20T21:13:36.000000-06:00 · UTC 2026-09-21T03:13:36.000000+00:00
Google Analytics · www.etsy.com/es/listing/4303042674/pendiente-de-sol-en-oro-macizo-piercing
S012 · {"record_index_1based": 137, "html_line_1based": 33, "html_column_0based": 146988}

[Abrir enlace](http://www.etsy.com/es/listing/4303042674/pendiente-de-sol-en-oro-macizo-piercing)

**E024575** · México 2026-09-20T21:18:59.000000-06:00 · UTC 2026-09-21T03:18:59.000000+00:00
Búsqueda · g.co/sc
S004 · {"record_index_1based": 168, "html_line_1based": 34, "html_column_0based": 135664}

[Abrir enlace](https://www.google.com/search?q=g.co%2Fsc)

**E024578** · México 2026-09-20T21:32:10.000000-06:00 · UTC 2026-09-21T03:32:10.000000+00:00
Google Analytics · miperfil.clarin.com/
S012 · {"record_index_1based": 135, "html_line_1based": 33, "html_column_0based": 144822}

[Abrir enlace](http://miperfil.clarin.com/)

**E024579** · México 2026-09-20T21:36:31.000000-06:00 · UTC 2026-09-21T03:36:31.000000+00:00
Búsqueda · clarin
S004 · {"record_index_1based": 167, "html_line_1based": 34, "html_column_0based": 134335}

[Abrir enlace](https://www.google.com/search?q=clarin)

**E024584** · México 2026-09-20T21:40:31.000000-06:00 · UTC 2026-09-21T03:40:31.000000+00:00
Búsqueda · inwebo authenticator
S004 · {"record_index_1based": 164, "html_line_1based": 34, "html_column_0based": 130939}

[Abrir enlace](https://www.google.com/search?q=inwebo+authenticator)

**E024587** · México 2026-09-20T21:42:20.000000-06:00 · UTC 2026-09-21T03:42:20.000000+00:00
Google Analytics · www.hermes.com/mx/es/
S012 · {"record_index_1based": 131, "html_line_1based": 33, "html_column_0based": 140589}

[Abrir enlace](http://www.hermes.com/mx/es/)

**E024588** · México 2026-09-20T21:42:20.000000-06:00 · UTC 2026-09-21T03:42:20.000000+00:00
Google Analytics · www.hermes.com/mx/es/login/
S012 · {"record_index_1based": 132, "html_line_1based": 33, "html_column_0based": 141645}

[Abrir enlace](http://www.hermes.com/mx/es/login/)

**E024594** · México 2026-09-20T21:44:31.000000-06:00 · UTC 2026-09-21T03:44:31.000000+00:00
Traductor de Google · el sitio web traducido https://hermes-agent.nousresearch.com/docs/user-guide/messaging
S026 · {"record_index_1based": 1, "html_line_1based": 33, "html_column_0based": 43}

[Abrir enlace](https://hermes--agent-nousresearch-com.translate.goog/docs/user-guide/messaging?_x_tr_sl=auto&_x_tr_tl=es&_x_tr_hl=es-419&_x_tr_pto=tc)

**E024595** · México 2026-09-20T21:47:08.000000-06:00 · UTC 2026-09-21T03:47:08.000000+00:00
Google Analytics · postlogin.clarin.com/post-login
S012 · {"record_index_1based": 129, "html_line_1based": 33, "html_column_0based": 138369}

[Abrir enlace](http://postlogin.clarin.com/post-login)

**E024600** · México 2026-09-20T21:48:56.266751-06:00 · UTC 2026-09-21T03:48:56.266751+00:00
Google Play Store · Installs · Installs · firstInstallationTime · TrustBuilder Authenticator
S058 · {"json_pointer": "/367/install/firstInstallationTime"}

**E024601** · México 2026-09-20T21:48:56.266751-06:00 · UTC 2026-09-21T03:48:56.266751+00:00
Google Play Store · Installs · Installs · lastUpdateTime · TrustBuilder Authenticator
S058 · {"json_pointer": "/367/install/lastUpdateTime"}

**E024603** · México 2026-09-20T21:49:27.000000-06:00 · UTC 2026-09-21T03:49:27.000000+00:00
Google Play Store · TrustBuilder Authenticator
S016 · {"record_index_1based": 276, "html_line_1based": 33, "html_column_0based": 274049}

[Abrir enlace](https://play.google.com/store/apps/details?id=com.inwebo.near.prod)

**E024633** · México 2026-09-20T22:56:36.000000-06:00 · UTC 2026-09-21T04:56:36.000000+00:00
Google Analytics · www.hermes.com/us/en/account/create/
S012 · {"record_index_1based": 111, "html_line_1based": 33, "html_column_0based": 117884}

[Abrir enlace](http://www.hermes.com/us/en/account/create/)

**E024635** · México 2026-09-20T22:58:55.000000-06:00 · UTC 2026-09-21T04:58:55.000000+00:00
Búsqueda · Hermes Agent — Open-Source AI Agent That Grows With You ...
S004 · {"record_index_1based": 150, "html_line_1based": 34, "html_column_0based": 112759}

[Abrir enlace](https://hermes-agent.nousresearch.com/)

**E024636** · México 2026-09-20T22:59:59.000000-06:00 · UTC 2026-09-21T04:59:59.000000+00:00
Búsqueda · hermes agent
S004 · {"record_index_1based": 149, "html_line_1based": 34, "html_column_0based": 111593}

[Abrir enlace](https://www.google.com/search?q=hermes+agent)

**E024638** · México 2026-09-20T23:01:38.000000-06:00 · UTC 2026-09-21T05:01:38.000000+00:00
Google Analytics · www.hermes.com/us/en/login/
S012 · {"record_index_1based": 108, "html_line_1based": 33, "html_column_0based": 114671}

[Abrir enlace](http://www.hermes.com/us/en/login/)

**E024644** · México 2026-09-20T23:07:02.000000-06:00 · UTC 2026-09-21T05:07:02.000000+00:00
Google Analytics · www.hermes.com/us/en/
S012 · {"record_index_1based": 106, "html_line_1based": 33, "html_column_0based": 112548}

[Abrir enlace](http://www.hermes.com/us/en/)

**E024681** · México 2026-09-20T23:36:40.000000-06:00 · UTC 2026-09-21T05:36:40.000000+00:00
Google Play Store · Se ha utilizado TrustBuilder Authenticator
S016 · {"record_index_1based": 412, "html_line_1based": 33, "html_column_0based": 409776}

[Abrir enlace](https://play.google.com/store/apps/details?id=com.inwebo.near.prod)

**E024467** · México 2026-09-20T16:12:12.000000-06:00 · UTC 2026-09-20T22:12:12.000000+00:00
Google Analytics · portal.nousresearch.com/cloud
S012 · {"record_index_1based": 147, "html_line_1based": 33, "html_column_0based": 157875}

[Abrir enlace](http://portal.nousresearch.com/cloud)

**E024468** · México 2026-09-20T16:13:44.000000-06:00 · UTC 2026-09-20T22:13:44.000000+00:00
Google Analytics · portal.nousresearch.com/orgs/3d6ba8ff/billing
S012 · {"record_index_1based": 146, "html_line_1based": 33, "html_column_0based": 156747}

[Abrir enlace](http://portal.nousresearch.com/orgs/3d6ba8ff/billing)

**E024469** · México 2026-09-20T16:14:57.000000-06:00 · UTC 2026-09-20T22:14:57.000000+00:00
Google Analytics · portal.nousresearch.com/
S012 · {"record_index_1based": 145, "html_line_1based": 33, "html_column_0based": 155682}

[Abrir enlace](http://portal.nousresearch.com/)

**E024476** · México 2026-09-20T16:17:50.000000-06:00 · UTC 2026-09-20T22:17:50.000000+00:00
Google Analytics · portal.nousresearch.com/login
S012 · {"record_index_1based": 144, "html_line_1based": 33, "html_column_0based": 154602}

[Abrir enlace](http://portal.nousresearch.com/login)

**E024608** · México 2026-09-20T21:59:47.000000-06:00 · UTC 2026-09-21T03:59:47.000000+00:00
Google Analytics · portal.nousresearch.com/manage-subscription
S012 · {"record_index_1based": 124, "html_line_1based": 33, "html_column_0based": 132591}

[Abrir enlace](http://portal.nousresearch.com/manage-subscription)

**E024609** · México 2026-09-20T22:05:38.000000-06:00 · UTC 2026-09-21T04:05:38.000000+00:00
Google Analytics · portal.nousresearch.com/orgs/3d6ba8ff/billing
S012 · {"record_index_1based": 123, "html_line_1based": 33, "html_column_0based": 131462}

[Abrir enlace](http://portal.nousresearch.com/orgs/3d6ba8ff/billing)

**E024610** · México 2026-09-20T22:16:28.000000-06:00 · UTC 2026-09-21T04:16:28.000000+00:00
Google Analytics · portal.nousresearch.com/orgs/3d6ba8ff/api-keys
S012 · {"record_index_1based": 122, "html_line_1based": 33, "html_column_0based": 130330}

[Abrir enlace](http://portal.nousresearch.com/orgs/3d6ba8ff/api-keys)

**E024611** · México 2026-09-20T22:16:49.000000-06:00 · UTC 2026-09-21T04:16:49.000000+00:00
Google Analytics · portal.nousresearch.com/cloud
S012 · {"record_index_1based": 121, "html_line_1based": 33, "html_column_0based": 129249}

[Abrir enlace](http://portal.nousresearch.com/cloud)

**E024612** · México 2026-09-20T22:17:02.000000-06:00 · UTC 2026-09-21T04:17:02.000000+00:00
Google Analytics · portal.nousresearch.com/orgs/3d6ba8ff/agents
S012 · {"record_index_1based": 120, "html_line_1based": 33, "html_column_0based": 128123}

[Abrir enlace](http://portal.nousresearch.com/orgs/3d6ba8ff/agents)

**E024637** · México 2026-09-20T23:00:20.000000-06:00 · UTC 2026-09-21T05:00:20.000000+00:00
Google Analytics · portal.nousresearch.com/cloud
S012 · {"record_index_1based": 109, "html_line_1based": 33, "html_column_0based": 115746}

[Abrir enlace](http://portal.nousresearch.com/cloud)

**E024640** · México 2026-09-20T23:02:35.000000-06:00 · UTC 2026-09-21T05:02:35.000000+00:00
Búsqueda · https://portal.nousresearch.com/
S004 · {"record_index_1based": 147, "html_line_1based": 34, "html_column_0based": 108937}

[Abrir enlace](https://portal.nousresearch.com/)

**E024641** · México 2026-09-20T23:03:11.000000-06:00 · UTC 2026-09-21T05:03:11.000000+00:00
Google Analytics · portal.nousresearch.com/
S012 · {"record_index_1based": 107, "html_line_1based": 33, "html_column_0based": 113605}

[Abrir enlace](http://portal.nousresearch.com/)

**E024646** · México 2026-09-20T23:11:40.000000-06:00 · UTC 2026-09-21T05:11:40.000000+00:00
Google Analytics · portal.nousresearch.com/orgs/3d6ba8ff/usage
S012 · {"record_index_1based": 104, "html_line_1based": 33, "html_column_0based": 110353}

[Abrir enlace](http://portal.nousresearch.com/orgs/3d6ba8ff/usage)

La visita a postlogin.clarin.com/post-login y las rutas de Hermès /login/ y /account/create/ son hechos del historial. El historial no guarda los formularios enviados ni una confirmación de inicio de sesión o alta, por lo que no prueba qué credencial se introdujo o si funcionó. Tampoco se demuestra que Etsy haya entregado una credencial para esos sitios.

Hermès de hermes.com es la tienda; Hermes Agent de hermes-agent.nousresearch.com es un proyecto de agente de IA. En el historial aparecen ambos. La documentación de mensajería de Hermes Agent fue visitada traducida a las 21:44:31. Su documentación actual usa autorización por usuarios/plataforma o emparejamiento; no describe que un ID empresarial de Etsy o Clarín dé acceso. [P04]

[Hermes Agent: pasarela de mensajería y autorizaciones](https://hermes-agent.nousresearch.com/docs/user-guide/messaging)

Ninguno de los seis números empresariales/de evento/sufijo enumerados aparece literalmente en los archivos de Google Takeout. Tampoco aparecen en el texto ni enlaces de los mensajes de Messenger. La hipótesis del usuario de identificarse con el mismo dato queda abierta, pendiente de precisar el número y la cuenta; no se convierte en conclusión. La secuencia cronológica se conserva como relación de navegación, no de autenticación.

## Pista adicional para validar con una imagen: inWebo / TrustBuilder

La misma noche hubo búsquedas inwebo authenticator, acceso a myinwebo.com y una primera instalación de TrustBuilder Authenticator a las 21:48:56.266751. El registro de uso de Google Play es de las 23:36:40. Esta es una nueva pista concreta para la consulta anterior sobre validar con una imagen, aunque no se encontró la frase exacta ni un QR de activación personal.

**E024470** · México 2026-09-20T16:15:48.000000-06:00 · UTC 2026-09-20T22:15:48.000000+00:00
Búsqueda · inwebo authenticator
S004 · {"record_index_1based": 176, "html_line_1based": 34, "html_column_0based": 144610}

[Abrir enlace](https://www.google.com/search?q=inwebo+authenticator)

**E024471** · México 2026-09-20T16:16:03.000000-06:00 · UTC 2026-09-20T22:16:03.000000+00:00
Búsqueda · inWebo Authenticator 6 para Android - Descargar
S004 · {"record_index_1based": 175, "html_line_1based": 34, "html_column_0based": 143532}

[Abrir enlace](https://inwebo-authenticator-6.softonic.com/android)

**E024472** · México 2026-09-20T16:16:08.000000-06:00 · UTC 2026-09-20T22:16:08.000000+00:00
Búsqueda · my inwebo authenticator
S004 · {"record_index_1based": 174, "html_line_1based": 34, "html_column_0based": 142345}

[Abrir enlace](https://www.google.com/search?q=my+inwebo+authenticator)

**E024473** · México 2026-09-20T16:16:11.000000-06:00 · UTC 2026-09-20T22:16:11.000000+00:00
Búsqueda · MyinWebo.com
S004 · {"record_index_1based": 173, "html_line_1based": 34, "html_column_0based": 141332}

[Abrir enlace](https://myinwebo.com/)

**E024474** · México 2026-09-20T16:16:37.000000-06:00 · UTC 2026-09-20T22:16:37.000000+00:00
Búsqueda · inwebo admin
S004 · {"record_index_1based": 172, "html_line_1based": 34, "html_column_0based": 140167}

[Abrir enlace](https://www.google.com/search?q=inwebo+admin)

**E024475** · México 2026-09-20T16:17:13.000000-06:00 · UTC 2026-09-20T22:17:13.000000+00:00
Búsqueda · https://www.myinwebo.com/console/logon
S004 · {"record_index_1based": 171, "html_line_1based": 34, "html_column_0based": 139111}

[Abrir enlace](https://www.myinwebo.com/console/logon)

**E024584** · México 2026-09-20T21:40:31.000000-06:00 · UTC 2026-09-21T03:40:31.000000+00:00
Búsqueda · inwebo authenticator
S004 · {"record_index_1based": 164, "html_line_1based": 34, "html_column_0based": 130939}

[Abrir enlace](https://www.google.com/search?q=inwebo+authenticator)

**E024585** · México 2026-09-20T21:40:35.000000-06:00 · UTC 2026-09-21T03:40:35.000000+00:00
Búsqueda · https://www.myinwebo.com/
S004 · {"record_index_1based": 163, "html_line_1based": 34, "html_column_0based": 129909}

[Abrir enlace](https://www.myinwebo.com/)

**E024600** · México 2026-09-20T21:48:56.266751-06:00 · UTC 2026-09-21T03:48:56.266751+00:00
Google Play Store · Installs · Installs · firstInstallationTime · TrustBuilder Authenticator
S058 · {"json_pointer": "/367/install/firstInstallationTime"}

**E024601** · México 2026-09-20T21:48:56.266751-06:00 · UTC 2026-09-21T03:48:56.266751+00:00
Google Play Store · Installs · Installs · lastUpdateTime · TrustBuilder Authenticator
S058 · {"json_pointer": "/367/install/lastUpdateTime"}

**E024603** · México 2026-09-20T21:49:27.000000-06:00 · UTC 2026-09-21T03:49:27.000000+00:00
Google Play Store · TrustBuilder Authenticator
S016 · {"record_index_1based": 276, "html_line_1based": 33, "html_column_0based": 274049}

[Abrir enlace](https://play.google.com/store/apps/details?id=com.inwebo.near.prod)

**E024681** · México 2026-09-20T23:36:40.000000-06:00 · UTC 2026-09-21T05:36:40.000000+00:00
Google Play Store · Se ha utilizado TrustBuilder Authenticator
S016 · {"record_index_1based": 412, "html_line_1based": 33, "html_column_0based": 409776}

[Abrir enlace](https://play.google.com/store/apps/details?id=com.inwebo.near.prod)

La documentación del fabricante describe autenticación mediante QR y activación con código o QR válido. Otra página distingue los parámetros sessionId, login y serviceId de la sesión de autenticación. No se recuperó ese serviceId personal ni se demostró una equivalencia con los números de Etsy. No se ha identificado el método como más rápido en tu caso. [P05, P06]

[TrustBuilder Authenticator móvil: QR y activación](https://docs.trustbuilder.com/mfa/trustbuilder-authenticator-mobile-app)

[TrustBuilder: parámetros de la autenticación con QR](https://docs.trustbuilder.com/mfa/web-sdk-qr-code-authentication)

## Google Fotos: metadatos diferentes y posible cuenta de negocios

En /home/deep-logic/Documentos se leyeron los metadatos de 289 imágenes: 5 de Takeout y 284 de Facebook. No se encontró una carpeta Google Fotos/Google Photos ni archivos JSON complementarios de fotos. Solo una imagen tiene un campo EXIF: Orientation=1 en un sticker. Las demás pueden conservar otros campos de PNG/JPEG, como Software o perfiles de color. Se verificó que no se modificaron los originales.

Se encontraron 57 grupos de imágenes con píxeles idénticos; en todos sus archivos el SHA-256 binario también coincide. En esta copia no se encontró un par con los mismos píxeles y bytes/metadatos distintos. Esto no descarta diferencias en fotos que no estén incluidas aquí. Los archivos de la muestra no permiten comparar un original con su descarga de Google Fotos.

Google distingue tres capas: fecha del archivo que puede cambiar al descargar; metadatos originales dentro de la imagen; información adicional de Google Fotos exportada en JSON. Una diferencia entre esas capas no demuestra por sí sola una vinculación a un negocio. [P01]

[Google Fotos: metadatos al exportar](https://support.google.com/photos/answer/3024190?hl=es)

Como ejemplo de evidencia explícita de vinculación, la API de Perfil de Negocio representa medios mediante accounts/{accountId}/locations/{locationId}/media/{mediaKey}. Una ruta de ese tipo, un registro de publicación o el enlace verificable a la misma imagen en una ficha ayudaría a comprobar la asociación. No se encontró esa relación para las imágenes revisadas. La forma de ese recurso no garantiza que aparezca en EXIF o en un export de Google Fotos. [P02]

[Google: medios de una ubicación de Perfil de Negocio](https://developers.google.com/my-business/reference/rest/v4/accounts.locations.media)

La hipótesis de vincular fotos mediante metadatos queda registrada como no comprobada. La comparación futura requiere las dos versiones concretas y sus JSON complementarios, si existen. No se atribuye a negocios el nombre Software=Matplotlib de los archivos IA de Facebook ni un horario de descarga.

<!-- FIN_RESULTADOS_SESION_4 -->


<!-- INICIO_RESULTADOS_SESION_5 -->
## Sesión 5: sitio portable y publicación pendiente

Solicitud: conservar las páginas locales de los datos, preparar GitHub y una carta personal. Nombre provisional: documentacion-adilene. La declaración del usuario no equivale a una conclusión del análisis.

Se prepara un sitio privado local con cronología, 482 fuentes, copias originales y vistas derivadas sin navegación externa. No se ha creado una cuenta ni publicado un repositorio. La cuenta requiere alta/verificación y conexión autorizada de GitHub.

GitHub Pages no se habilita automáticamente: la privacidad del repositorio no garantiza la privacidad de Pages. Referencia local G02 en referencias.html. Consulta del 1 de octubre de 2026.

Cuatro archivos contienen la clave VAPID; se conservan mediante respaldo cifrado y permanecen intactos en sus ubicaciones locales. La clave del respaldo no se incluye en el repositorio. El resto de research se copia para archivo privado. La carta se guarda como testimonio solicitado, sin verificación de las acusaciones.

Actualización preparada: 2026-10-01T15:27:19.200361+00:00. Las próximas actualizaciones requieren ejecutar el constructor; no hay una tarea automática ni vigilancia permanente.
<!-- FIN_RESULTADOS_SESION_5 -->
