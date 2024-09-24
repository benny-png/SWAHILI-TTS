# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.11.2
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/bin/bash" \
    --uid "${UID}" \
    appuser

# Set environment variables for Hugging Face and Matplotlib
ENV TRANSFORMERS_CACHE=/home/appuser/.cache/huggingface
ENV MPLCONFIGDIR=/home/appuser/.config/matplotlib

# Download dependencies as a separate step to take advantage of Docker's caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container.
COPY . .

# Change ownership of the application directory to appuser
RUN chown -R appuser:appuser /app

# Switch to the non-privileged user to run the application.
USER appuser

# Create necessary directories with correct permissions
RUN mkdir -p /home/appuser/.cache/huggingface \
    && mkdir -p /home/appuser/.config/matplotlib

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD ["uvicorn", "tts_linkedin:app", "--host", "0.0.0.0", "--port", "8000"]