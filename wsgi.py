"""
WSGI entrypoint for Synthetic Minds production deployment on Render.
Exposes 'app' for Gunicorn: gunicorn --bind 0.0.0.0:$PORT wsgi:app
"""
import os
import sys

# Ensure backend directory is in sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app import create_app

app = create_app()

if __name__ == '__main__':
    # Safe local fallback when executed directly
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT') or os.environ.get('FLASK_PORT') or 5001)
    app.run(host=host, port=port)
