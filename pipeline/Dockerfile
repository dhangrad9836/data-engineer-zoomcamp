FROM python:3.13.11-slim

# Copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

COPY pyproject.toml .python-version uv.lock ./

# this will install the dependencies from the uv.lock file
RUN uv sync --locked

# RUN pip install pandas pyarrow

# create the current dirctory
WORKDIR /code

#copy the pipeline.py to the current directory .
COPY pipeline.py .

ENTRYPOINT ["uv", "run","python", "pipeline.py"]