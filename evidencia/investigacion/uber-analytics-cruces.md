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
