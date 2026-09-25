"""
Synthetic Minds Backend - Flask Application Factory
"""

import os
import warnings

# Suppress multiprocessing resource_tracker warnings from third-party libraries
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

import mimetypes
# Ensure standard MIME types are recognized correctly across environments
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('image/svg+xml', '.svg')

from flask import Flask, request, send_from_directory, jsonify, make_response
from flask_cors import CORS

from .config import Config
from .utils.logger import setup_logger, get_logger


def create_app(config_class=Config):
    """Flask application factory."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Set JSON encoding: ensure clean UTF-8 string rendering
    if hasattr(app, 'json') and hasattr(app.json, 'ensure_ascii'):
        app.json.ensure_ascii = False
    
    # Setup logger
    logger = setup_logger('synthetic_minds')
    
    # Only print startup banner in reloader subprocess to avoid duplicate logs in debug mode
    is_reloader_process = os.environ.get('WERKZEUG_RUN_MAIN') == 'true'
    debug_mode = app.config.get('DEBUG', False)
    should_log_startup = not debug_mode or is_reloader_process
    
    if should_log_startup:
        logger.info("=" * 50)
        logger.info("Synthetic Minds Backend starting...")
        logger.info("=" * 50)
    import re

    # Configure CORS: allow same-origin, onrender.com domains, and explicitly configured trusted origins
    allowed_origins = [
        re.compile(r"^https?://.*\.onrender\.com$"),
        "https://synthetic-minds.onrender.com",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    render_external_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
    if render_external_hostname:
        for proto in ["https://", "http://"]:
            h = f"{proto}{render_external_hostname}"
            if h not in allowed_origins:
                allowed_origins.append(h)
    custom_origins = os.environ.get('CORS_ALLOWED_ORIGINS')
    if custom_origins:
        for origin in custom_origins.split(','):
            origin = origin.strip()
            if origin and origin not in allowed_origins:
                allowed_origins.append(origin)
    
    CORS(app, resources={r"/api/*": {"origins": allowed_origins if not debug_mode else "*"}})
    
    # Register simulation process cleanup handlers on server exit
    from .services.simulation_runner import SimulationRunner
    SimulationRunner.register_cleanup()
    if should_log_startup:
        logger.info("Registered simulation process cleanup handlers")
    
    # Request logging middleware
    @app.before_request
    def log_request():
        req_logger = get_logger('synthetic_minds.request')
        req_logger.debug(f"Request: {request.method} {request.path}")
        if request.content_type and 'json' in request.content_type:
            req_logger.debug(f"Request Body: {request.get_json(silent=True)}")
    
    @app.after_request
    def apply_security_and_log(response):
        res_logger = get_logger('synthetic_minds.request')
        res_logger.debug(f"Response: {response.status_code}")
        # Standard production security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        return response
    
    # Register blueprints
    from .api import graph_bp, simulation_bp, report_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    
    # Locate frontend distribution directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    possible_dist_dirs = [
        os.path.join(root_dir, 'frontend', 'dist'),
        os.path.join(root_dir, 'dist'),
        os.path.abspath(os.path.join(os.getcwd(), 'frontend', 'dist')),
        os.path.abspath(os.path.join(os.getcwd(), 'dist')),
    ]
    dist_dir = next((d for d in possible_dist_dirs if os.path.isdir(d)), None)
    if dist_dir and should_log_startup:
        logger.info(f"Serving frontend static files from: {dist_dir}")

    # Health check endpoints (support both GET and HEAD)
    @app.route('/health', methods=['GET', 'HEAD'])
    @app.route('/api/health', methods=['GET', 'HEAD'])
    def health():
        return jsonify({'status': 'ok', 'service': 'Synthetic Minds Backend'}), 200

    # Root route: serve frontend index.html or health fallback
    @app.route('/', methods=['GET', 'HEAD'])
    def serve_root():
        if dist_dir and os.path.isfile(os.path.join(dist_dir, 'index.html')):
            response = make_response(send_from_directory(dist_dir, 'index.html'))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response
        return jsonify({
            'status': 'ok',
            'service': 'Synthetic Minds Backend',
            'message': 'Frontend not built yet. Run npm run build in frontend directory.'
        }), 200

    # Catch-all route for static assets, SPA client-side routing, and API 404 isolation
    @app.route('/<path:path>', methods=['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'])
    def serve_spa(path):
        # Strict API 404 isolation: Unmatched API requests never fall back to index.html
        if path.startswith('api/') or path == 'api':
            return jsonify({'success': False, 'error': f"Endpoint not found: /{path}"}), 404

        if request.method not in ['GET', 'HEAD']:
            return jsonify({'success': False, 'error': 'Method Not Allowed'}), 405

        if dist_dir:
            file_path = os.path.join(dist_dir, path)
            if os.path.isfile(file_path):
                return send_from_directory(dist_dir, path)
            # SPA fallback: return index.html for non-asset frontend routes
            index_path = os.path.join(dist_dir, 'index.html')
            if os.path.isfile(index_path):
                response = make_response(send_from_directory(dist_dir, 'index.html'))
                response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                return response

        return jsonify({'success': False, 'error': f"Endpoint not found: /{path}"}), 404

    # Global error handlers (consistent JSON responses for APIs and SPA fallback)
    @app.errorhandler(400)
    def handle_bad_request(e):
        return jsonify({'success': False, 'error': str(e.description) if hasattr(e, 'description') else 'Bad Request'}), 400

    @app.errorhandler(404)
    def handle_not_found(e):
        if request.path.startswith('/api/') or request.path == '/api':
            return jsonify({'success': False, 'error': f"Endpoint not found: {request.path}"}), 404
        if dist_dir and os.path.isfile(os.path.join(dist_dir, 'index.html')) and request.method in ['GET', 'HEAD']:
            response = make_response(send_from_directory(dist_dir, 'index.html'))
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            return response
        return jsonify({'success': False, 'error': f"Endpoint not found: {request.path}"}), 404

    @app.errorhandler(405)
    def handle_method_not_allowed(e):
        return jsonify({'success': False, 'error': 'Method Not Allowed'}), 405

    @app.errorhandler(500)
    def handle_server_error(e):
        logger.error(f"Internal server error: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Internal server error occurred.'}), 500

    @app.errorhandler(Exception)
    def handle_unexpected_exception(e):
        logger.error(f"Unhandled exception: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'An unexpected error occurred.'}), 500
    
    if should_log_startup:
        logger.info("Synthetic Minds Backend started successfully")
    
    return app
