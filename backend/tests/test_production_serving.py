"""
Production Serving Tests for Render Deployment
Verifies:
1. GET / and HEAD / return 200 and frontend index.html
2. GET /health and HEAD /health return 200 JSON
3. GET /api/health returns 200 JSON
4. Direct SPA navigation (e.g., /process/new, /simulation/abc) returns 200 and index.html
5. Static assets (favicon, robots, sitemap, css, js) are served with correct status
6. API routes strictly return 404 JSON (never HTML index.html fallback)
7. Production security headers are applied to responses
8. CORS configuration allows Render origins
"""
import os
import pytest
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_root_get_returns_spa(client):
    """Test GET / returns 200 with index.html."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Synthetic Minds' in response.data or b'id="app"' in response.data


def test_root_head_returns_200(client):
    """Test HEAD / returns 200."""
    response = client.head('/')
    assert response.status_code == 200


def test_health_get_returns_200_json(client):
    """Test GET /health returns 200 JSON."""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert data.get('status') == 'ok'


def test_health_head_returns_200(client):
    """Test HEAD /health returns 200."""
    response = client.head('/health')
    assert response.status_code == 200


def test_api_health_returns_200(client):
    """Test GET /api/health returns 200."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data is not None
    assert data.get('status') == 'ok'


def test_spa_direct_routes(client):
    """Test SPA fallback for direct navigation to client-side routes."""
    routes = [
        '/process/new',
        '/process/proj-12345',
        '/simulation/sim-67890',
        '/simulation/sim-67890/start',
        '/report/rep-11111',
        '/interaction/rep-11111',
    ]
    for route in routes:
        response = client.get(route)
        assert response.status_code == 200, f"Route {route} failed with {response.status_code}"
        assert b'id="app"' in response.data or b'Synthetic Minds' in response.data


def test_static_files_served(client):
    """Test static assets are served properly."""
    for asset in ['/favicon.svg', '/robots.txt', '/sitemap.xml']:
        response = client.get(asset)
        assert response.status_code == 200, f"Asset {asset} failed with {response.status_code}"


def test_api_404_isolation(client):
    """Test that nonexistent /api routes return 404 JSON, NOT SPA HTML."""
    response = client.get('/api/nonexistent_endpoint')
    assert response.status_code == 404
    data = response.get_json()
    assert data is not None
    assert data.get('success') is False
    assert 'not found' in data.get('error', '').lower()

    # Also test POST to nonexistent api endpoint
    post_res = client.post('/api/nonexistent_endpoint', json={'test': 1})
    assert post_res.status_code == 404
    post_data = post_res.get_json()
    assert post_data is not None
    assert post_data.get('success') is False


def test_security_headers_applied(client):
    """Test that standard production security headers are set."""
    response = client.get('/health')
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('X-Frame-Options') == 'SAMEORIGIN'
    assert response.headers.get('Referrer-Policy') == 'strict-origin-when-cross-origin'


def test_cors_render_origin(client):
    """Test that Render production origins are accepted via CORS."""
    headers = {
        'Origin': 'https://synthetic-minds.onrender.com'
    }
    response = client.get('/api/health', headers=headers)
    assert response.status_code == 200
    assert response.headers.get('Access-Control-Allow-Origin') == 'https://synthetic-minds.onrender.com'
