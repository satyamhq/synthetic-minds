FROM python:3.11-slim

# Install Node.js (>=18), npm, and required system utilities
RUN apt-get update \
  && apt-get install -y --no-install-recommends nodejs npm \
  && rm -rf /var/lib/apt/lists/*

# Copy uv from official Astral image
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

WORKDIR /app

# Copy dependency specifications for layer caching
COPY package.json package-lock.json ./
COPY frontend/package.json frontend/package-lock.json ./frontend/
COPY backend/pyproject.toml backend/uv.lock backend/requirements.txt ./backend/
COPY requirements.txt ./

# Install dependencies (Node + Python)
RUN npm ci \
  && npm ci --prefix frontend \
  && cd backend && uv sync --frozen

# Copy application source
COPY . .

# Build frontend production assets into frontend/dist
RUN npm run build --prefix frontend

# Expose Render standard port
EXPOSE 10000

ENV PORT=10000
ENV FLASK_DEBUG=False
ENV PYTHONUNBUFFERED=1

# Start production WSGI server with Gunicorn (single process on $PORT)
CMD ["sh", "-c", "cd /app/backend && uv run gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --threads 4 --timeout 120 wsgi:app"]