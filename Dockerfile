# Bug Bounty Cal-Report — FastAPI service image.
# Compatibility only: this file makes the repo Docker-ready.
# Nothing deploys unless someone builds and runs the image.
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the package definition and source, then install.
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir .

# Run as a non-root user.
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/')" || exit 1

CMD ["uvicorn", "src.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
