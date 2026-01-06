FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# create the current dirctory
WORKDIR /code


COPY pyproject.toml .python-version uv.lock ./

# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked


# set up our image by installing prerequisites; pandas in this case
#RUN pip install pandas pyarrow


# Add virtual environment to PATH so we can use installed packages
ENV PATH="/code/.venv/bin:$PATH"


#copy the pipeline.py to the current directory .
COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]