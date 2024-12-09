FROM python:${PYTHON_VERSION}-slim as base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/bin/bash" \
    --uid "${UID}" \
    appuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Make sure .env has correct permissions
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE 8000
CMD ["gunicorn", \
     "-w", "3", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--preload", \
     "--timeout", "300", \
     "--graceful-timeout", "300", \
     "--max-requests", "1000", \
     "--max-requests-jitter", "50", \
     "tts_linkedin:app", \
     "--bind", "0.0.0.0:8000"]
