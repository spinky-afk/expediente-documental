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

La cronología integra 84,642 observaciones fechadas de 508 archivos consultados, de 2022-08-15 a 2026-09-27. Google, Facebook y Uber se ordenan conjuntamente por instante UTC y se muestran en America/Mexico_City. Hay 54 secciones sin fecha o sin zona determinada, conservadas por separado.

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

**E020306** · 2026-08-27T21:25:17.000000-06:00 · Messenger · Epazote Tulancingo · Adilenee Razo: En su página de Google maps dice que el día de hoy está cerrado
S438 · message_index_1based=45; línea 13, columna 16063

**E020318** · 2026-08-27T21:50:40.000000-06:00 · Messenger · Epazote Tulancingo · Adilenee Razo: Toca "Confirmar pago" para verificar el comprobante y avisar a Epazote Tulancingo que realizaste el pago. Confirmar pago
S438 · message_index_1based=36; línea 13, columna 12726

**E020331** · 2026-08-27T21:57:22.000000-06:00 · Messenger · Epazote Tulancingo · Adilenee Razo: Lo que pasa es sé no hizo tarde y queríamos avisar que llegaríamos a las 9 pero decía que cerraban a esa hora y después ví en Google maps que era a las 10 y como ya se realizó el pago pues para que la reservación sea para el día de mañana
S438 · message_index_1based=23; línea 13, columna 8117

Se inspeccionó visualmente la foto adjunta enviada el 27-08-2026 a las 21:50:38 (E020317; S438 · message_index_1based=37; línea 13, columna 13153). Es una captura de una conversación de WhatsApp con 'Epazote / Restaurante Epazote', que incluye un comprobante por $650.00, concepto 'paquete', referencia 7116298, beneficiario visible Rafael Santos y cuentas bancarias parcialmente ocultas. La referencia 7116298 es bancaria, no un identificador de empresa de Facebook o de Google. No se atribuye al beneficiario la propiedad legal del restaurante. La captura no proporciona un historial completo de WhatsApp ni un enlace a su cuenta.

[Foto original: captura y comprobante](file:///home/deep-logic/Documentos/facebook/your_facebook_activity/messages/inbox/epazotetulancingo_1514670583749704/photos/1395635869197307.jpg)

El texto de Messenger menciona el horario de Google Maps, pero no incluye un enlace a la ficha ni su ID. No se encontró una consulta de Epazote en los registros de Google que permita confirmar la misma visita. La relación con Maps proviene del texto de los mensajes. El botón Confirmar pago es una pista de verificación de comprobante con imagen; no demuestra que sea la búsqueda sobre validar más rápido que se recuerda.

## Coppel: una relación comprobable entre Facebook y Google Play

El 03-08-2026 a las 21:31:46 se registró un clic de anuncio cuyo título/destino indica com.coppel.coppelapp. El ID de biblioteca de anuncios es 2475207562964622. La misma cadena de paquete aparece en Google Play, Analytics y Publicidad. Es una relación por paquete de aplicación, sin afirmar que el anuncio causó los usos posteriores.

**E017779** · 2026-08-03T21:31:46.000000-06:00 · Anunciantes con los que interactuaste · Acción
Clic
Título
http://play.google.com/store/apps/details?id=com.coppel.coppelapp
URL pública de la biblioteca de anuncios
https://www.facebook.com/ads/library/?id=2475207562964622
URL
https://www.facebook.com/tiendascoppel/posts/pfbid02zQM9YcGqykwunYPveL647kTsmMunxFa79qzhtE4oLGJQWHMFAKJRWX5gMRyZk9S8l
S101 · section_index_1based=13; línea 13, columna 7125

[Abrir fuente web](https://www.facebook.com/ads/library/?id=2475207562964622)

**E018004** · 2026-08-04T18:33:20.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=4272; línea 33, columna 4245057

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E018364** · 2026-08-08T04:13:20.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=4055; línea 33, columna 4029793

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E018513** · 2026-08-08T20:36:40.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=4008; línea 33, columna 3982952

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E019004** · 2026-08-16T02:46:40.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=3835; línea 33, columna 3811772

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E019024** · 2026-08-16T10:16:40.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
S016 · record_index_1based=3815; línea 33, columna 3791749

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E030474** · 2026-09-08T23:26:45.000000-06:00 · Google Analytics · Has utilizado Coppel: compras en línea
S012 · record_index_1based=290; línea 33, columna 313990

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E030475** · 2026-09-08T23:26:45.000000-06:00 · Publicidad · Has utilizado Coppel: compras en línea
S024 · record_index_1based=245; línea 33, columna 289523

[Abrir fuente web](https://play.google.com/store/apps/details?id=com.coppel.coppelapp)

**E030513** · 2026-09-09T02:36:40.000000-06:00 · Google Play Store · Se ha utilizado Coppel: compras en línea
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

**E084292** · 2026-09-26T22:29:46.000000-06:00 · Búsqueda · perfil negocios google
S004 · record_index_1based=4; línea 33, columna 3190

[Abrir fuente web](https://www.google.com/search?q=perfil+negocios+google)

**E084293** · 2026-09-26T22:29:51.142605-06:00 · Historial de Chrome · Muestra tu empresa en Google: Perfil de Negocio de Google
S028 · record_index_1based=63

[Abrir fuente web](https://business.google.com/es-all/business-profile/)

**E084294** · 2026-09-26T22:30:02.753842-06:00 · Historial de Chrome · Muestra tu empresa en Google: Perfil de Negocio de Google
S028 · record_index_1based=62

[Abrir fuente web](https://business.google.com/es-all/business-profile/)

**E084295** · 2026-09-26T22:30:06.000000-06:00 · Chrome · Haz que tu empresa aparezca en Google
S008 · record_index_1based=18; línea 33, columna 14195

[Abrir fuente web](https://business.google.com/create/new?gmbsrc=all-es-419-z-z-z-gmb-s-z-u~bgcmhp-hom_hr-u&hl=es-419&skipLandingPage=&skipPagesList=1&cbl=hr&cbp=hom&cbt=now&service=ome&original_intent=GMB)

**E084296** · 2026-09-26T22:30:06.453130-06:00 · Historial de Chrome · Haz que tu empresa aparezca en Google
S028 · record_index_1based=61

[Abrir fuente web](https://business.google.com/create/new?gmbsrc=all-es-419-z-z-z-gmb-s-z-u~bgcmhp-hom_hr-u&hl=es-419&skipLandingPage=&skipPagesList=1&cbl=hr&cbp=hom&cbt=now&service=ome&original_intent=GMB)

**E084297** · 2026-09-26T22:30:07.000000-06:00 · Perfil de Empresa en Google · Viste Registro
S022 · record_index_1based=1; línea 33, columna 43

[Abrir fuente web](https://business.google.com/)

**E084298** · 2026-09-26T22:30:12.000000-06:00 · Búsqueda · Muestra tu empresa en Google: Perfil de Negocio de Google
S004 · record_index_1based=3; línea 33, columna 2166

[Abrir fuente web](https://business.google.com/es-all/business-profile/)

**E084299** · 2026-09-26T22:30:12.000000-06:00 · Chrome · Muestra tu empresa en Google: Perfil de Negocio de Google
S008 · record_index_1based=17; línea 33, columna 13496

[Abrir fuente web](https://business.google.com/es-all/business-profile/)

**E084300** · 2026-09-26T22:30:12.887103-06:00 · Historial de Chrome · Muestra tu empresa en Google: Perfil de Negocio de Google
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

Hay 705 relaciones automáticas propuestas en datos/actividad-correlaciones.json. Cada observación tiene ID de esta versión, fecha original, precisión, fuente y localizador de registro. El catálogo permite volver al HTML/JSON/CSV original y comprobar SHA-256. Los originales fueron verificados sin modificaciones.

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

**E047328** · México 2026-09-14T11:00:51.000000-06:00 · UTC 2026-09-14T17:00:51.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 311, "html_line_1based": 34, "html_column_0based": 297861}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E047340** · México 2026-09-14T12:17:55.000000-06:00 · UTC 2026-09-14T18:17:55.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 310, "html_line_1based": 34, "html_column_0based": 296699}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E058023** · México 2026-09-14T20:13:32.000000-06:00 · UTC 2026-09-15T02:13:32.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 307, "html_line_1based": 34, "html_column_0based": 293182}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E058080** · México 2026-09-14T22:12:26.000000-06:00 · UTC 2026-09-15T04:12:26.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 293, "html_line_1based": 34, "html_column_0based": 276638}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E058116** · México 2026-09-14T23:04:27.000000-06:00 · UTC 2026-09-15T05:04:27.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 292, "html_line_1based": 34, "html_column_0based": 275476}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E058459** · México 2026-09-15T01:29:15.000000-06:00 · UTC 2026-09-15T07:29:15.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 290, "html_line_1based": 34, "html_column_0based": 273107}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E058973** · México 2026-09-15T11:18:48.000000-06:00 · UTC 2026-09-15T17:18:48.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 274, "html_line_1based": 34, "html_column_0based": 254324}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E058986** · México 2026-09-15T11:51:34.000000-06:00 · UTC 2026-09-15T17:51:34.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 270, "html_line_1based": 34, "html_column_0based": 249664}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E071360** · México 2026-09-20T16:11:03.000000-06:00 · UTC 2026-09-20T22:11:03.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 177, "html_line_1based": 34, "html_column_0based": 145791}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E072521** · México 2026-09-20T20:47:22.000000-06:00 · UTC 2026-09-21T02:47:22.000000+00:00
Chat · 6850175308
S007 · {"record_index_1based": 1, "html_line_1based": 33, "html_column_0based": 43}

[Abrir enlace](https://mail.google.com/chat/#search/6850175308)

**E072537** · México 2026-09-20T21:12:50.000000-06:00 · UTC 2026-09-21T03:12:50.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 170, "html_line_1based": 34, "html_column_0based": 137950}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E078474** · México 2026-09-25T15:20:10.000000-06:00 · UTC 2026-09-25T21:20:10.000000+00:00
MBOX · Cabeceras Date · Correo · noreply@notice.xiaomi.com · Xiaomi Account password changed
S508 · {"mbox_message_index_1based": 27, "mail_id": "M000027", "message_id": "<1790371210682_112866_1088606_3539.sc-10-2-255-203-inbound0@em1424.notice.xiaomi.com>"}

**E078490** · México 2026-09-25T15:24:48.502037-06:00 · UTC 2026-09-25T21:24:48.502037+00:00
Historial de Chrome · Xiaomi Account
S028 · {"record_index_1based": 146, "json_pointer": "/Browser History/145"}

[Abrir enlace](https://account.xiaomi.com/fe/service/account?cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&userId=6850175308)

**E078491** · México 2026-09-25T15:24:49.124575-06:00 · UTC 2026-09-25T21:24:49.124575+00:00
Historial de Chrome · Xiaomi Account
S028 · {"record_index_1based": 145, "json_pointer": "/Browser History/144"}

[Abrir enlace](https://account.xiaomi.com/fe/service/account?cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&userId=6850175308&_locale=en_US)

**E078495** · México 2026-09-25T15:25:33.256443-06:00 · UTC 2026-09-25T21:25:33.256443+00:00
Historial de Chrome · Xiaomi Account
S028 · {"record_index_1based": 142, "json_pointer": "/Browser History/141"}

[Abrir enlace](https://account.xiaomi.com/auth/jump?target=https%3A%2F%2Faccount.xiaomi.com%2Ffe%2Fservice%2Faccount%2Fprivacy%3FcUserId%3DwAb6f4ntA20ZEJ6WDRaIbXk_M8I%26userId%3D6850175308%26_locale%3Den_US&cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&userId=6850175308)

**E078496** · México 2026-09-25T15:25:33.788076-06:00 · UTC 2026-09-25T21:25:33.788076+00:00
Historial de Chrome · Xiaomi Account
S028 · {"record_index_1based": 141, "json_pointer": "/Browser History/140"}

[Abrir enlace](https://account.xiaomi.com/fe/service/account/privacy?cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&_locale=en_US&userId=6850175308)

**E078497** · México 2026-09-25T15:25:38.000000-06:00 · UTC 2026-09-25T21:25:38.000000+00:00
Chrome · Xiaomi Account
S008 · {"record_index_1based": 53, "html_line_1based": 33, "html_column_0based": 53412}

[Abrir enlace](https://account.xiaomi.com/fe/service/account/privacy/application?cUserId=wAb6f4ntA20ZEJ6WDRaIbXk_M8I&_locale=en_US&userId=6850175308)

**E078498** · México 2026-09-25T15:25:38.671916-06:00 · UTC 2026-09-25T21:25:38.671916+00:00
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

**E072537** · México 2026-09-20T21:12:50.000000-06:00 · UTC 2026-09-21T03:12:50.000000+00:00
Búsqueda · 6850175308
S004 · {"record_index_1based": 170, "html_line_1based": 34, "html_column_0based": 137950}

[Abrir enlace](https://www.google.com/search?q=6850175308)

**E072542** · México 2026-09-20T21:13:29.000000-06:00 · UTC 2026-09-21T03:13:29.000000+00:00
Búsqueda · Pendiente de sol en oro macizo, piercing para labio en oro macizo ...
S004 · {"record_index_1based": 169, "html_line_1based": 34, "html_column_0based": 136819}

[Abrir enlace](https://www.etsy.com/es/listing/4303042674/pendiente-de-sol-en-oro-macizo-piercing)

**E072543** · México 2026-09-20T21:13:36.000000-06:00 · UTC 2026-09-21T03:13:36.000000+00:00
Google Analytics · www.etsy.com/es/listing/4303042674/pendiente-de-sol-en-oro-macizo-piercing
S012 · {"record_index_1based": 137, "html_line_1based": 33, "html_column_0based": 146988}

[Abrir enlace](http://www.etsy.com/es/listing/4303042674/pendiente-de-sol-en-oro-macizo-piercing)

**E072545** · México 2026-09-20T21:18:59.000000-06:00 · UTC 2026-09-21T03:18:59.000000+00:00
Búsqueda · g.co/sc
S004 · {"record_index_1based": 168, "html_line_1based": 34, "html_column_0based": 135664}

[Abrir enlace](https://www.google.com/search?q=g.co%2Fsc)

**E072548** · México 2026-09-20T21:32:10.000000-06:00 · UTC 2026-09-21T03:32:10.000000+00:00
Google Analytics · miperfil.clarin.com/
S012 · {"record_index_1based": 135, "html_line_1based": 33, "html_column_0based": 144822}

[Abrir enlace](http://miperfil.clarin.com/)

**E072549** · México 2026-09-20T21:36:31.000000-06:00 · UTC 2026-09-21T03:36:31.000000+00:00
Búsqueda · clarin
S004 · {"record_index_1based": 167, "html_line_1based": 34, "html_column_0based": 134335}

[Abrir enlace](https://www.google.com/search?q=clarin)

**E072554** · México 2026-09-20T21:40:31.000000-06:00 · UTC 2026-09-21T03:40:31.000000+00:00
Búsqueda · inwebo authenticator
S004 · {"record_index_1based": 164, "html_line_1based": 34, "html_column_0based": 130939}

[Abrir enlace](https://www.google.com/search?q=inwebo+authenticator)

**E072557** · México 2026-09-20T21:42:20.000000-06:00 · UTC 2026-09-21T03:42:20.000000+00:00
Google Analytics · www.hermes.com/mx/es/
S012 · {"record_index_1based": 131, "html_line_1based": 33, "html_column_0based": 140589}

[Abrir enlace](http://www.hermes.com/mx/es/)

**E072558** · México 2026-09-20T21:42:20.000000-06:00 · UTC 2026-09-21T03:42:20.000000+00:00
Google Analytics · www.hermes.com/mx/es/login/
S012 · {"record_index_1based": 132, "html_line_1based": 33, "html_column_0based": 141645}

[Abrir enlace](http://www.hermes.com/mx/es/login/)

**E072564** · México 2026-09-20T21:44:31.000000-06:00 · UTC 2026-09-21T03:44:31.000000+00:00
Traductor de Google · el sitio web traducido https://hermes-agent.nousresearch.com/docs/user-guide/messaging
S026 · {"record_index_1based": 1, "html_line_1based": 33, "html_column_0based": 43}

[Abrir enlace](https://hermes--agent-nousresearch-com.translate.goog/docs/user-guide/messaging?_x_tr_sl=auto&_x_tr_tl=es&_x_tr_hl=es-419&_x_tr_pto=tc)

**E072565** · México 2026-09-20T21:47:08.000000-06:00 · UTC 2026-09-21T03:47:08.000000+00:00
Google Analytics · postlogin.clarin.com/post-login
S012 · {"record_index_1based": 129, "html_line_1based": 33, "html_column_0based": 138369}

[Abrir enlace](http://postlogin.clarin.com/post-login)

**E072570** · México 2026-09-20T21:48:56.266751-06:00 · UTC 2026-09-21T03:48:56.266751+00:00
Google Play Store · Installs · Installs · firstInstallationTime · TrustBuilder Authenticator
S058 · {"json_pointer": "/367/install/firstInstallationTime"}

**E072571** · México 2026-09-20T21:48:56.266751-06:00 · UTC 2026-09-21T03:48:56.266751+00:00
Google Play Store · Installs · Installs · lastUpdateTime · TrustBuilder Authenticator
S058 · {"json_pointer": "/367/install/lastUpdateTime"}

**E072573** · México 2026-09-20T21:49:27.000000-06:00 · UTC 2026-09-21T03:49:27.000000+00:00
Google Play Store · TrustBuilder Authenticator
S016 · {"record_index_1based": 276, "html_line_1based": 33, "html_column_0based": 274049}

[Abrir enlace](https://play.google.com/store/apps/details?id=com.inwebo.near.prod)

**E072610** · México 2026-09-20T22:56:36.000000-06:00 · UTC 2026-09-21T04:56:36.000000+00:00
Google Analytics · www.hermes.com/us/en/account/create/
S012 · {"record_index_1based": 111, "html_line_1based": 33, "html_column_0based": 117884}

[Abrir enlace](http://www.hermes.com/us/en/account/create/)

**E072612** · México 2026-09-20T22:58:55.000000-06:00 · UTC 2026-09-21T04:58:55.000000+00:00
Búsqueda · Hermes Agent — Open-Source AI Agent That Grows With You ...
S004 · {"record_index_1based": 150, "html_line_1based": 34, "html_column_0based": 112759}

[Abrir enlace](https://hermes-agent.nousresearch.com/)

**E072613** · México 2026-09-20T22:59:59.000000-06:00 · UTC 2026-09-21T04:59:59.000000+00:00
Búsqueda · hermes agent
S004 · {"record_index_1based": 149, "html_line_1based": 34, "html_column_0based": 111593}

[Abrir enlace](https://www.google.com/search?q=hermes+agent)

**E072616** · México 2026-09-20T23:01:38.000000-06:00 · UTC 2026-09-21T05:01:38.000000+00:00
Google Analytics · www.hermes.com/us/en/login/
S012 · {"record_index_1based": 108, "html_line_1based": 33, "html_column_0based": 114671}

[Abrir enlace](http://www.hermes.com/us/en/login/)

**E072622** · México 2026-09-20T23:07:02.000000-06:00 · UTC 2026-09-21T05:07:02.000000+00:00
Google Analytics · www.hermes.com/us/en/
S012 · {"record_index_1based": 106, "html_line_1based": 33, "html_column_0based": 112548}

[Abrir enlace](http://www.hermes.com/us/en/)

**E072660** · México 2026-09-20T23:36:40.000000-06:00 · UTC 2026-09-21T05:36:40.000000+00:00
Google Play Store · Se ha utilizado TrustBuilder Authenticator
S016 · {"record_index_1based": 412, "html_line_1based": 33, "html_column_0based": 409776}

[Abrir enlace](https://play.google.com/store/apps/details?id=com.inwebo.near.prod)

**E071361** · México 2026-09-20T16:12:12.000000-06:00 · UTC 2026-09-20T22:12:12.000000+00:00
Google Analytics · portal.nousresearch.com/cloud
S012 · {"record_index_1based": 147, "html_line_1based": 33, "html_column_0based": 157875}

[Abrir enlace](http://portal.nousresearch.com/cloud)

**E071363** · México 2026-09-20T16:13:44.000000-06:00 · UTC 2026-09-20T22:13:44.000000+00:00
Google Analytics · portal.nousresearch.com/orgs/3d6ba8ff/billing
S012 · {"record_index_1based": 146, "html_line_1based": 33, "html_column_0based": 156747}

[Abrir enlace](http://portal.nousresearch.com/orgs/3d6ba8ff/billing)

**E071364** · México 2026-09-20T16:14:57.000000-06:00 · UTC 2026-09-20T22:14:57.000000+00:00
Google Analytics · portal.nousresearch.com/
S012 · {"record_index_1based": 145, "html_line_1based": 33, "html_column_0based": 155682}

[Abrir enlace](http://portal.nousresearch.com/)

**E071371** · México 2026-09-20T16:17:50.000000-06:00 · UTC 2026-09-20T22:17:50.000000+00:00
Google Analytics · portal.nousresearch.com/login
S012 · {"record_index_1based": 144, "html_line_1based": 33, "html_column_0based": 154602}

[Abrir enlace](http://portal.nousresearch.com/login)

**E072580** · México 2026-09-20T21:59:47.000000-06:00 · UTC 2026-09-21T03:59:47.000000+00:00
Google Analytics · portal.nousresearch.com/manage-subscription
S012 · {"record_index_1based": 124, "html_line_1based": 33, "html_column_0based": 132591}

[Abrir enlace](http://portal.nousresearch.com/manage-subscription)

**E072584** · México 2026-09-20T22:05:38.000000-06:00 · UTC 2026-09-21T04:05:38.000000+00:00
Google Analytics · portal.nousresearch.com/orgs/3d6ba8ff/billing
S012 · {"record_index_1based": 123, "html_line_1based": 33, "html_column_0based": 131462}

[Abrir enlace](http://portal.nousresearch.com/orgs/3d6ba8ff/billing)

**E072586** · México 2026-09-20T22:16:28.000000-06:00 · UTC 2026-09-21T04:16:28.000000+00:00
Google Analytics · portal.nousresearch.com/orgs/3d6ba8ff/api-keys
S012 · {"record_index_1based": 122, "html_line_1based": 33, "html_column_0based": 130330}

[Abrir enlace](http://portal.nousresearch.com/orgs/3d6ba8ff/api-keys)

**E072587** · México 2026-09-20T22:16:49.000000-06:00 · UTC 2026-09-21T04:16:49.000000+00:00
Google Analytics · portal.nousresearch.com/cloud
S012 · {"record_index_1based": 121, "html_line_1based": 33, "html_column_0based": 129249}

[Abrir enlace](http://portal.nousresearch.com/cloud)

**E072588** · México 2026-09-20T22:17:02.000000-06:00 · UTC 2026-09-21T04:17:02.000000+00:00
Google Analytics · portal.nousresearch.com/orgs/3d6ba8ff/agents
S012 · {"record_index_1based": 120, "html_line_1based": 33, "html_column_0based": 128123}

[Abrir enlace](http://portal.nousresearch.com/orgs/3d6ba8ff/agents)

**E072614** · México 2026-09-20T23:00:20.000000-06:00 · UTC 2026-09-21T05:00:20.000000+00:00
Google Analytics · portal.nousresearch.com/cloud
S012 · {"record_index_1based": 109, "html_line_1based": 33, "html_column_0based": 115746}

[Abrir enlace](http://portal.nousresearch.com/cloud)

**E072618** · México 2026-09-20T23:02:35.000000-06:00 · UTC 2026-09-21T05:02:35.000000+00:00
Búsqueda · https://portal.nousresearch.com/
S004 · {"record_index_1based": 147, "html_line_1based": 34, "html_column_0based": 108937}

[Abrir enlace](https://portal.nousresearch.com/)

**E072619** · México 2026-09-20T23:03:11.000000-06:00 · UTC 2026-09-21T05:03:11.000000+00:00
Google Analytics · portal.nousresearch.com/
S012 · {"record_index_1based": 107, "html_line_1based": 33, "html_column_0based": 113605}

[Abrir enlace](http://portal.nousresearch.com/)

**E072625** · México 2026-09-20T23:11:40.000000-06:00 · UTC 2026-09-21T05:11:40.000000+00:00
Google Analytics · portal.nousresearch.com/orgs/3d6ba8ff/usage
S012 · {"record_index_1based": 104, "html_line_1based": 33, "html_column_0based": 110353}

[Abrir enlace](http://portal.nousresearch.com/orgs/3d6ba8ff/usage)

La visita a postlogin.clarin.com/post-login y las rutas de Hermès /login/ y /account/create/ son hechos del historial. El historial no guarda los formularios enviados ni una confirmación de inicio de sesión o alta, por lo que no prueba qué credencial se introdujo o si funcionó. Tampoco se demuestra que Etsy haya entregado una credencial para esos sitios.

Hermès de hermes.com es la tienda; Hermes Agent de hermes-agent.nousresearch.com es un proyecto de agente de IA. En el historial aparecen ambos. La documentación de mensajería de Hermes Agent fue visitada traducida a las 21:44:31. Su documentación actual usa autorización por usuarios/plataforma o emparejamiento; no describe que un ID empresarial de Etsy o Clarín dé acceso. [P04]

[Hermes Agent: pasarela de mensajería y autorizaciones](https://hermes-agent.nousresearch.com/docs/user-guide/messaging)

Ninguno de los seis números empresariales/de evento/sufijo enumerados aparece literalmente en los archivos de Google Takeout. Tampoco aparecen en el texto ni enlaces de los mensajes de Messenger. La hipótesis del usuario de identificarse con el mismo dato queda abierta, pendiente de precisar el número y la cuenta; no se convierte en conclusión. La secuencia cronológica se conserva como relación de navegación, no de autenticación.

## Pista adicional para validar con una imagen: inWebo / TrustBuilder

La misma noche hubo búsquedas inwebo authenticator, acceso a myinwebo.com y una primera instalación de TrustBuilder Authenticator a las 21:48:56.266751. El registro de uso de Google Play es de las 23:36:40. Esta es una nueva pista concreta para la consulta anterior sobre validar con una imagen, aunque no se encontró la frase exacta ni un QR de activación personal.

**E071365** · México 2026-09-20T16:15:48.000000-06:00 · UTC 2026-09-20T22:15:48.000000+00:00
Búsqueda · inwebo authenticator
S004 · {"record_index_1based": 176, "html_line_1based": 34, "html_column_0based": 144610}

[Abrir enlace](https://www.google.com/search?q=inwebo+authenticator)

**E071366** · México 2026-09-20T16:16:03.000000-06:00 · UTC 2026-09-20T22:16:03.000000+00:00
Búsqueda · inWebo Authenticator 6 para Android - Descargar
S004 · {"record_index_1based": 175, "html_line_1based": 34, "html_column_0based": 143532}

[Abrir enlace](https://inwebo-authenticator-6.softonic.com/android)

**E071367** · México 2026-09-20T16:16:08.000000-06:00 · UTC 2026-09-20T22:16:08.000000+00:00
Búsqueda · my inwebo authenticator
S004 · {"record_index_1based": 174, "html_line_1based": 34, "html_column_0based": 142345}

[Abrir enlace](https://www.google.com/search?q=my+inwebo+authenticator)

**E071368** · México 2026-09-20T16:16:11.000000-06:00 · UTC 2026-09-20T22:16:11.000000+00:00
Búsqueda · MyinWebo.com
S004 · {"record_index_1based": 173, "html_line_1based": 34, "html_column_0based": 141332}

[Abrir enlace](https://myinwebo.com/)

**E071369** · México 2026-09-20T16:16:37.000000-06:00 · UTC 2026-09-20T22:16:37.000000+00:00
Búsqueda · inwebo admin
S004 · {"record_index_1based": 172, "html_line_1based": 34, "html_column_0based": 140167}

[Abrir enlace](https://www.google.com/search?q=inwebo+admin)

**E071370** · México 2026-09-20T16:17:13.000000-06:00 · UTC 2026-09-20T22:17:13.000000+00:00
Búsqueda · https://www.myinwebo.com/console/logon
S004 · {"record_index_1based": 171, "html_line_1based": 34, "html_column_0based": 139111}

[Abrir enlace](https://www.myinwebo.com/console/logon)

**E072554** · México 2026-09-20T21:40:31.000000-06:00 · UTC 2026-09-21T03:40:31.000000+00:00
Búsqueda · inwebo authenticator
S004 · {"record_index_1based": 164, "html_line_1based": 34, "html_column_0based": 130939}

[Abrir enlace](https://www.google.com/search?q=inwebo+authenticator)

**E072555** · México 2026-09-20T21:40:35.000000-06:00 · UTC 2026-09-21T03:40:35.000000+00:00
Búsqueda · https://www.myinwebo.com/
S004 · {"record_index_1based": 163, "html_line_1based": 34, "html_column_0based": 129909}

[Abrir enlace](https://www.myinwebo.com/)

**E072570** · México 2026-09-20T21:48:56.266751-06:00 · UTC 2026-09-21T03:48:56.266751+00:00
Google Play Store · Installs · Installs · firstInstallationTime · TrustBuilder Authenticator
S058 · {"json_pointer": "/367/install/firstInstallationTime"}

**E072571** · México 2026-09-20T21:48:56.266751-06:00 · UTC 2026-09-21T03:48:56.266751+00:00
Google Play Store · Installs · Installs · lastUpdateTime · TrustBuilder Authenticator
S058 · {"json_pointer": "/367/install/lastUpdateTime"}

**E072573** · México 2026-09-20T21:49:27.000000-06:00 · UTC 2026-09-21T03:49:27.000000+00:00
Google Play Store · TrustBuilder Authenticator
S016 · {"record_index_1based": 276, "html_line_1based": 33, "html_column_0based": 274049}

[Abrir enlace](https://play.google.com/store/apps/details?id=com.inwebo.near.prod)

**E072660** · México 2026-09-20T23:36:40.000000-06:00 · UTC 2026-09-21T05:36:40.000000+00:00
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

Solicitud: conservar las páginas locales de los datos, preparar GitHub y una carta personal. Cuenta indicada por el usuario: spinky-afk. La declaración del usuario no equivale a una conclusión del análisis.

Se prepara un sitio privado local con cronología, catálogo de fuentes actualizado, copias originales y vistas derivadas sin navegación externa. El usuario confirmó la cuenta spinky-afk. GitHub CLI quedó autorizado para spinky-afk. El estado remoto verificado se conserva en estado-publicacion.json.

GitHub Pages no se habilita automáticamente: la privacidad del repositorio no garantiza la privacidad de Pages. Referencia local G02 en referencias.html. Consulta del 1 de octubre de 2026.

Cuatro archivos contienen la clave VAPID; se conservan mediante respaldo cifrado y permanecen intactos en sus ubicaciones locales. El usuario autorizó posteriormente subir todos los originales y datos privados. La carpeta evidencia conserva íntegros los originales, las claves recuperadas y todo research; las vistas de lectura del sitio son derivados. La carta se guarda como testimonio solicitado, sin verificación de las acusaciones.

Actualización preparada: 2026-10-01T19:28:15.123900+00:00. Las próximas actualizaciones requieren ejecutar el constructor; no hay una tarea automática ni vigilancia permanente.
<!-- FIN_RESULTADOS_SESION_5 -->


<!-- INICIO_RESULTADOS_SESION_6 -->
## Sesión 6: pistas del 20/21 y dispositivos

## Noche del 20 y día 21: mensajes, juegos, respaldos y dispositivos

Revisión de 2889 observaciones del 20-09-2026 18:00 al 22-09-2026 00:00, hora de Ciudad de México. Se incorporaron 173 fechas de configuración Android, juegos y registros de sincronización de Chrome antes omitidas; la cronología completa tiene 84,642 observaciones y 508 fuentes. Los IDs E se reasignaron al ordenar esta versión; las referencias duraderas son ruta, localizador y SHA-256. La versión anterior permanece en el historial Git local.

## El respaldo que sí aparece antes de esa noche

El 20 de septiembre a las 14:02:14 hubo una pregunta de Gemini en Workspace: «Backup en enlace». La respuesta de Gemini cita Cloud Backup and Restore en Drive, ID 1iO7scCcYFZiCkEFrMaqHI2BwIAIxEy9L. Es una respuesta y referencia exportada; la exportación no incluye el contenido de la carpeta. Queda fuera del intervalo nocturno y se conserva como contexto previo.

**E071336** · México 2026-09-20T14:02:14.333391-06:00 · UTC 2026-09-20T20:02:14.333391+00:00
Gemini en Workspace · conversation_1789934534 · conversation_1789934534 · turn_last_modified · Backup en enlace
S083 · {"json_pointer": "/conversation_turns/0/user_turn/turn_last_modified"}

**E071337** · México 2026-09-20T14:02:14.333391-06:00 · UTC 2026-09-20T20:02:14.333391+00:00
Gemini en Workspace · conversation_1789934534 · conversation_1789934534 · turn_last_modified · Puedes acceder a la carpeta de copia de seguridad a través del siguiente enlace: [Cloud Backup and Restore](https://drive.google.com/open?id=1iO7scCcYFZiCkEFrMaqHI2BwIAIxEy9L%29.  
  
¿Te gustaría que busque algún archivo específico en tus fuentes?
S083 · {"json_pointer": "/conversation_turns/1/system_turn/turn_last_modified"}

Corrección de alcance de las consultas externas: el usuario indicó que se debe consultar hadilene116@gmail.com. La comprobación posterior google_drive_get_profile identifica la conexión actual como velez@deeplogic.com.mx. Las consultas previas no verificaron la identidad en el momento de lectura; se conservan separadas y no establecen el estado del Drive de hadilene116@gmail.com ni la propiedad de los archivos. Se suspenden nuevas lecturas de archivos en esa conexión hasta autorizar la cuenta solicitada. La contraseña aportada no se transcribe al registro, al sitio ni al PDF.

Dentro de esas consultas de alcance no atribuible a la cuenta solicitada, los metadatos devuelven la carpeta Cloud Backup and Restore, creada el 20-09-2026 13:01:59.315 UTC y modificada el 27-09-2026 00:29:43.649 UTC; el listado devuelve cero archivos hijos visibles. Las tres referencias Lark Player respondieron 404. Ninguno de estos resultados permite afirmar que falten o se hayan borrado archivos de hadilene116@gmail.com, reconstruir contenido anterior o atribuir cambios a una persona.

[Verificación local de la cuenta conectada y corrección de alcance](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/drive-identidad-consultada.json)

El Takeout local sí incluye hadilene116@gmail.com en Perfil/Perfil.json y Cuenta de Google/hadilene116.SubscriberInfo.html. Estos archivos identifican el conjunto exportado y permiten continuar su análisis local. La exportación y el conector de Drive se mantienen como fuentes distintas; esta identificación no determina quién realizó cada acción.

[Perfil conservado del Takeout](file:///home/deep-logic/Documentos/Registro/Takeout/Perfil/Perfil.json)

[Información del suscriptor conservada del Takeout](file:///home/deep-logic/Documentos/Registro/Takeout/Cuenta%20de%20Google/hadilene116.SubscriberInfo.html)

[Comprobación de procedencia del Takeout local](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/cuenta-takeout-local.json)

[Resultado local de consulta de metadatos Drive](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/drive-respaldos-consulta-reintento.json)

[Listado local de la carpeta de respaldo](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/drive-cloud-backup-listado.json)

## Mensajes y el perfil de negocios que se recuerda

**E072461** · México 2026-09-20T19:19:57.000000-06:00 · UTC 2026-09-21T01:19:57.000000+00:00
Ayuda de Google · Has chateado con Ayuda de Google
S003 · {"record_index_1based": 3, "html_line_1based": 33, "html_column_0based": 2387}

Hay una acción de chat con Ayuda de Google el 20 a las 19:19:57. El registro no contiene el texto de la conversación ni una empresa destinataria. A las 20:47:22 aparece una búsqueda del número 6850175308 en Google Chat; una búsqueda no establece que se haya enviado un mensaje.

**E072521** · México 2026-09-20T20:47:22.000000-06:00 · UTC 2026-09-21T02:47:22.000000+00:00
Chat · 6850175308
S007 · {"record_index_1based": 1, "html_line_1based": 33, "html_column_0based": 43}

En las conversaciones exportadas solo se recuperaron dos observaciones de Messenger en esta ventana: ambas del 21 a las 14:03:05. SOY MASON figura como remitente y se comparte una publicación sobre una biblioteca masónica en los chats SOY MASON y UN ETERNO APRENDIZ. No se halló en esta ventana un mensaje saliente verificable a un perfil empresarial. La ausencia en esta copia no demuestra que nunca se enviara.

**E075330** · México 2026-09-21T14:03:05.000000-06:00 · UTC 2026-09-21T20:03:05.000000+00:00
Messenger · SOY MASON · SOY MASON: SOY MASON envió un archivo adjunto.
Encuentra nuestra BIBLIOTECA Masónica dentro de nuestra Página de Facebook o en el primer comentario... Siempre trabajando a favor del estudio constante...
S.F.U.
https://www.facebook.com/story.php?story_fbid=pfbid0CdtKxNkKRfhcygRRcFnyr2Grw1gTobzmSbAs2KUnAS4QEsAcViEMjSyS9BRProgdl&id=61553075107468&post_id=61553075107468_pfbid0CdtKxNkKRfhcygRRcFnyr2Grw1gTobzmSbAs2KUnAS4QEsAcViEMjSyS9BRProgdl
478547315650144
478547315650144
478547315650144
478547315650144
478547315650144
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
S447 · {"message_index_1based": 7, "html_line_1based": 36, "html_column_0based": 3914}

**E075331** · México 2026-09-21T14:03:05.000000-06:00 · UTC 2026-09-21T20:03:05.000000+00:00
Messenger · UN ETERNO APRENDIZ · SOY MASON: SOY MASON envió un archivo adjunto.
Encuentra nuestra BIBLIOTECA Masónica dentro de nuestra Página de Facebook o en el primer comentario... Siempre trabajando a favor del estudio constante...
S.F.U.
https://www.facebook.com/story.php?story_fbid=pfbid0CdtKxNkKRfhcygRRcFnyr2Grw1gTobzmSbAs2KUnAS4QEsAcViEMjSyS9BRProgdl&id=61553075107468&post_id=61553075107468_pfbid0CdtKxNkKRfhcygRRcFnyr2Grw1gTobzmSbAs2KUnAS4QEsAcViEMjSyS9BRProgdl
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1635855486666999
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
1678524932434102
S449 · {"message_index_1based": 7, "html_line_1based": 36, "html_column_0based": 2888}

El enlace del adjunto contiene el ID 61553075107468. El cuerpo también repite 478547315650144, 1635855486666999 y 1678524932434102. Esos valores se hallaron únicamente en las dos conversaciones dentro de los HTML revisados; no coinciden con los IDs de empresas ya catalogados ni con las fuentes de juegos. No se les asigna una función de autenticación, empresa o ataque.

## Los dos o tres juegos: dos listas diferentes

El perfil de Juegos de Google Play es privado, con ID FamousSmile6745 y creación el 21 a las 05:17:55. La sección de último juego contiene Words of Wonders: Crucigrama. La copia del producto contiene un juego y dos archivos guardados de ese juego: ALF.FugoID y com.fugo.wow.cloudData. Son dos recursos guardados, no dos juegos distintos.

[Perfil original de Juegos de Google Play](file:///home/deep-logic/Documentos/Registro/Takeout/Servicios%20de%20juego%20de%20Google%20Play/Global/Player.html)

[Resumen original de sesión de juego](file:///home/deep-logic/Documentos/Registro/Takeout/Servicios%20de%20juego%20de%20Google%20Play/Global/Playtime.html)

Playtime indica comienzo 05:17:44, fin 05:18:05, duración declarada de 10 segundos y Number of Sessions=0. Se preservan esos valores tal como están; el intervalo entre extremos es 21 segundos, por lo que no se reemplaza la duración declarada por una duración calculada. Los metadatos guardados tienen modificación 05:18:02 y 05:18:04.

**E072759** · México 2026-09-21T05:17:44.000000-06:00 · UTC 2026-09-21T11:17:44.000000+00:00
Servicios de juego de Google Play · Playtime · Daily Playtime · First Session Start · com.fugo.wow
S489 · {"table_index_1based": 2, "row_index_1based": 2, "column": "First Session Start", "html_line_1based": 1, "html_column_0based": 620}

**E072760** · México 2026-09-21T05:17:55.000000-06:00 · UTC 2026-09-21T11:17:55.000000+00:00
Servicios de juego de Google Play · Player · Información general del reproductor · Player profile was created on · Player profile was created on
S488 · {"table_index_1based": 1, "row_index_1based": 6, "column": "Player profile was created on", "html_line_1based": 1, "html_column_0based": 688}

**E072761** · México 2026-09-21T05:17:57.000000-06:00 · UTC 2026-09-21T11:17:57.000000+00:00
Servicios de juego de Google Play · Player · Último juego que se jugó · Jugado por última vez · Words of Wonders: Crucigrama
S488 · {"table_index_1based": 2, "row_index_1based": 2, "column": "Jugado por última vez", "html_line_1based": 1, "html_column_0based": 903}

**E072762** · México 2026-09-21T05:17:57.000000-06:00 · UTC 2026-09-21T11:17:57.000000+00:00
Servicios de juego de Google Play · Actividad ·  · Time First Played · Time First Played
S491 · {"table_index_1based": 1, "row_index_1based": 2, "column": "Time First Played", "html_line_1based": 1, "html_column_0based": 356}

**E072763** · México 2026-09-21T05:17:57.000000-06:00 · UTC 2026-09-21T11:17:57.000000+00:00
Servicios de juego de Google Play · Actividad ·  · Time Last Played · Time Last Played
S491 · {"table_index_1based": 1, "row_index_1based": 3, "column": "Time Last Played", "html_line_1based": 1, "html_column_0based": 420}

**E072764** · México 2026-09-21T05:18:02.000000-06:00 · UTC 2026-09-21T11:18:02.000000+00:00
Servicios de juego de Google Play · Metadatos ·  · Última modificación: · Última modificación:
S493 · {"table_index_1based": 1, "row_index_1based": 4, "column": "Última modificación:", "html_line_1based": 1, "html_column_0based": 450}

**E072767** · México 2026-09-21T05:18:04.000000-06:00 · UTC 2026-09-21T11:18:04.000000+00:00
Servicios de juego de Google Play · Metadatos ·  · Última modificación: · Última modificación:
S494 · {"table_index_1based": 1, "row_index_1based": 4, "column": "Última modificación:", "html_line_1based": 1, "html_column_0based": 462}

**E072768** · México 2026-09-21T05:18:05.000000-06:00 · UTC 2026-09-21T11:18:05.000000+00:00
Servicios de juego de Google Play · Playtime · Daily Playtime · Last Session End · com.fugo.wow
S489 · {"table_index_1based": 2, "row_index_1based": 2, "column": "Last Session End", "html_line_1based": 1, "html_column_0based": 620}

En Facebook, Tus puntuaciones más recientes en juegos instantáneos contiene exactamente tres nombres: Chess Club, Club de Pool: Billar 8 bolas y 8 Ball Pool. El catálogo distinto Juegos instantáneos contiene nueve nombres. Las fechas que aparecen en estas secciones son principalmente de octubre de 2025 y junio de 2026; no se recuperó una sesión de esos tres juegos del 20/21 de septiembre.

[Las tres puntuaciones de juegos en Facebook](file:///home/deep-logic/Documentos/facebook/your_facebook_activity/facebook_gaming/your_latest_instant_game_scores.html)

[Catálogo completo de juegos instantáneos](file:///home/deep-logic/Documentos/facebook/your_facebook_activity/facebook_gaming/instant_games.html)

## Respaldos, restauración y coincidencias de hora

El 20 a las 23:15:33 se buscó com.google.android.apps.restore. El 21 a las 04:14:28 se visitó una referencia de Drive titulada tweakradje - Restore apps (Android Switch); a las 04:29 y 06:01 hubo más consultas sobre restauración, y a las 06:16 búsquedas tweaking restore/tweaking restore android. Son consultas y visitas, sin el contenido del archivo de Drive ni una prueba de ejecución.

**E072630** · México 2026-09-20T23:15:33.000000-06:00 · UTC 2026-09-21T05:15:33.000000+00:00
Búsqueda · com.google.android.apps.restore
S004 · {"record_index_1based": 142, "html_line_1based": 34, "html_column_0based": 103377}

**E072713** · México 2026-09-21T04:14:28.000000-06:00 · UTC 2026-09-21T10:14:28.000000+00:00
Búsqueda · tweakradje - Restore apps (Android Switch) - Google Drive: Sign-in
S004 · {"record_index_1based": 141, "html_line_1based": 34, "html_column_0based": 102321}

**E072729** · México 2026-09-21T04:29:51.000000-06:00 · UTC 2026-09-21T10:29:51.000000+00:00
Búsqueda · com.google.android.apps.restore
S004 · {"record_index_1based": 140, "html_line_1based": 34, "html_column_0based": 101118}

**E072730** · México 2026-09-21T04:29:52.000000-06:00 · UTC 2026-09-21T10:29:52.000000+00:00
Ayuda · Back up or restore data on your Android device - Android Help
S002 · {"record_index_1based": 258, "html_line_1based": 33, "html_column_0based": 343767}

**E072774** · México 2026-09-21T06:01:24.000000-06:00 · UTC 2026-09-21T12:01:24.000000+00:00
Búsqueda · com.google.android.apps.restore
S004 · {"record_index_1based": 139, "html_line_1based": 34, "html_column_0based": 99915}

**E072775** · México 2026-09-21T06:01:25.000000-06:00 · UTC 2026-09-21T12:01:25.000000+00:00
Ayuda · Back up or restore data on your Android device - Android Help
S002 · {"record_index_1based": 257, "html_line_1based": 33, "html_column_0based": 342747}

**E072780** · México 2026-09-21T06:16:36.000000-06:00 · UTC 2026-09-21T12:16:36.000000+00:00
Búsqueda · tweaking restore
S004 · {"record_index_1based": 138, "html_line_1based": 34, "html_column_0based": 98742}

**E072781** · México 2026-09-21T06:16:46.000000-06:00 · UTC 2026-09-21T12:16:46.000000+00:00
Búsqueda · tweaking restore android
S004 · {"record_index_1based": 137, "html_line_1based": 34, "html_column_0based": 97553}

A 2026-09-20T23:36:40.000000-06:00 hay 66 observaciones de uso de apps con la misma marca temporal. Aparecen componentes de Xiaomi/Google, apps personales y juegos. Esa coincidencia no identifica una automatización ni prueba que una persona abriera todas las apps exactamente a la vez.

A 2026-09-21T07:56:40.000000-06:00 hay 45 observaciones de uso de apps con la misma marca temporal. Aparecen componentes de Xiaomi/Google, apps personales y juegos. Esa coincidencia no identifica una automatización ni prueba que una persona abriera todas las apps exactamente a la vez.

**E072652** · México 2026-09-20T23:36:40.000000-06:00 · UTC 2026-09-21T05:36:40.000000+00:00
Google Play Store · Se ha utilizado com.miui.backup
S016 · {"record_index_1based": 404, "html_line_1based": 33, "html_column_0based": 401810}

**E072679** · México 2026-09-20T23:36:40.000000-06:00 · UTC 2026-09-21T05:36:40.000000+00:00
Google Play Store · Se ha utilizado Android Switch
S016 · {"record_index_1based": 511, "html_line_1based": 33, "html_column_0based": 509474}

**E072713** · México 2026-09-21T04:14:28.000000-06:00 · UTC 2026-09-21T10:14:28.000000+00:00
Búsqueda · tweakradje - Restore apps (Android Switch) - Google Drive: Sign-in
S004 · {"record_index_1based": 141, "html_line_1based": 34, "html_column_0based": 102321}

**E072792** · México 2026-09-21T06:35:14.706367-06:00 · UTC 2026-09-21T12:35:14.706367+00:00
Google Play Store · Installs · Installs · lastUpdateTime · Android Switch
S058 · {"json_pointer": "/136/install/lastUpdateTime"}

**E072899** · México 2026-09-21T07:56:40.000000-06:00 · UTC 2026-09-21T13:56:40.000000+00:00
Google Play Store · Se ha utilizado com.miui.cloudbackup
S016 · {"record_index_1based": 213, "html_line_1based": 33, "html_column_0based": 211208}

**E072900** · México 2026-09-21T07:56:40.000000-06:00 · UTC 2026-09-21T13:56:40.000000+00:00
Google Play Store · Se ha utilizado com.miui.backup
S016 · {"record_index_1based": 214, "html_line_1based": 33, "html_column_0based": 212135}

**E072916** · México 2026-09-21T07:56:40.000000-06:00 · UTC 2026-09-21T13:56:40.000000+00:00
Google Play Store · Se ha utilizado Android Switch
S016 · {"record_index_1based": 230, "html_line_1based": 33, "html_column_0based": 228105}

Google documenta respaldos automáticos y recuperación de apps/datos al configurar la cuenta [N02]. En los archivos revisados no hay un registro de error de restablecimiento ni una cadena técnica que atribuya el problema a un juego. El campo Device Booted señala un arranque; no prueba un restablecimiento de fábrica.

Words of Wonders, Android Switch y Xiaomi Home comparten la marca lastUpdateTime 2026-09-21T12:35:14.706367Z (06:35:14.706367 México) en Installs.json, entradas 53, 136 y 466. Es una coincidencia concreta del inventario de instalaciones, sin probar una relación causal ni identificar un programa que inicie restauraciones.

[Inventario original de instalaciones, entradas 53, 136 y 466](file:///home/deep-logic/Documentos/Registro/Takeout/Google%C2%A0Play%C2%A0Store/Installs.json)

El inventario también registra AirDroid Parental Control, entrada 433, con firstInstallationTime 26-09-2026 23:55:17.240431 UTC (17:55:17.240431 México), modelo 23129RA5FL. Es posterior al intervalo recordado. El título de la app y su instalación no demuestran quién la instaló, sus permisos activos ni que bloqueara un restablecimiento.

## Cinco IDs de Android con el mismo hardware registrado

Los IDs 3644671859603123984, 3778158131092576330, 3975241346881164962, 4247182940332696163 y 4511226476644240739 coinciden en modelo 23129RA5FL, IMEI primario terminado en 0505 y número de serie. El IMEI completo y la serie quedan en el anexo privado. Esta coincidencia agrupa registros de hardware; no acredita cinco teléfonos ni clonación.

S483 · ID 3644671859603123984 · registro: 26 sept 2026, 5:42:46 a.m. UTC · última conexión: 27 sept 2026, 4:18:19 a.m. UTC · motivo: Account Changed

[Configuración original Android 3644671859603123984](file:///home/deep-logic/Documentos/Registro/Takeout/Servicio%20de%20configuraci%C3%B3n%20de%20dispositivos%20Android/Device-3644671859603123984.html)

S484 · ID 3778158131092576330 · registro: 11 sept 2026, 5:03:08 p.m. UTC · última conexión: 11 sept 2026, 5:04:08 p.m. UTC · motivo: Account Changed

[Configuración original Android 3778158131092576330](file:///home/deep-logic/Documentos/Registro/Takeout/Servicio%20de%20configuraci%C3%B3n%20de%20dispositivos%20Android/Device-3778158131092576330.html)

S485 · ID 3975241346881164962 · registro: 12 sept 2026, 3:20:34 p.m. UTC · última conexión: 21 sept 2026, 8:00:06 p.m. UTC · motivo: Device Booted

[Configuración original Android 3975241346881164962](file:///home/deep-logic/Documentos/Registro/Takeout/Servicio%20de%20configuraci%C3%B3n%20de%20dispositivos%20Android/Device-3975241346881164962.html)

S486 · ID 4247182940332696163 · registro: 23 sept 2026, 6:38:57 p.m. UTC · última conexión: 26 sept 2026, 4:06:35 a.m. UTC · motivo: Internal Trigger

[Configuración original Android 4247182940332696163](file:///home/deep-logic/Documentos/Registro/Takeout/Servicio%20de%20configuraci%C3%B3n%20de%20dispositivos%20Android/Device-4247182940332696163.html)

S487 · ID 4511226476644240739 · registro: 11 ene 2025, 8:45:54 p.m. UTC · última conexión: 12 sept 2026, 12:45:45 p.m. UTC · motivo: Unknown

[Configuración original Android 4511226476644240739](file:///home/deep-logic/Documentos/Registro/Takeout/Servicio%20de%20configuraci%C3%B3n%20de%20dispositivos%20Android/Device-4511226476644240739.html)

El registro 3975241346881164962 tiene conexiones correctas el 21 a las 05:14:17 y 14:00:06; el último motivo es Device Booted. El CSV de acceso contiene registros de actividad Android, Linux, Windows e iPhone. Sus tiempos son actividad/última comunicación, no se presentan como inicios de sesión exitosos de otras personas. Google explica que un dispositivo puede tener varias sesiones y actividad de sincronización en segundo plano [N03].

**E072756** · México 2026-09-21T05:14:17.000000-06:00 · UTC 2026-09-21T11:14:17.000000+00:00
Configuración de dispositivos Android · Conexión de configuración Android · 3975241346881164962 · Conexiones recientes con el servicio de configuración de dispositivos Android que se establecieron correctamente:
S485 · {"table_index_1based": 3, "row_index_1based": 30, "column": "Hora de conexión", "html_line_1based": 701, "html_column_0based": 5}

**E075327** · México 2026-09-21T14:00:06.000000-06:00 · UTC 2026-09-21T20:00:06.000000+00:00
Configuración de dispositivos Android · Conexión de configuración Android · 3975241346881164962 · Conexiones recientes con el servicio de configuración de dispositivos Android que se establecieron correctamente:
S485 · {"table_index_1based": 3, "row_index_1based": 31, "column": "Hora de conexión", "html_line_1based": 709, "html_column_0based": 5}

**E075328** · México 2026-09-21T14:00:06.000000-06:00 · UTC 2026-09-21T20:00:06.000000+00:00
Configuración de dispositivos Android · Hora de la última conexión de datos · Android 3975241346881164962 · modelo 23129RA5FL
S485 · {"field": "Hora de la última conexión de datos", "html_line_1based": 462, "html_column_0based": 67}

## Google Home, la app de consejos HomeKit y Apple pendiente

Los ocho JSON del producto App de Home contienen {} o una lista con un objeto vacío. Automations.json, ApplicationPermissions.json y HomeApp.json no aportan reglas, permisos ni miembros recuperables. No se puede reconstruir automatización doméstica de esta copia.

[Original Google Home: ApplicationPermissions.json](file:///home/deep-logic/Documentos/Registro/Takeout/App%20de%20Home/ApplicationPermissions.json)

[Original Google Home: Automations.json](file:///home/deep-logic/Documentos/Registro/Takeout/App%20de%20Home/Automations.json)

[Original Google Home: GoogleNestConnect.json](file:///home/deep-logic/Documentos/Registro/Takeout/App%20de%20Home/GoogleNestConnect.json)

[Original Google Home: GoogleNestPartnerConnections.json](file:///home/deep-logic/Documentos/Registro/Takeout/App%20de%20Home/GoogleNestPartnerConnections.json)

[Original Google Home: HomeApp.json](file:///home/deep-logic/Documentos/Registro/Takeout/App%20de%20Home/HomeApp.json)

[Original Google Home: HomeHistory.json](file:///home/deep-logic/Documentos/Registro/Takeout/App%20de%20Home/HomeHistory.json)

[Original Google Home: SecurityAlarmClips.json](file:///home/deep-logic/Documentos/Registro/Takeout/App%20de%20Home/SecurityAlarmClips.json)

[Original Google Home: SoundSensing.json](file:///home/deep-logic/Documentos/Registro/Takeout/App%20de%20Home/SoundSensing.json)

El 21 a las 06:35 se buscaron apple home/apple homekit en Play. A las 06:36:04.337999 se registró la instalación de HomeKit App for Android Hints para el modelo 23129RA5FL, paquete com.snailhd.inara.app. La ficha actual del desarrollador describe una guía educativa independiente sin afiliación con Apple [N01]. Encontrar esta app no acredita la app Home oficial, acceso a una casa de Apple ni infección.

**E072844** · México 2026-09-21T06:35:15.000000-06:00 · UTC 2026-09-21T12:35:15.000000+00:00
Google Play Store · apple home
S016 · {"record_index_1based": 257, "html_line_1based": 33, "html_column_0based": 255010}

**E072845** · México 2026-09-21T06:35:19.000000-06:00 · UTC 2026-09-21T12:35:19.000000+00:00
Google Play Store · apple home
S016 · {"record_index_1based": 255, "html_line_1based": 33, "html_column_0based": 253041}

**E072847** · México 2026-09-21T06:35:34.000000-06:00 · UTC 2026-09-21T12:35:34.000000+00:00
Google Play Store · apple homekit
S016 · {"record_index_1based": 254, "html_line_1based": 33, "html_column_0based": 252046}

**E072848** · México 2026-09-21T06:35:35.000000-06:00 · UTC 2026-09-21T12:35:35.000000+00:00
Google Play Store · apple homekit
S016 · {"record_index_1based": 253, "html_line_1based": 33, "html_column_0based": 251049}

**E072849** · México 2026-09-21T06:35:40.000000-06:00 · UTC 2026-09-21T12:35:40.000000+00:00
Google Play Store · HomeKit App for Android Hints
S016 · {"record_index_1based": 252, "html_line_1based": 33, "html_column_0based": 250030}

**E072850** · México 2026-09-21T06:36:04.337999-06:00 · UTC 2026-09-21T12:36:04.337999+00:00
Google Play Store · Installs · Installs · firstInstallationTime · HomeKit App for Android Hints
S058 · {"json_pointer": "/434/install/firstInstallationTime"}

**E072851** · México 2026-09-21T06:36:08.000000-06:00 · UTC 2026-09-21T12:36:08.000000+00:00
Publicidad · Se ha utilizado HomeKit App for Android Hints
S024 · {"record_index_1based": 100, "html_line_1based": 33, "html_column_0based": 109741}

**E072852** · México 2026-09-21T06:36:30.000000-06:00 · UTC 2026-09-21T12:36:30.000000+00:00
Google Play Store · HomeKit App for Android Hints
S016 · {"record_index_1based": 251, "html_line_1based": 33, "html_column_0based": 249011}

**E072873** · México 2026-09-21T07:03:55.209503-06:00 · UTC 2026-09-21T13:03:55.209503+00:00
Google Play Store · Installs · Installs · lastUpdateTime · HomeKit App for Android Hints
S058 · {"json_pointer": "/434/install/lastUpdateTime"}

**E072893** · México 2026-09-21T07:56:40.000000-06:00 · UTC 2026-09-21T13:56:40.000000+00:00
Google Play Store · Se ha utilizado HomeKit App for Android Hints
S016 · {"record_index_1based": 207, "html_line_1based": 33, "html_column_0based": 205443}

**E074147** · México 2026-09-21T13:02:48.000000-06:00 · UTC 2026-09-21T19:02:48.000000+00:00
Publicidad · Se ha utilizado HomeKit App for Android Hints
S024 · {"record_index_1based": 88, "html_line_1based": 33, "html_column_0based": 96792}

Apple se deja pendiente porque el usuario indica que por ahora no puede consultar sus datos. En esta fase no se ha accedido a Apple Home ni realizado cambios en sus dispositivos. Las visitas a iCloud recuperadas son actividad web, no un historial de comandos de Home.

## Qué sigue sin resolverse

No se ha identificado el juego recordado con certeza, un evento de chat que cause cambios en dispositivos, un mensaje empresarial saliente del intervalo, la causa del problema de restablecimiento ni una ejecución de automatizaciones de Home. Las exportaciones no incluyen imágenes de disco, APK inspeccionados o el texto íntegro de Gmail/Google Chat. Se conservan pistas y límites en los anexos, sin convertir coincidencias en una atribución de ataque.

[N01 · Ficha del desarrollador: HomeKit App for Android Hints](https://play.google.com/store/apps/details?id=com.snailhd.inara.app)

[N02 · Google: respaldo y restauración de Android](https://support.google.com/android/answer/2819582?hl=es-419)

[N03 · Google: dispositivos y sesiones de cuenta](https://support.google.com/accounts/answer/3067630?hl=es-419)

[N04 · Google: restablecimiento de fábrica Android](https://support.google.com/android/answer/6088915?hl=es-419)

[N05 · Apple: app Home oficial](https://www.apple.com/home-app/)

<!-- FIN_RESULTADOS_SESION_6 -->


<!-- INICIO_RESULTADOS_SESION_7 -->
## Sesión 7: cuenta conectada y conversaciones separadas

El usuario corrigió la cuenta solicitada a hadilene116@gmail.com. Se comprobó únicamente el perfil del conector: velez@deeplogic.com.mx. No se hicieron más lecturas de archivos con esa conexión. Las consultas previas se conservan fuera de las conclusiones sobre la cuenta solicitada. La comprobación se guarda en [identidad del conector](datos/drive-identidad-consultada.json); el perfil del Takeout local incluye hadilene116@gmail.com, según [procedencia local](datos/cuenta-takeout-local.json). La contraseña no se transcribe ni se usa para autenticar el conector.

Para la pregunta sobre otra sesión se aplicó la habilidad OpenAI Docs. Consulta oficial: las conversaciones conservan su historial individual y pueden trabajar con archivos compartidos del mismo proyecto. Véase [ficha O01 y consulta](datos/sesiones-fuentes-web.json). No hay una tarea automática de investigación permanente.
<!-- FIN_RESULTADOS_SESION_7 -->


<!-- INICIO_RESULTADOS_SESION_8 -->
## Sesión 8: Uber y cruces de Analytics

## Uber Rider y Eats: cruces de Analytics, Facebook y soporte

Aclaración posterior del usuario, 01-10-2026: «no no lo clonaron simplemente no entendia». El usuario aclara que no hubo clonación de la cuenta Uber y que su consulta reflejaba que no entendía los datos. Se mantiene el mensaje histórico a soporte como parte del historial, acompañado de esta aclaración actual. El propósito de estos cruces es entender los registros y su funcionamiento.

[Aclaración del usuario conservada localmente](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/uber-aclaracion-usuario.json)

Se incorporan 12 archivos de la carpeta /home/deep-logic/Documentos/Uber Data Request 5A426B63, situada junto a Facebook en Documentos. Los 696 archivos originales de Facebook no cambiaron respecto al inventario anterior. La nueva cronología reúne 84,642 observaciones fechadas y 508 fuentes; las referencias E pertenecen a esta edición. Los originales de Uber se preservan con SHA-256 y vistas locales.

user_profile-0.csv y driver_profile-0.csv contienen hadilene116@gmail.com. El perfil de usuario indica User Type=Partner; el de conductor indica Driver Profile=UberEats, Is Partner=Yes y Lifetime Completed Trips=0. Es lo que declara la exportación; no acredita entregas realizadas, quién creó el perfil o una relación criminal. Las fechas Signup Date no tienen zona y no se colocan como instantes confirmados.

[Perfil original Account and Profile/user_profile-0.csv](file:///home/deep-logic/Documentos/Uber%20Data%20Request%205A426B63/Uber%20Data/Account%20and%20Profile/user_profile-0.csv)

[Perfil original Account and Profile/driver_profile-0.csv](file:///home/deep-logic/Documentos/Uber%20Data%20Request%205A426B63/Uber%20Data/Account%20and%20Profile/driver_profile-0.csv)

## Los dos Analytics de Uber y el producto Google Analytics

Uber Rider: 10,833 filas, de 2026-08-29T22:07:08.956000-06:00 a 2026-09-18T20:56:24.228000-06:00, hora México. Tipos literales: {"custom": 6075, "impression": 4322, "lifecycle": 87, "tap": 346, "": 3}. El modelo normalizado es 23129ra5fl con Android 15. La exportación no incluye nombres específicos de acciones para CUSTOM, ni destinatarios de mensajes en estos Analytics.

[Analytics original Rider](file:///home/deep-logic/Documentos/Uber%20Data%20Request%205A426B63/Uber%20Data/Rider/rider_app_analytics-0.csv)

Uber Eats: 45,178 filas, de 2026-08-29T03:53:23.184000-06:00 a 2026-09-27T17:35:30.739000-06:00, hora México. Tipos literales: {"custom": 26434, "tap": 1168, "lifecycle": 415, "impression": 17161}. El modelo normalizado es 23129ra5fl con Android 15. La exportación no incluye nombres específicos de acciones para CUSTOM, ni destinatarios de mensajes en estos Analytics.

[Analytics original Eats](file:///home/deep-logic/Documentos/Uber%20Data%20Request%205A426B63/Uber%20Data/Eats/eats_app_analytics-0.csv)

Mi actividad de Google contiene 866 observaciones del producto Google Analytics; 14 mencionan uso de Uber Eats y una visita a un sitio de Uber. Estos registros no son un informe de una propiedad de Analytics administrada por el usuario. Se cruzan con el CSV de Uber por producto y hora, conservando ambos registros y su precisión. Los eventos Uber se presentan de forma compacta en el PDF; los dispositivos y campos completos están en el visor y en cada fila original.

## Coincidencias de Google Analytics y Uber Eats

Las 14 observaciones de uso de Uber Eats en Google Analytics tienen filas del mismo producto en una ventana de ±60 segundos. Se muestra la fila más próxima; el conteo de candidatos de la ventana queda en el JSON. La cercanía no identifica un evento único: puede haber cientos de filas en dos minutos y no hay un ID común exportado.

Cruce E025218 ↔ E025217: diferencia Uber menos Google = -0.056 segundos; 304 filas candidatas en ±60 s.

**E025218** · 2026-09-03T15:18:18.000000-06:00 · UTC 2026-09-03T21:18:18.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 331, "html_line_1based": 33, "html_column_0based": 359230}

**E025217** · 2026-09-03T15:18:17.944000-06:00 · UTC 2026-09-03T21:18:17.944000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 15526, "csv_line_1based": 15527, "csv_end_line_1based": 15527}

Cruce E028756 ↔ E028758: diferencia Uber menos Google = +0.172 segundos; 59 filas candidatas en ±60 s.

**E028756** · 2026-09-05T12:38:38.000000-06:00 · UTC 2026-09-05T18:38:38.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 322, "html_line_1based": 33, "html_column_0based": 349361}

**E028758** · 2026-09-05T12:38:38.172000-06:00 · UTC 2026-09-05T18:38:38.172000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 3242, "csv_line_1based": 3243, "csv_end_line_1based": 3243}

Cruce E046683 ↔ E046684: diferencia Uber menos Google = +0.013 segundos; 8 filas candidatas en ±60 s.

**E046683** · 2026-09-13T17:35:30.000000-06:00 · UTC 2026-09-13T23:35:30.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 258, "html_line_1based": 33, "html_column_0based": 279275}

**E046684** · 2026-09-13T17:35:30.013000-06:00 · UTC 2026-09-13T23:35:30.013000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 44974, "csv_line_1based": 44975, "csv_end_line_1based": 44975}

Cruce E046743 ↔ E046744: diferencia Uber menos Google = +0.270 segundos; 16 filas candidatas en ±60 s.

**E046743** · 2026-09-13T20:20:50.000000-06:00 · UTC 2026-09-14T02:20:50.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 252, "html_line_1based": 33, "html_column_0based": 272727}

**E046744** · 2026-09-13T20:20:50.270000-06:00 · UTC 2026-09-14T02:20:50.270000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 27802, "csv_line_1based": 27803, "csv_end_line_1based": 27803}

Cruce E047055 ↔ E047056: diferencia Uber menos Google = +0.150 segundos; 263 filas candidatas en ±60 s.

**E047055** · 2026-09-13T21:55:51.000000-06:00 · UTC 2026-09-14T03:55:51.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 248, "html_line_1based": 33, "html_column_0based": 268405}

**E047056** · 2026-09-13T21:55:51.150000-06:00 · UTC 2026-09-14T03:55:51.150000+00:00 · Eats · Analytics
Uber Eats · lifecycle · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 17453, "csv_line_1based": 17454, "csv_end_line_1based": 17454}

Cruce E047920 ↔ E047921: diferencia Uber menos Google = +0.069 segundos; 634 filas candidatas en ±60 s.

**E047920** · 2026-09-14T13:35:39.000000-06:00 · UTC 2026-09-14T19:35:39.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 224, "html_line_1based": 33, "html_column_0based": 242274}

**E047921** · 2026-09-14T13:35:39.069000-06:00 · UTC 2026-09-14T19:35:39.069000+00:00 · Eats · Analytics
Uber Eats · lifecycle · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 18241, "csv_line_1based": 18242, "csv_end_line_1based": 18242}

Cruce E049897 ↔ E049898: diferencia Uber menos Google = +0.522 segundos; 42 filas candidatas en ±60 s.

**E049897** · 2026-09-14T14:39:16.000000-06:00 · UTC 2026-09-14T20:39:16.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 221, "html_line_1based": 33, "html_column_0based": 239055}

**E049898** · 2026-09-14T14:39:16.522000-06:00 · UTC 2026-09-14T20:39:16.522000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 20212, "csv_line_1based": 20213, "csv_end_line_1based": 20213}

Cruce E050814 ↔ E050813: diferencia Uber menos Google = -0.084 segundos; 245 filas candidatas en ±60 s.

**E050814** · 2026-09-14T15:10:58.000000-06:00 · UTC 2026-09-14T21:10:58.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 220, "html_line_1based": 33, "html_column_0based": 237974}

**E050813** · 2026-09-14T15:10:57.916000-06:00 · UTC 2026-09-14T21:10:57.916000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 21123, "csv_line_1based": 21124, "csv_end_line_1based": 21124}

Cruce E071503 ↔ E071505: diferencia Uber menos Google = +1.141 segundos; 892 filas candidatas en ±60 s.

**E071503** · 2026-09-20T16:48:56.000000-06:00 · UTC 2026-09-20T22:48:56.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 143, "html_line_1based": 33, "html_column_0based": 153521}

**E071505** · 2026-09-20T16:48:57.141000-06:00 · UTC 2026-09-20T22:48:57.141000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 14507, "csv_line_1based": 14508, "csv_end_line_1based": 14508}

Cruce E073799 ↔ E073801: diferencia Uber menos Google = +0.193 segundos; 445 filas candidatas en ±60 s.

**E073799** · 2026-09-21T12:49:03.000000-06:00 · UTC 2026-09-21T18:49:03.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 81, "html_line_1based": 33, "html_column_0based": 85586}

**E073801** · 2026-09-21T12:49:03.193000-06:00 · UTC 2026-09-21T18:49:03.193000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 10698, "csv_line_1based": 10699, "csv_end_line_1based": 10699}

Cruce E076641 ↔ E076643: diferencia Uber menos Google = +0.121 segundos; 67 filas candidatas en ±60 s.

**E076641** · 2026-09-24T18:02:20.000000-06:00 · UTC 2026-09-25T00:02:20.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 73, "html_line_1based": 33, "html_column_0based": 76731}

**E076643** · 2026-09-24T18:02:20.121000-06:00 · UTC 2026-09-25T00:02:20.121000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 12922, "csv_line_1based": 12923, "csv_end_line_1based": 12923}

Cruce E077341 ↔ E077340: diferencia Uber menos Google = -0.053 segundos; 261 filas candidatas en ±60 s.

**E077341** · 2026-09-25T09:12:00.000000-06:00 · UTC 2026-09-25T15:12:00.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 61, "html_line_1based": 33, "html_column_0based": 64037}

**E077340** · 2026-09-25T09:11:59.947000-06:00 · UTC 2026-09-25T15:11:59.947000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 13345, "csv_line_1based": 13346, "csv_end_line_1based": 13346}

Cruce E077999 ↔ E078001: diferencia Uber menos Google = +0.006 segundos; 289 filas candidatas en ±60 s.

**E077999** · 2026-09-25T11:47:53.000000-06:00 · UTC 2026-09-25T17:47:53.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 60, "html_line_1based": 33, "html_column_0based": 62955}

**E078001** · 2026-09-25T11:47:53.006000-06:00 · UTC 2026-09-25T17:47:53.006000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 12541, "csv_line_1based": 12542, "csv_end_line_1based": 12542}

Cruce E083887 ↔ E083889: diferencia Uber menos Google = +0.045 segundos; 73 filas candidatas en ±60 s.

**E083887** · 2026-09-26T15:14:44.000000-06:00 · UTC 2026-09-26T21:14:44.000000+00:00 · Google Analytics
Has utilizado Uber Eats: Food and Grocery - Apps on Google Play
S012 · /home/deep-logic/Documentos/Registro/Takeout/Mi actividad/Google Analytics/MiActividad.html · {"record_index_1based": 16, "html_line_1based": 33, "html_column_0based": 16133}

**E083889** · 2026-09-26T15:14:44.045000-06:00 · UTC 2026-09-26T21:14:44.045000+00:00 · Eats · Analytics
Uber Eats · impression · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 39835, "csv_line_1based": 39836, "csv_end_line_1based": 39836}

## Facebook: tres identidades diferentes y dos horas coincidentes

ubereats.com · ID de encabezado 1862931440390914 · Identificador dentro de eventos 920222691346894 · S275

Uber Eats: Food and Grocery · ID de encabezado 1109643685726224 · Identificador dentro de eventos 403591763184357 · S276

Uber - Request a ride · ID de encabezado 723297837696301 · Identificador dentro de eventos 277064115737714 · S277

Estos seis valores de Facebook no aparecen literalmente en los 12 archivos de Uber. El identificador dentro de eventos se repite en distintos eventos de cada servicio; no se interpreta como número único de cada acción o credencial. El CSV de Analytics no aporta un identificador que permita equipararlos. El sufijo numérico del archivo de Facebook se mantiene separado.

Hay 4 candidatos temporales Facebook↔Uber, que representan dos horas de Eats repetidas en las vistas resumen/detalle. El 02-09 a las 12:39 Facebook registra ACTIVATE_APP y la fila Uber más próxima es CUSTOM a las 12:38:59.950 (−0,050 s). A las 13:23 Facebook registra CUSTOM y la fila Uber más próxima es IMPRESSION a las 13:23:25.202 (+25,202 s). Los tipos no se equiparan. Las horas Facebook son de actividad recibida, no un reloj confirmado del clic en Uber.

**E023833** · 2026-09-02T12:39:00.000000-06:00 · UTC 2026-09-02T18:39:00.000000+00:00 · Actividad fuera de Meta
Uber Eats: Food and Grocery · ACTIVATE_APP · identificador de evento 403591763184357
S121 · /home/deep-logic/Documentos/facebook/apps_and_websites_off_of_facebook/your_activity_off_meta_technologies/2.html · {"table_index_1based": 5, "html_line_1based": 16, "html_column_0based": 2573}

**E023832** · 2026-09-02T12:38:59.950000-06:00 · UTC 2026-09-02T18:38:59.950000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 8829, "csv_line_1based": 8830, "csv_end_line_1based": 8830}

**E023834** · 2026-09-02T12:39:00.000000-06:00 · UTC 2026-09-02T18:39:00.000000+00:00 · Actividad fuera de Meta
Uber Eats: Food and Grocery · ACTIVATE_APP · identificador de evento 403591763184357
S276 · /home/deep-logic/Documentos/facebook/apps_and_websites_off_of_facebook/your_activity_off_meta_technologies/ubereatsfoodandgrocery_105529809654844411.html · {"table_index_1based": 6, "html_line_1based": 13, "html_column_0based": 3104}

**E023832** · 2026-09-02T12:38:59.950000-06:00 · UTC 2026-09-02T18:38:59.950000+00:00 · Eats · Analytics
Uber Eats · custom · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 8829, "csv_line_1based": 8830, "csv_end_line_1based": 8830}

**E024632** · 2026-09-02T13:23:00.000000-06:00 · UTC 2026-09-02T19:23:00.000000+00:00 · Actividad fuera de Meta
Uber Eats: Food and Grocery · CUSTOM · identificador de evento 403591763184357
S121 · /home/deep-logic/Documentos/facebook/apps_and_websites_off_of_facebook/your_activity_off_meta_technologies/2.html · {"table_index_1based": 3, "html_line_1based": 16, "html_column_0based": 1839}

**E024638** · 2026-09-02T13:23:25.202000-06:00 · UTC 2026-09-02T19:23:25.202000+00:00 · Eats · Analytics
Uber Eats · impression · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 9681, "csv_line_1based": 9682, "csv_end_line_1based": 9682}

**E024634** · 2026-09-02T13:23:00.000000-06:00 · UTC 2026-09-02T19:23:00.000000+00:00 · Actividad fuera de Meta
Uber Eats: Food and Grocery · CUSTOM · identificador de evento 403591763184357
S276 · /home/deep-logic/Documentos/facebook/apps_and_websites_off_of_facebook/your_activity_off_meta_technologies/ubereatsfoodandgrocery_105529809654844411.html · {"table_index_1based": 4, "html_line_1based": 13, "html_column_0based": 2175}

**E024638** · 2026-09-02T13:23:25.202000-06:00 · UTC 2026-09-02T19:23:25.202000+00:00 · Eats · Analytics
Uber Eats · impression · 23129ra5fl / android 15
S502 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/eats_app_analytics-0.csv · {"csv_record_index_1based": 9681, "csv_line_1based": 9682, "csv_end_line_1based": 9682}

El mismo 02-09 a las 13:23 hay CUSTOM para Uber Rider en Facebook, pero no se recuperaron filas Rider próximas a esa hora. El pedido Little Caesars tiene Request_Time_Local=12:39:45 y Final_Delivery_Time_Local=13:23:22. Estas horas son compatibles con el grupo de Eats bajo la interpretación de zona Local, no una prueba de que un evento concreto represente esa entrega.

## La noche del 20 y el día 21

Del 20-09 18:00 al 22-09 00:00 México hay 2,060 filas Eats y 0 Rider. El último registro Rider exportado es 2026-09-18T20:56:24.228000-06:00; su ausencia en esa noche no demuestra que la app no se utilizara. El 20 a las 16:48:56 hay uso Eats en Google y la fila Uber más próxima está a +1,141 s, antes del intervalo nocturno.

El 21 a las 12:49:03 Google Analytics registra uso Eats; Uber tiene CUSTOM a las 12:49:03.193. El pedido Little Caesars figura solicitado a las 12:50:08 y entregado a las 13:50:14, según sus columnas Local. Es una secuencia relacionada por producto y tiempos compatibles; la zona de pedidos sigue marcada como hipótesis por el sufijo Z contradictorio. No identifica una automatización Home, un ataque o un mensaje Facebook saliente.

**E073990** · 2026-09-21T12:50:08.000000-06:00 · UTC 2026-09-21T18:50:08.000000+00:00 · Eats · Pedidos
Uber Eats · completed · Little Caesars (Tulancingo) · Italian Cheese Bread · Request_Time_Local
S503 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/user_orders-0.csv · {"csv_record_index_1based": 5, "csv_line_1based": 6, "csv_end_line_1based": 6, "csv_field": "Request_Time_Local"}

**E073991** · 2026-09-21T12:50:08.000000-06:00 · UTC 2026-09-21T18:50:08.000000+00:00 · Eats · Pedidos
Uber Eats · completed · Little Caesars (Tulancingo) · Pepperoni · Request_Time_Local
S503 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/user_orders-0.csv · {"csv_record_index_1based": 6, "csv_line_1based": 7, "csv_end_line_1based": 7, "csv_field": "Request_Time_Local"}

**E075307** · 2026-09-21T13:50:14.000000-06:00 · UTC 2026-09-21T19:50:14.000000+00:00 · Eats · Pedidos
Uber Eats · completed · Little Caesars (Tulancingo) · Italian Cheese Bread · Final_Delivery_Time_Local
S503 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/user_orders-0.csv · {"csv_record_index_1based": 5, "csv_line_1based": 6, "csv_end_line_1based": 6, "csv_field": "Final_Delivery_Time_Local"}

**E075308** · 2026-09-21T13:50:14.000000-06:00 · UTC 2026-09-21T19:50:14.000000+00:00 · Eats · Pedidos
Uber Eats · completed · Little Caesars (Tulancingo) · Pepperoni · Final_Delivery_Time_Local
S503 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Eats/user_orders-0.csv · {"csv_record_index_1based": 6, "csv_line_1based": 7, "csv_end_line_1based": 7, "csv_field": "Final_Delivery_Time_Local"}

## 18 de septiembre: consulta histórica a soporte y respuesta de Uber

A las 05:50:32 México figura Deleted At en un método VISA/Banco Azteca. A las 06:10:32 hay un registro Creator=User que afirma «Creo que mi cuenta fue clonada y me llegan solicitudes de acceso». A las 06:42:14 Creator=Uber responde que restableció la contraseña como medida de seguridad. Se documentan la eliminación registrada, el reporte y la respuesta, sin concluir quién eliminó el método, que se confirmara clonación o que ese episodio sea el del 20/21.

La sospecha escrita entonces no describe la explicación actual del usuario: posteriormente aclaró que no hubo clonación y que simplemente no entendía lo observado. La respuesta de soporte sobre restablecer la contraseña se conserva como respuesta, sin convertirla en confirmación de aquella sospecha.

**E062145** · 2026-09-18T05:50:32.000000-06:00 · UTC 2026-09-18T11:50:32.000000+00:00 · Métodos de pago
Uber · método de pago · BANK_CARD · VISA · BANCO AZTECA S.A. INSTITUCION DE BANCA MULTIPLE
S499 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Account and Profile/payment_methods-0.csv · {"csv_record_index_1based": 6, "csv_line_1based": 7, "csv_end_line_1based": 7}

**E062880** · 2026-09-18T06:10:32.000000-06:00 · UTC 2026-09-18T12:10:32.000000+00:00 · Soporte
Uber · Creator=User · Uso la app Uber para conducir o hacer entregas  : false      I use Uber as a User  : false      Uso Uber Freight  : false      Otro  : false      Quiero una copia de mis datos  : true      Quiero corregir mis datos  : false      Quiero recurrir una decisión sobre una solicitud sobre privacidad anterior  : false      Tengo otras preguntas sobre mis datos  : false      Quiero contactar con el responsable de la protección de datos de Uber  : false      (Obligatorio) Proporciona más detalles sobre el motivo por el que contactas con el equipo de Uber.  : Creo que mi cuenta fue clonada y me llegan solicitudes de acceso
S497 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Account and Profile/customer_support_tickets-0.csv · {"csv_record_index_1based": 8, "csv_line_1based": 9, "csv_end_line_1based": 9}

**E062904** · 2026-09-18T06:42:14.000000-06:00 · UTC 2026-09-18T12:42:14.000000+00:00 · Soporte
Uber · Creator=Uber · Traducido por IA            Hola, Eduardo‍.    Gracias por ponerte en contacto sobre este tema. Sé que puede ser preocupante, permíteme ayudarte.    A veces recibirás un código de verificación destinado a proteger tu cuenta. Sin embargo, si no actualizaste la información de tu cuenta ni intentaste iniciar sesión desde un dispositivo nuevo antes de recibir el código de verificación, no introduzcas el código en la app.    Como medida de seguridad, la contraseña de tu cuenta se ha restablecido. Para acceder de nuevo a tu cuenta,   deberás crear una contraseña nueva y única  . Con la nueva contraseña, podrás seguir usando tu cuenta de forma segura. Te recomendamos comprobar que tus credenciales de acceso sean únicas en diferentes sitios web.    También puedes considerar activar la verificación en dos pasos. Para ello, sigue estos pasos: * Pulsa en   Cuenta   * Pulsa en   Gestionar cuenta de Uber   * Pulsa en   Seguridad   o en “  Iniciar revisión  ” para completar la revisión de tu cuenta.    Si tienes problemas para restablecer tu contraseña, no dudes en contactarnos.
S497 · /home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data/Account and Profile/customer_support_tickets-0.csv · {"csv_record_index_1based": 9, "csv_line_1based": 10, "csv_end_line_1based": 10}

## Dispositivos e IP: relaciones y límites

Rider · Device ID d0666f2c-f032-3cff-a5b2-bcdddd9a4c40 · 6,796 filas · UTC original 2026-08-30 04:07:08.956 → 2026-09-12 14:52:44.483 · modelo 23129ra5fl. Los Device ID de Rider cubren periodos distintos con el mismo modelo; no se equiparan a IMEI, Android ID o número de serie.

Rider · Device ID ac1f0639-322f-3c6d-94f2-a187112cafa1 · 4,037 filas · UTC original 2026-09-18 11:01:26.817 → 2026-09-19 02:56:24.228 · modelo 23129RA5FL, 23129ra5fl. Los Device ID de Rider cubren periodos distintos con el mismo modelo; no se equiparan a IMEI, Android ID o número de serie.

Eats · Device ID [no exportado] · 45,178 filas · UTC original 2026-08-29 09:53:23.184 → 2026-09-27 23:35:30.739 · modelo 23129ra5fl. Los Device ID de Rider cubren periodos distintos con el mismo modelo; no se equiparan a IMEI, Android ID o número de serie.

El modelo coincide, sin distinguir mayúsculas, con las configuraciones Android del Takeout y los agentes de Facebook antes revisados. Rider no exporta IMEI/serie y Eats no exporta Device ID; este puente compara modelo/SO y no acredita una identidad física única. Las coincidencias literales de IP se guardan con referencias y prefijos en el JSON; relacionan una red, no una persona ni autoría de acciones.

GPS Time muestra 1970-01-01 en 170 filas Rider y 1847 Eats. Es una marca que se conserva como auxiliar; no se usa para afirmar actividad en 1970 ni para inventar una posición. La cronología de Analytics usa Event Time (UTC).

## Pedidos, viajes y mensajes sin zona

user_orders contiene 23 filas de artículos, agrupables en 15 combinaciones de solicitud/restaurante; no se presentan como 23 pedidos diferentes. Rider tiene dos viajes: uno rider_canceled y otro completed. Se usan sus campos UTC explícitos. Los seis registros communications_sent tienen Time sin zona y dos medios repetidos, intercom_text/push; se preservan íntegros entre los anexos sin zona confirmada y no se tratan como seis conversaciones distintas.

Los nombres Local de los pedidos contradicen su sufijo Z. Se interpretó el reloj como México y se marcó la hipótesis en cada entrada, apoyándose en los pares local/UTC de Rider (seis horas) y la hora del pedido KFC del texto de soporte. Esta interpretación debe revisarse si Uber proporciona el diccionario de datos. Los perfiles y comunicaciones sin zona no reciben una hora inventada. El readme exportado solo muestra Loading; no aporta ese diccionario en contenido estático.

[Fuente original Eats/user_orders-0.csv](file:///home/deep-logic/Documentos/Uber%20Data%20Request%205A426B63/Uber%20Data/Eats/user_orders-0.csv)

[Fuente original Rider/rider_lifetime_trips-0.csv](file:///home/deep-logic/Documentos/Uber%20Data%20Request%205A426B63/Uber%20Data/Rider/rider_lifetime_trips-0.csv)

[Fuente original Account and Profile/communications_sent-0.csv](file:///home/deep-logic/Documentos/Uber%20Data%20Request%205A426B63/Uber%20Data/Account%20and%20Profile/communications_sent-0.csv)

[Fuente original Account and Profile/payment_methods-0.csv](file:///home/deep-logic/Documentos/Uber%20Data%20Request%205A426B63/Uber%20Data/Account%20and%20Profile/payment_methods-0.csv)

[Paquete local de cruces, filas, estadísticas y límites](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/uber-analytics-cruces.json)

<!-- FIN_RESULTADOS_SESION_8 -->


<!-- INICIO_RESULTADOS_SESION_9 -->
## Sesión 9: correo y uso de apps

## Correo local: aplicaciones, Etsy, Hermes, Clarín y Google Play

Se incorporan 1,527 mensajes del MBOX de Documentos, original de 104,855,969 bytes y SHA-256 a2c0b40d481a02e6829c9aba9f61d7874c1da23bf3e3d8bca83e1474d58f674d. El corpus tiene principalmente hadilene116@gmail.com en sus cabeceras de destinatario. Se conserva cada correo y sus adjuntos en el original íntegro; las páginas locales facilitan la lectura. La cronología añade Date declarado con su zona: no confunde envío con lectura o apertura de una aplicación. Los remitentes no se han validado criptográficamente.

La subida completa autorizada por el usuario conserva los archivos originales y todos los datos privados del conjunto investigado en el repositorio privado. Las vistas de lectura facilitan consulta local; el original permanece disponible íntegro. Se mantiene la aclaración del usuario de que no hubo clonación de Uber y que simplemente no entendía los registros.

[MBOX original completo](file:///home/deep-logic/Documentos/Todo%20el%20correo%2C%20con%20Spam%20y%20Papelera%20incluidos.mbox)

## La pista de validar con una imagen: rostro o huella en Play

Dos correos de Google Play, del 12-09 a las 10:28:53 y del 26-09 a las 00:59:28 México, dicen que se actualizó la verificación de compras en Redmi 23129RA5FL para usar rostro o huella. Esta es una candidata concreta para la pista de validar con una imagen más rápido; no demuestra que sea la búsqueda recordada ni una validación mediante Google Lens. El propio correo delimita la configuración a esa cuenta y ese dispositivo.

**E041180** · 2026-09-12T10:28:53.000000-06:00 · UTC 2026-09-12T16:28:53.000000+00:00 · MBOX · Cabeceras Date
Correo · googleplay-noreply@google.com · Cambios en la configuración de verificación de compras de Google Play
S508 · {"mbox_message_index_1based": 305, "mail_id": "M000305", "message_id": "<4ed01a67f8f54e6fcaa92c1bc2f713185bf39d91-20300789-111457209@google.com>"}

[Leer correo local M000305](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000305.html)

**E078831** · 2026-09-26T00:59:28.000000-06:00 · UTC 2026-09-26T06:59:28.000000+00:00 · MBOX · Cabeceras Date
Correo · googleplay-noreply@google.com · Cambios en la configuración de verificación de compras de Google Play
S508 · {"mbox_message_index_1based": 11, "mail_id": "M000011", "message_id": "<3aeba3e251113bb420a4ab8285373425b8897838-20300789-111457209@google.com>"}

[Leer correo local M000011](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000011.html)

## Etsy el 20 por la noche: Google y correo de Etsy

El 20-09 a las 21:50:33 México aparecen dos correos: Google indica que se usó Acceder con Google para Etsy y que se compartieron nombre/foto de perfil y dirección de correo; Etsy pregunta por una sesión Chrome 135 / Android 15 y menciona Pachuca como ubicación en su aviso. La ubicación es la descrita por el correo, sin identificar a una persona. Se relaciona con las visitas Etsy y el PAGE_VIEW recibido por Meta esa noche, sin equiparar los IDs empresariales de Meta a una credencial de acceso.

**E072577** · 2026-09-20T21:50:33.000000-06:00 · UTC 2026-09-21T03:50:33.000000+00:00 · MBOX · Cabeceras Date
Correo · noreply-accounts@google.com · Compartiste algunos datos de tu Cuenta de Google con Etsy
S508 · {"mbox_message_index_1based": 285, "mail_id": "M000285", "message_id": "<3959ae36de87eb9b76087455be3e54cf3c3d572a-20376977-337030291@google.com>"}

[Leer correo local M000285](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000285.html)

**E072576** · 2026-09-20T21:50:33.000000-06:00 · UTC 2026-09-21T03:50:33.000000+00:00 · MBOX · Cabeceras Date
Correo · noreply@mail.etsy.com · Adilene, ¿iniciaste sesión hace poco en Etsy?
S508 · {"mbox_message_index_1based": 202, "mail_id": "M000202", "message_id": "<20260921035032.7AE577E140@web-red-fpxm.localdomain>"}

[Leer correo local M000202](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000202.html)

**E072574** · 2026-09-20T21:50:00.000000-06:00 · UTC 2026-09-21T03:50:00.000000+00:00 · Actividad fuera de Meta
etsy.com · PAGE_VIEW · identificador de evento 114623403312281
S109 · {"table_index_1based": 1, "html_line_1based": 16, "html_column_0based": 1075}

**E072575** · 2026-09-20T21:50:00.000000-06:00 · UTC 2026-09-21T03:50:00.000000+00:00 · Actividad fuera de Meta
etsy.com · PAGE_VIEW · identificador de evento 114623403312281
S229 · {"table_index_1based": 2, "html_line_1based": 13, "html_column_0based": 1179}

**E072578** · 2026-09-20T21:51:59.000000-06:00 · UTC 2026-09-21T03:51:59.000000+00:00 · Google Analytics
www.etsy.com/es/r/similar/4303042674
S012 · {"record_index_1based": 126, "html_line_1based": 33, "html_column_0based": 134928}

**E072579** · 2026-09-20T21:52:43.000000-06:00 · UTC 2026-09-21T03:52:43.000000+00:00 · Google Analytics
www.etsy.com/es/listing/4303042674/pendiente-de-sol-en-oro-macizo-piercing
S012 · {"record_index_1based": 125, "html_line_1based": 33, "html_column_0based": 133713}

## Hermes y Clarín: dos servicios y momentos distintos

Hermes.com envió dos correos para finalizar creación de cuenta, a las 22:56:33 y 23:00:47 del 20-09. Son de ecommerce.hermes.com, la tienda, y piden confirmar el correo con un código; el texto dice que, si se ignora, no se crea la cuenta. No se presentan como confirmación de una cuenta terminada ni como Hermes Agent. Clarín envía una bienvenida el 21-09 a las 15:00:17 y agradece el registro. No hay en estos mensajes una cadena que convierta el número 6850175308 o un ID de Meta en mecanismo de identificación compartido entre los tres servicios.

**E072609** · 2026-09-20T22:56:33.000000-06:00 · UTC 2026-09-21T04:56:33.000000+00:00 · MBOX · Cabeceras Date
Correo · customer-service@ecommerce.hermes.com · Hermes.com - Your security code to finalize your account creation
S508 · {"mbox_message_index_1based": 226, "mail_id": "M000226", "message_id": "<202609210456.13786924000@smtp-relay.mailin.fr>"}

[Leer correo local M000226](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000226.html)

**E072615** · 2026-09-20T23:00:47.000000-06:00 · UTC 2026-09-21T05:00:47.000000+00:00 · MBOX · Cabeceras Date
Correo · customer-service@ecommerce.hermes.com · Hermes.com - Your security code to finalize your account creation
S508 · {"mbox_message_index_1based": 225, "mail_id": "M000225", "message_id": "<202609210500.71955169878@smtp-relay.mailin.fr>"}

[Leer correo local M000225](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000225.html)

**E075333** · 2026-09-21T15:00:17.000000-06:00 · UTC 2026-09-21T21:00:17.000000+00:00 · MBOX · Cabeceras Date
Correo · info@noticias.clarin.com · ¡Te damos la bienvenida aClarín, con una invitación exclusiva! 👋
S508 · {"mbox_message_index_1based": 138, "mail_id": "M000138", "message_id": "<29b466315a52477880d8c02a9bf95f8b@1741127422>"}

[Leer correo local M000138](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000138.html)

## Google Play y Analytics: qué uso de apps está registrado

En el intervalo 20-09 18:00 → 22-09 00:00 México se recuperan 138 observaciones de uso de apps en Google Play/Google Analytics, además de 87 registros de instalación o actualización separados. Se guardan todos los usos en el CSV y se agrupan por marca temporal. Un registro Se ha utilizado/Has utilizado documenta el uso registrado por ese producto; no acredita por sí solo que una persona abriera manualmente la app en primer plano.

[Usos de apps del 20/21 en CSV](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/correo-play-20-21.csv)

2026-09-20T23:36:40.000000-06:00 · 66 observaciones: Se ha utilizado Shortcut Maker; Se ha utilizado Banco Azteca; Se ha utilizado Banco Azteca; Se ha utilizado TikTok; Se ha utilizado ShareMe: File sharing; Se ha utilizado Mi Calendar; Se ha utilizado WhatsApp Messenger; Se ha utilizado Uber Eats: Food and Grocery; Se ha utilizado StarMaker: Canta Karaoke; Se ha utilizado Spotify: app música y podcasts; Se ha utilizado Snapchat: Conecta con Amigos; Se ha utilizado ChatGPT; Se ha utilizado com.miui.thirdappassistant; Se ha utilizado Security; Se ha utilizado com.miui.notification; Se ha utilizado com.miui.home; Se ha utilizado com.miui.home; Se ha utilizado com.miui.cloudservice; Se ha utilizado Cleaner; Se ha utilizado com.miui.backup; Se ha utilizado Bóveda de aplicaciones; Se ha utilizado Navegador Mi - Rápido y seguro; Se ha utilizado Xiaomi Community; Se ha utilizado File Manager by Xiaomi; Se ha utilizado Información del dispositivo; Se ha utilizado com.lbe.security.miui; Se ha utilizado Administrador de aplicaciones; Se ha utilizado TrustBuilder Authenticator; Se ha utilizado Instagram; Se ha utilizado Speech Recognition & Synthesis; Se ha utilizado Android Auto; Se ha utilizado com.google.android.photopicker; Se ha utilizado Permissions Controller; Se ha utilizado Gboard: el Teclado de Google; Se ha utilizado Google; Se ha utilizado Gmail; Se ha utilizado Gmail; Se ha utilizado DocumentsUI; Se ha utilizado Teléfono de Google; Se ha utilizado Contactos; Se ha utilizado Calendario de Google; Se ha utilizado Android System Intelligence; Se ha utilizado YouTube Music; Se ha utilizado Bienestar digital; Se ha utilizado Google One; Se ha utilizado Seguridad personal; Se ha utilizado Android Switch; Se ha utilizado Google Fotos; Se ha utilizado Files de Google; Se ha utilizado Mensajes de Google; Se ha utilizado Google Chat; Se ha utilizado Google Drive; Se ha utilizado Google Home; Se ha utilizado Meta AI; Se ha utilizado Messenger; Se ha utilizado Facebook; Se ha utilizado BBVA México; Se ha utilizado com.android.updater; Se ha utilizado com.android.traceur; Se ha utilizado com.android.server.telecom; Se ha utilizado com.android.providers.downloads.ui; Se ha utilizado com.android.intentresolver; Se ha utilizado Shortcut Maker; Se ha utilizado Google Chrome; Se ha utilizado Google; Se ha utilizado WPS Office: PDF, Word, Excel. La hora compartida no implica aperturas simultáneas.

2026-09-21T07:56:40.000000-06:00 · 45 observaciones: Se ha utilizado Shortcut Maker; Se ha utilizado Banco Azteca; Se ha utilizado Xiaomi Home; Se ha utilizado ShareMe: File sharing; Se ha utilizado Mi Calendar; Se ha utilizado HomeKit App for Android Hints; Se ha utilizado ChatGPT; Se ha utilizado com.miui.securitycore; Se ha utilizado Security; Se ha utilizado com.miui.home; Se ha utilizado com.miui.cloudservice; Se ha utilizado com.miui.cloudbackup; Se ha utilizado com.miui.backup; Se ha utilizado Bóveda de aplicaciones; Se ha utilizado Navegador Mi - Rápido y seguro; Se ha utilizado Xiaomi Community; Se ha utilizado File Manager by Xiaomi; Se ha utilizado Información del dispositivo; Se ha utilizado Administrador de aplicaciones; Se ha utilizado Android Auto; Se ha utilizado com.google.android.photopicker; Se ha utilizado Permissions Controller; Se ha utilizado com.google.android.packageinstaller; Se ha utilizado Google; Se ha utilizado Gmail; Se ha utilizado DocumentsUI; Se ha utilizado Teléfono de Google; Se ha utilizado Google One; Se ha utilizado Android Switch; Se ha utilizado Google Fotos; Se ha utilizado Files de Google; Se ha utilizado Mensajes de Google; Se ha utilizado Google Chat; Se ha utilizado Google Drive; Se ha utilizado Google Home; Se ha utilizado Words of Wonders: Crucigrama; Se ha utilizado Meta AI; Se ha utilizado Facebook; Se ha utilizado Dropbox: Secure Cloud Storage; Se ha utilizado com.android.intentresolver; Se ha utilizado com.android.htmlviewer; Se ha utilizado Google Chrome; Se ha utilizado WPS Office Lite; Se ha utilizado WPS Office: PDF, Word, Excel; Se ha utilizado Photo Picker. La hora compartida no implica aperturas simultáneas.

2026-09-20T19:29:40.000000-06:00 · 1 observaciones: Has utilizado Banco Azteca - Apps on Google Play. La hora compartida no implica aperturas simultáneas.

## Dropbox: un cruce muy próximo con la actividad de la app

El 21-09 a las 07:03:33 aparecen búsqueda/ficha de Dropbox en Play. Los avisos de correo son de 07:04:25 (Dropbox for Android) y 07:04:26 (explorador web). Google Analytics registra uso de com.dropbox.android a las 07:04:32: seis/siete segundos después de los avisos. Son representaciones coherentes por servicio y proximidad; se conservan ambas, sin atribuir la sesión a otra persona ni inferir una automatización.

**E072878** · 2026-09-21T07:04:25.000000-06:00 · UTC 2026-09-21T13:04:25.000000+00:00 · MBOX · Cabeceras Date
Correo · no-reply@dropbox.com · Hola, Adilene, notamos un nuevo inicio de sesión en tu cuenta de Dropbox
S508 · {"mbox_message_index_1based": 268, "mail_id": "M000268", "message_id": "<010101a0c411575d-a60dec68-f732-4fd4-941d-8402a5e7c306-000000@us-west-2.amazonses.com>"}

[Leer correo local M000268](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000268.html)

**E072879** · 2026-09-21T07:04:26.000000-06:00 · UTC 2026-09-21T13:04:26.000000+00:00 · MBOX · Cabeceras Date
Correo · no-reply@dropbox.com · Hola, Adilene, notamos un nuevo inicio de sesión en tu cuenta de Dropbox
S508 · {"mbox_message_index_1based": 267, "mail_id": "M000267", "message_id": "<010001a0c4115983-3c6de24a-584a-4f47-92a2-a6520b13c89b-000000@email.amazonses.com>"}

[Leer correo local M000267](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000267.html)

**E072880** · 2026-09-21T07:04:32.000000-06:00 · UTC 2026-09-21T13:04:32.000000+00:00 · Google Analytics
Has utilizado Dropbox: Secure Cloud Storage - Apps on Google Play
S012 · {"record_index_1based": 89, "html_line_1based": 33, "html_column_0based": 94172}

**E072881** · 2026-09-21T07:04:32.000000-06:00 · UTC 2026-09-21T13:04:32.000000+00:00 · Publicidad
Has utilizado Dropbox: Secure Cloud Storage - Apps on Google Play
S024 · {"record_index_1based": 102, "html_line_1based": 33, "html_column_0based": 111892}

**E072880** · 2026-09-21T07:04:32.000000-06:00 · UTC 2026-09-21T13:04:32.000000+00:00 · Google Analytics
Has utilizado Dropbox: Secure Cloud Storage - Apps on Google Play
S012 · {"record_index_1based": 89, "html_line_1based": 33, "html_column_0based": 94172}

**E072881** · 2026-09-21T07:04:32.000000-06:00 · UTC 2026-09-21T13:04:32.000000+00:00 · Publicidad
Has utilizado Dropbox: Secure Cloud Storage - Apps on Google Play
S024 · {"record_index_1based": 102, "html_line_1based": 33, "html_column_0based": 111892}

**E072885** · 2026-09-21T07:05:45.000000-06:00 · UTC 2026-09-21T13:05:45.000000+00:00 · MBOX · Cabeceras Date
Correo · noreply-accounts@google.com · Compartiste algunos datos de tu Cuenta de Google con WPS Office
S508 · {"mbox_message_index_1based": 235, "mail_id": "M000235", "message_id": "<631091175a1640ab8271c9d62f5cba6a2d4f3e0d-20376977-337030291@google.com>"}

[Leer correo local M000235](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000235.html)

A las 07:05:45 el correo de Google informa Acceder con Google para WPS Office. Ese mensaje describe una conexión de cuenta; las entradas de Play permiten revisar usos e instalaciones por separado. No se convierte automáticamente en una apertura de WPS a esa misma hora.

## Uber: soporte corroborado y un recibo que aclara las horas Local

**E062905** · 2026-09-18T06:42:14.000000-06:00 · UTC 2026-09-18T12:42:14.000000+00:00 · MBOX · Cabeceras Date
Correo · contact_c1d772bd-662b-41eb-a467-fc91bdcef4a9@email-support.uber.com · Cómo enviar una consulta de privacidad
S508 · {"mbox_message_index_1based": 239, "mail_id": "M000239", "message_id": "<78d0c658-2007-459a-a54b-4ab6582592a1@mail.uber.com>"}

[Leer correo local M000239](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000239.html)

El correo de soporte Uber del 18-09 a las 06:42:14 coincide exactamente en fecha UTC con la respuesta del CSV customer_support_tickets. Se puede leer la misma respuesta en dos exportaciones. Esto mantiene la aclaración actual del usuario: no hubo clonación, el mensaje reflejaba su duda de entonces.

**E075334** · 2026-09-21T15:00:47.000000-06:00 · UTC 2026-09-21T21:00:47.000000+00:00 · MBOX · Cabeceras Date
Correo · noreply@uber.com · Tu pedido con Uber Eats del lunes por la tarde
S508 · {"mbox_message_index_1based": 181, "mail_id": "M000181", "message_id": "<a1202521-7914-54c5-bbb3-1df0c85f2e4d@mail.uber.com>"}

[Leer correo local M000181](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000181.html)

El recibo Eats del 21-09 muestra pedido 12:50 p.m., entrega 1:50 p.m. y pago/monto extra 3:00 p.m.; Date del correo es 15:00:47 México. Esto corrobora la interpretación local de Request_Time_Local=12:50:08 y Final_Delivery_Time_Local=13:50:14 del CSV, pese al sufijo Z. El correo posterior es un recibo con monto extra, no necesariamente el momento de entrega. La codificación del CSV se conserva sin modificar.

## La pista del juego en un mensaje de Facebook

**E075438** · 2026-09-24T09:21:33.000000-06:00 · UTC 2026-09-24T15:21:33.000000+00:00 · MBOX · Cabeceras Date
Correo · reminders@facebookmail.com · 8 Ball Pool Game te envió un mensaje y tienes 9 notificaciones más
S508 · {"mbox_message_index_1based": 166, "mail_id": "M000166", "message_id": "<727c12bb-9531-47ec-a7fa-3d6344b6b689@facebookmail.com>"}

[Leer correo local M000166](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000166.html)

Hay una notificación de Facebook del 24-09 a las 09:21:33: 8 Ball Pool Game te envió un mensaje y tienes 9 notificaciones más. Relaciona el nombre del juego con un aviso, pero su fecha está fuera de la noche del 20/21. El cuerpo no recupera el mensaje del juego. No se presenta como prueba de infección, un ataque o bloqueo del teléfono.

## Apple y Google: avisos recuperados por correo

**E072703** · 2026-09-21T03:53:35.000000-06:00 · UTC 2026-09-21T09:53:35.000000+00:00 · MBOX · Cabeceras Date
Correo · noreply@email.apple.com · Tu cuenta de Apple se usó para iniciar sesión en iCloud desde un navegador web
S508 · {"mbox_message_index_1based": 262, "mail_id": "M000262", "message_id": "<1060071348.105609466.1789984415091@email.apple.com>"}

[Leer correo local M000262](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000262.html)

**E072935** · 2026-09-21T08:28:18.000000-06:00 · UTC 2026-09-21T14:28:18.000000+00:00 · MBOX · Cabeceras Date
Correo · noreply@email.apple.com · Tu cuenta de Apple se usó para iniciar sesión en iCloud desde un navegador web
S508 · {"mbox_message_index_1based": 261, "mail_id": "M000261", "message_id": "<54930695.107137326.1790000898661@email.apple.com>"}

[Leer correo local M000261](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000261.html)

**E072979** · 2026-09-21T10:40:31.000000-06:00 · UTC 2026-09-21T16:40:31.000000+00:00 · MBOX · Cabeceras Date
Correo · noreply@email.apple.com · Tu cuenta de Apple se usó para iniciar sesión en iCloud desde un navegador web
S508 · {"mbox_message_index_1based": 260, "mail_id": "M000260", "message_id": "<618194584.108178056.1790008831295@email.apple.com>"}

[Leer correo local M000260](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000260.html)

Los tres correos Apple del 21-09 avisan de uso de iCloud en navegador. Sus cuerpos describen horas UTC distintas de Date por el tiempo de envío; se conservan ambos. Aportan avisos históricos de correo, sin consultar Apple Home o recuperar automatizaciones. Los registros iPhone del CSV Google se mantienen como actividad del dispositivo, no como prueba de identidad de quien actuó.

**E075041** · 2026-09-21T13:45:32.000000-06:00 · UTC 2026-09-21T19:45:32.000000+00:00 · MBOX · Cabeceras Date
Correo · no-reply@accounts.google.com · Alerta de seguridad
S508 · {"mbox_message_index_1based": 173, "mail_id": "M000173", "message_id": "<2NDhxryn4XZ_HLYrdoc4gg@notifications.google.com>"}

[Leer correo local M000173](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000173.html)

**E072948** · 2026-09-21T09:42:07.000000-06:00 · UTC 2026-09-21T15:42:07.000000+00:00 · MBOX · Cabeceras Date
Correo · families-noreply@google.com · Borraste tu grupo familiar
S508 · {"mbox_message_index_1based": 284, "mail_id": "M000284", "message_id": "<DfSom7dc0E1PQRP7iHwReg@notifications.google.com>"}

[Leer correo local M000284](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000284.html)

**E075337** · 2026-09-21T18:37:14.000000-06:00 · UTC 2026-09-22T00:37:14.000000+00:00 · MBOX · Cabeceras Date
Correo · no-reply@accounts.google.com · Alerta de seguridad crítica
S508 · {"mbox_message_index_1based": 158, "mail_id": "M000158", "message_id": "<Lg9zCsD31IZdej0QhGZ1lA@notifications.google.com>"}

[Leer correo local M000158](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000158.html)

**E075338** · 2026-09-21T18:39:22.000000-06:00 · UTC 2026-09-22T00:39:22.000000+00:00 · MBOX · Cabeceras Date
Correo · no-reply@accounts.google.com · Alerta de seguridad crítica
S508 · {"mbox_message_index_1based": 157, "mail_id": "M000157", "message_id": "<iEkWCoWt5j5NmkYGXSh6TQ@notifications.google.com>"}

[Leer correo local M000157](file:///home/deep-logic/ai-lab/research/vapid-webpush/correos/M000157.html)

Otros avisos del 21-09 describen cambio de contraseña Google (13:45:32), borrado de grupo familiar (09:42:07) y solicitudes de ayuda para acceder (18:37:14 y 18:39:22). Los mensajes de recuperación indican revisar eduardovelez@tutanota.de después de 30 días. Son el contenido de los avisos y no identifican quién realizó las acciones. No se atribuyen automáticamente a un ataque.

## Cómo seguir cada cruce

Hay 41 correos en la ventana del 20/21 y 8 cruces específicos guardados, además del contexto de usos de apps a ±5 minutos. El JSON distingue relaciones por texto/fecha y simples vecindades temporales. Los valores originales y adjuntos quedan íntegros en el MBOX y en el archivo privado de investigación. Los códigos M identifican el mensaje del MBOX; los E son de esta versión de la cronología.

[Índice local de correo](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/correo-indice.json)

[Cruces de correo y apps](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/correo-cruces-play.json)

<!-- FIN_RESULTADOS_SESION_9 -->


<!-- INICIO_RESULTADOS_SESION_10 -->
## Sesión 10: pista bydefault

## Pista bydefault: búsquedas y contexto recuperado

Se encontraron 16 observaciones Google sobre open by default: cuatro del 12 de enero (dos consultas de Ayuda y dos representaciones de una visita en Chrome) y doce del 26 de septiembre. No aparece el literal unido bydefault en los tres originales coincidentes. La sesión del 26-09 va de 20:59:15 a 21:00:21 México: una búsqueda Android y once registros support.google.com/apis/search con helpcenter=android y query=open by default. El campo next_page_token cambia; max_results=8 se mantiene. Esto es compatible con paginación de la misma consulta, como inferencia por la estructura de URL. No se conservó el resultado de cada petición ni se acredita contenido oculto.

Chrome/Historial.json, Browser History, registro 758, documenta la visita a support.google.com/android/search?q=open+by+default el 12-01 a las 18:58:48.969625 México, con CLIENT_REDIRECT. La actividad Chrome muestra esa visita a las 18:58:48 y Ayuda guarda la búsqueda a las 18:58:49. Es un cruce temporal concreto de la misma dirección; CLIENT_REDIRECT describe la transición registrada, sin identificar su causa ni demostrar manipulación.

La documentación oficial de Google usa Abrir de forma predeterminada para gestionar qué app abre una acción. En el contexto inmediato del 26-09 también hay consultas sobre Seguridad de los datos en Play y, a las 21:00:41, una pregunta sobre por qué Play busca libros en lugar de apps. Se conservan los parámetros completos en los originales y el JSON del cruce, sin convertirlos en una contraseña o un identificador de empresa.

[Cruce completo y parámetros conservados](file:///home/deep-logic/ai-lab/research/vapid-webpush/datos/bydefault-cruces.json)

[Ficha técnica BD01: aplicaciones predeterminadas](https://support.google.com/pixelphone/answer/6271667?hl=es)

2026-01-12T11:42:25.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 814, "html_line_1based": 33, "html_column_0based": 1076301}

2026-01-12T18:58:48.000000-06:00 · Chrome · Resultados de la búsqueda - Ayuda de Android
S008 · {"record_index_1based": 233, "html_line_1based": 33, "html_column_0based": 256029}

2026-01-12T18:58:48.969625-06:00 · Historial de Chrome · Resultados de la búsqueda - Ayuda de Android
S028 · {"record_index_1based": 758, "json_pointer": "/Browser History/757"}

2026-01-12T18:58:49.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 813, "html_line_1based": 33, "html_column_0based": 1075328}

2026-09-26T20:59:15.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 29, "html_line_1based": 33, "html_column_0based": 43845}

2026-09-26T20:59:39.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 28, "html_line_1based": 33, "html_column_0based": 41981}

2026-09-26T20:59:44.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 27, "html_line_1based": 33, "html_column_0based": 40114}

2026-09-26T20:59:47.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 26, "html_line_1based": 33, "html_column_0based": 38245}

2026-09-26T20:59:53.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 25, "html_line_1based": 33, "html_column_0based": 36373}

2026-09-26T20:59:56.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 24, "html_line_1based": 33, "html_column_0based": 34498}

2026-09-26T21:00:01.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 23, "html_line_1based": 33, "html_column_0based": 32621}

2026-09-26T21:00:05.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 22, "html_line_1based": 33, "html_column_0based": 30741}

2026-09-26T21:00:08.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 21, "html_line_1based": 33, "html_column_0based": 28858}

2026-09-26T21:00:11.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 20, "html_line_1based": 33, "html_column_0based": 26973}

2026-09-26T21:00:17.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 19, "html_line_1based": 33, "html_column_0based": 25085}

2026-09-26T21:00:21.000000-06:00 · Ayuda · open by default
S002 · {"record_index_1based": 18, "html_line_1based": 33, "html_column_0based": 23194}

<!-- FIN_RESULTADOS_SESION_10 -->


<!-- INICIO_RESULTADOS_SESION_12 -->
## Sesión 12: iPhone conectado

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

<!-- FIN_RESULTADOS_SESION_12 -->


<!-- INICIO_RESULTADOS_SESION_11 -->
## Sesión 11: GitHub y autorización de archivo íntegro

El propietario pidió descargar las herramientas, enlazar spinky-afk y subir todo el conjunto investigado, incluidos datos privados necesarios como pruebas. Se instalaron GitHub CLI 2.102.0 y Git LFS 3.8.0 mediante binarios oficiales, verificados con sus SHA-256 publicados. Se completó OAuth y la API user confirmó el login spinky-afk. No se registraron tokens ni códigos de autorización.

La carpeta evidencia del repositorio conserva todos los originales investigados y todos los archivos de research, incluidas claves y el MBOX íntegro. No se excluyen datos privados del conjunto. Las páginas de lectura conservan sus derivados y enlaces locales a los datos. El repositorio debe permanecer privado. Los archivos grandes se suben mediante Git LFS y se recuperan con git lfs pull. Las credenciales de la herramienta quedan en .tools, fuera del expediente.

El estado remoto verificado y la hora de publicación se registran en estado-publicacion.json. Fuentes técnicas consultadas: G03 GitHub CLI oficial, G04 Git LFS oficial, G05 gh auth login, G06 límites de archivos GitHub. Las fichas y enlaces se conservan en datos/github-fuentes-web.json.
<!-- FIN_RESULTADOS_SESION_11 -->


Publicación GitHub comprobada: https://github.com/spinky-afk/expediente-documental · privado · 2026-10-01T19:46:08.573148+00:00 · commit 60c2b1c5ec861583068127ac9871910d853b3f04. Git y LFS terminaron correctamente; la referencia remota main coincide.


Aclaración posterior del propietario: no tiene copia local del iPhone y teme actualizar el respaldo existente. Se explicó la diferencia entre copia local e iCloud y cómo consultar Safari en iOS 16. No se inició copia, restauración ni borrado. La hora exacta de la lectura USB no quedó capturada; su fecha se conserva con precisión de día para evitar una hora inventada.
