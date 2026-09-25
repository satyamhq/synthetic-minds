"""
Synthetic Minds Backend Server
"""

import os
import sys

# Ensure UTF-8 encoding for console output on Windows across standard streams
if sys.platform == 'win32':
    os.environ.setdefault('PYTHONIOENCODING', 'utf-8')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# Add backend directory to system path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import Config


def main():
    """Main server entrypoint."""
    # Validate required configuration
    errors = Config.validate()
    if errors:
        print("Configuration error:")
        for err in errors:
            print(f"  - {err}")
        print("\nPlease check your configuration in .env")
        sys.exit(1)
    
    # Initialize Flask application
    app = create_app()
    
    # Retrieve runtime configuration
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5001))
    debug = Config.DEBUG
    
    # Start server
    app.run(host=host, port=port, debug=debug, threaded=True)


if __name__ == '__main__':
    main()
