"""Lectura fiel de la exportación de Uber, sin modificar los originales."""
import csv
import bisect
import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path('/home/deep-logic/Documentos/Uber Data Request 5A426B63/Uber Data')
ZONE = ZoneInfo('America/Mexico_City')

def rows(path):
    with Path(path).open(encoding='utf-8-sig', newline='') as handle:
        reader = csv.DictReader(handle)
        reader.fieldnames
        previous = reader.line_num
        for index, row in enumerate(reader, 1):
            locator = {'csv_record_index_1based': index, 'csv_line_1based': previous + 1, 'csv_end_line_1based': reader.line_num}
            previous = reader.line_num
            yield row, locator

def utc(value, explicit_utc=False):
    if not value:
        return None
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc) if explicit_utc else None
    return parsed.astimezone(timezone.utc)

def local_column(value):
    # The CSV labels these columns Local, but appends Z, also on Rider's
    # explicitly paired local/UTC columns. Preserve and flag this assumption.
    return datetime.fromisoformat(value.replace('Z', '+00:00')).replace(tzinfo=ZONE)

def cross_correlations(events):
    """Candidatos por proximidad, sin afirmar que dos filas sean el mismo evento."""
    pools = {}
    for product in ['Rider', 'Eats']:
        records = sorted((e for e in events if e['family']=='Uber' and e['channel']==product+' · Analytics'), key=lambda e:e['time_utc'])
        pools[product] = ([datetime.fromisoformat(e['time_utc']).timestamp() for e in records], records)
    matches=[]
    for target in events:
        product=None
        if target.get('business_name') in ['Uber Eats: Food and Grocery', 'ubereats.com']:
            product='Eats'
        elif target.get('business_name')=='Uber - Request a ride':
            product='Rider'
        elif target['family']=='Google' and target['channel'] in ['Google Analytics','Google Play Store']:
            url=target.get('url_original') or target.get('url') or ''
            if 'id=com.ubercab.eats' in url:product='Eats'
            elif 'id=com.ubercab' in url and 'driver' not in url:product='Rider'
        if product is None or not target.get('time_utc'):
            continue
        times, records=pools[product]
        if not times:continue
        stamp=datetime.fromisoformat(target['time_utc']).timestamp()
        left,right=bisect.bisect_left(times,stamp-60),bisect.bisect_right(times,stamp+60)
        if right<=left:continue
        index=min(range(left,right),key=lambda i:abs(times[i]-stamp))
        matches.append({'type':'Uber: mismo producto y proximidad de hasta 60 segundos; candidato temporal sin ID compartido', 'event_ids':[target['id'],records[index]['id']], 'product':product, 'seconds_signed_uber_minus_other':round(times[index]-stamp,6), 'uber_rows_in_60_second_window':right-left, 'shared_event_id':False})
    return matches

def collect(api):
    if not ROOT.exists():
        return
    for path in sorted(ROOT.rglob('*')):
        if not path.is_file():
            continue
        api.register(path, 'Uber')
        if path.suffix.lower() != '.csv':
            continue
        relative = str(path.relative_to(ROOT))
        for row, locator in rows(path):
            original = json.dumps(row, ensure_ascii=False)
            if path.name in ['rider_app_analytics-0.csv', 'eats_app_analytics-0.csv']:
                product = 'Rider' if relative.startswith('Rider/') else 'Eats'
                stamp = row['Event Time (UTC)']
                identifiers = {'product': product, 'device_model': row['Device Model'], 'device_os': row['Device OS'], 'device_os_version': row['Device OS Version'], 'analytics_event_type': row['Analytics Event Type']}
                if row.get('Device ID'):
                    identifiers['uber_device_id'] = row['Device ID']
                if row.get('App Version'):
                    identifiers['app_version'] = row['App Version']
                api.event(path, 'Uber', product+' · Analytics', 'evento de app',
                          'Uber '+product+' · '+(row['Analytics Event Type'] or '[tipo vacío]')+' · '+row['Device Model']+' / '+row['Device OS']+' '+row['Device OS Version'],
                          utc(stamp, True), locator, text=original, original_date=stamp,
                          precision='milisegundo', identifiers=identifiers,
                          timezone_basis='UTC explícito en Event Time (UTC). GPS Time y Session Start se conservan como campos auxiliares del CSV, no como eventos nuevos.')
            elif path.name == 'rider_lifetime_trips-0.csv':
                for label in ['request_timestamp_utc', 'begintrip_timestamp_utc', 'dropoff_timestamp_utc']:
                    if not row.get(label):
                        continue
                    api.event(path, 'Uber', 'Rider · Viajes', label,
                              'Uber Rider · '+row['status']+' · '+label+' · '+row['city_name'],
                              utc(row[label], True), {**locator, 'csv_field': label}, text=original, original_date=row[label],
                              precision='milisegundo', identifiers={'product': 'Rider', 'status': row['status']},
                              timezone_basis='Se usa la columna UTC; las columnas local y timezone permanecen en el original.')
            elif path.name == 'user_orders-0.csv':
                for label in ['Request_Time_Local', 'Final_Delivery_Time_Local']:
                    if not row.get(label):
                        continue
                    api.event(path, 'Uber', 'Eats · Pedidos', label,
                              'Uber Eats · '+row['Order_Status']+' · '+row['Restaurant_Name']+' · '+row['Item_Name']+' · '+label,
                              local_column(row[label]), {**locator, 'csv_field': label}, text=original, original_date=row[label],
                              precision='milisegundo', identifiers={'product': 'Eats', 'status': row['Order_Status']},
                              timezone_basis='HIPÓTESIS DE ZONA: la columna se llama Local pero el valor termina en Z. Se interpreta como reloj America/Mexico_City, apoyado por los pares local/UTC de Rider y el mensaje de soporte KFC; no se considera una conversión confirmada.')
            elif path.name == 'customer_support_tickets-0.csv':
                api.event(path, 'Uber', 'Soporte', 'registro de soporte',
                          'Uber · Creator='+row['Creator']+' · '+row['Message'],
                          utc(row['Date']), locator, text=original, original_date=row['Date'], precision='milisegundo',
                          identifiers={'creator_field': row['Creator']}, timezone_basis='Date tiene sufijo Z explícito. Creator se conserva como campo, sin corregir o inferir el remitente.')
            elif path.name == 'payment_methods-0.csv':
                stamp = row.get('Deleted At', '')
                api.event(path, 'Uber', 'Métodos de pago', 'borrado registrado' if stamp else 'inventario sin fecha',
                          'Uber · método de pago · '+row['Profile Type']+' · '+row['Payment Method Brand']+' · '+row['Bank/Issuer Name'],
                          utc(stamp), locator, text=original, original_date=stamp or None,
                          identifiers={'profile_type': row['Profile Type']}, timezone_basis='Deleted At se usa solo cuando contiene una zona explícita. El inventario no indica fechas de alta.')
            elif path.name == 'communications_sent-0.csv':
                api.event(path, 'Uber', 'Comunicaciones', 'mensaje con zona sin determinar',
                          'Uber · '+row['Direction']+' · '+row['Medium']+' · '+row['Content'],
                          utc(row['Time']), locator, text=original, original_date=row['Time'],
                          identifiers={'direction': row['Direction'], 'medium': row['Medium']},
                          timezone_basis='Time no especifica zona. Se conserva fuera de la cronología confirmada; canales repetidos no se eliminan.')
            else:
                stamp = row.get('Signup Date') or row.get('First Payment Method Added Timestamp')
                subject = 'Uber · '+relative
                if 'profile' in path.name:
                    subject += ' · '+str(row.get('E-Mail', row.get('E-mail', '')))+' · '+str(row.get('User Type', row.get('Driver Profile', '')))
                api.event(path, 'Uber', 'Cuenta y perfil', 'registro sin fecha o zona determinada', subject,
                          utc(stamp) if stamp else None, locator, text=original, original_date=stamp,
                          timezone_basis='No se asigna zona a fechas sin offset ni se inventa fecha para inventarios o puntuaciones.')
