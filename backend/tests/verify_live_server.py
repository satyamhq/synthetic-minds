"""
Live HTTP Server Verification Script
Starts wsgi.py on port 5005 and sends real HTTP requests to verify production behavior.
"""
import subprocess
import time
import sys
import os
import urllib.request
import urllib.error
import json

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
wsgi_file = os.path.join(root_dir, 'wsgi.py')

env = os.environ.copy()
env['PORT'] = '5005'
env['FLASK_HOST'] = '127.0.0.1'

print(f"Launching server: {wsgi_file} on port 5005...")
proc = subprocess.Popen(
    [sys.executable, wsgi_file],
    cwd=root_dir,
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

try:
    started = False
    for _ in range(40):
        time.sleep(0.5)
        try:
            req = urllib.request.Request('http://127.0.0.1:5005/health')
            with urllib.request.urlopen(req, timeout=2) as resp:
                if resp.status == 200:
                    started = True
                    break
        except Exception:
            pass

    if not started:
        stdout, stderr = proc.communicate(timeout=2)
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
        raise RuntimeError("Server failed to respond on http://127.0.0.1:5005/health")

    print("=== LIVE SERVER STARTED ON PORT 5005 ===")

    # 1. Test GET /
    with urllib.request.urlopen('http://127.0.0.1:5005/') as resp:
        assert resp.status == 200
        content = resp.read().decode('utf-8')
        assert 'Synthetic Minds' in content or 'id="app"' in content
        print(f"[OK] GET / -> 200 OK (Cache-Control: {resp.headers.get('Cache-Control')})")

    # 2. Test HEAD /
    req = urllib.request.Request('http://127.0.0.1:5005/', method='HEAD')
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        print("[OK] HEAD / -> 200 OK")

    # 3. Test GET /health
    with urllib.request.urlopen('http://127.0.0.1:5005/health') as resp:
        assert resp.status == 200
        data = json.loads(resp.read().decode('utf-8'))
        assert data.get('status') == 'ok'
        print("[OK] GET /health -> 200 OK JSON:", data)

    # 4. Test HEAD /health
    req = urllib.request.Request('http://127.0.0.1:5005/health', method='HEAD')
    with urllib.request.urlopen(req) as resp:
        assert resp.status == 200
        print("[OK] HEAD /health -> 200 OK")

    # 5. Test SPA direct navigation (e.g. /process/project-123)
    with urllib.request.urlopen('http://127.0.0.1:5005/process/project-123') as resp:
        assert resp.status == 200
        content = resp.read().decode('utf-8')
        assert 'id="app"' in content
        print("[OK] GET /process/project-123 -> 200 OK (SPA fallback returning index.html)")

    # 6. Test SPA direct navigation (e.g. /simulation/sim-456)
    with urllib.request.urlopen('http://127.0.0.1:5005/simulation/sim-456') as resp:
        assert resp.status == 200
        content = resp.read().decode('utf-8')
        assert 'id="app"' in content
        print("[OK] GET /simulation/sim-456 -> 200 OK (SPA fallback returning index.html)")

    # 7. Test static asset: favicon.svg
    with urllib.request.urlopen('http://127.0.0.1:5005/favicon.svg') as resp:
        assert resp.status == 200
        print(f"[OK] GET /favicon.svg -> 200 OK (Content-Type: {resp.headers.get('Content-Type')})")

    # 8. Test API 404 isolation (must return JSON, NOT SPA HTML)
    try:
        urllib.request.urlopen('http://127.0.0.1:5005/api/nonexistent_route')
        assert False, "Expected HTTP 404"
    except urllib.error.HTTPError as e:
        assert e.code == 404
        data = json.loads(e.read().decode('utf-8'))
        assert data.get('success') is False
        print("[OK] GET /api/nonexistent_route -> 404 Not Found JSON:", data)

    print("\n=== ALL LIVE HTTP TESTS PASSED WITH 100% SUCCESS ===")

finally:
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except Exception:
        proc.kill()
