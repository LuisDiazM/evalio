FROM python:3.12-slim

# Minimal, secure image for admin that requires OpenCV and is run via `uv`.
# - keep image small: install only runtime deps
# - run as non-root user

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_RUN_NO_SYNC=1 \
    UV_COMPILE_BYTECODE=1

WORKDIR /app

# Install only the runtime OS packages required by OpenCV and typical multimedia libs
# Avoid build tools to keep image small; add them only if you need to compile packages.
RUN apt-get update \
  && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# Create a non-root user for running the app
RUN groupadd --gid 1000 appgroup \
  && useradd --uid 1000 --gid appgroup --shell /bin/false --create-home appuser

# Copy pyproject first so we can cache dependency installation when code changes
COPY pyproject.toml /app/

# Upgrade pip and install hatchling (PEP 517 build backend) so we can install the package from pyproject
# Also install `uv` CLI so `uv run ...` is available inside the image (used by project tooling)
RUN pip install --upgrade pip hatchling \
  && pip install --no-cache-dir uv

# Copy application files
COPY . /app

# Install the package (this will install dependencies declared in pyproject.toml)
RUN uv sync --no-dev

# Ensure app files are owned by non-root user
RUN chown -R appuser:appgroup /app

USER appuser

# Use `uv` to run the app (assumes `uv` is declared in pyproject dependencies)
CMD ["uv", "run", "--no-sync", "admin/main.py"]

## Notes:
# docker build -f backend/admin/Dockerfile -t admin:latest backend/admin
