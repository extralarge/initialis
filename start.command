#!/bin/zsh
cd "$(dirname "$0")"
python3 - <<'PY'
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import threading
import webbrowser

server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(Path.cwd())))
url = f'http://localhost:{server.server_port}'
print(f'Initialis Cyrillic: {url}\nClose this terminal to stop the local preview.', flush=True)
threading.Timer(0.5, lambda: webbrowser.open(url)).start()
try:
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
PY
