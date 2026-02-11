# Start with slim Python 3.13 image
FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /app

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better caching)
COPY pyproject.toml uv.lock .python-version ./

# Install dependencies from lock file
RUN uv sync --locked

# Copy application code
COPY pipeline.py pipeline.py

# Set entry point
ENTRYPOINT ["python", "pipeline.py"]