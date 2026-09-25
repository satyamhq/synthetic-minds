"""
Synthetic Minds Backend - Flask Application Factory
"""

import os
import warnings

# Suppress multiprocessing resource_tracker warnings from third-party libraries
warnings.filterwarnings("ignore", message=".*resource_tracker.*")

from flask import Flask, request
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
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
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
    def log_response(response):
        res_logger = get_logger('synthetic_minds.request')
        res_logger.debug(f"Response: {response.status_code}")
        return response
    
    # Register blueprints
    from .api import graph_bp, simulation_bp, report_bp
    app.register_blueprint(graph_bp, url_prefix='/api/graph')
    app.register_blueprint(simulation_bp, url_prefix='/api/simulation')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'ok', 'service': 'Synthetic Minds Backend'}
    
    if should_log_startup:
        logger.info("Synthetic Minds Backend started successfully")
    
    return app
