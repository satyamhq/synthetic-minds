"""
WSGI entrypoint for Synthetic Minds backend service.
Exposes 'app' for Gunicorn: gunicorn --bind 0.0.0.0:$PORT wsgi:app
"""
import os
import sys

backend_dir = os.path.abspath(os.path.dirname(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app import create_app

app = create_app()

if __name__ == '__main__':
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT') or os.environ.get('FLASK_PORT') or 5001)
    app.run(host=host, port=port)
