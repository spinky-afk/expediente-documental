#!/usr/bin/env python3
"""Servidor de consulta local: no permite publicar el archivo en la red."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

class LocalHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control','no-store')
        self.send_header('Referrer-Policy','no-referrer')
        self.send_header('X-Content-Type-Options','nosniff')
        super().end_headers()

if __name__=='__main__':
    folder=Path(__file__).resolve().parent/'sitio'
    server=ThreadingHTTPServer(('127.0.0.1',8765),partial(LocalHandler,directory=str(folder)))
    print('Consulta local: http://127.0.0.1:8765 (Ctrl+C para terminar)',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: server.server_close()
