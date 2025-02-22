# Use an official Python image
FROM python:3.12

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PATH="/home/django/.local/bin:$PATH" \
    DATABASE_PATH="/docker_app/data/db.sqlite3"

# Create a non-root user and set up directories
RUN useradd -m django && \
    mkdir -p /docker_app && \
    mkdir -p /docker_app/data && \
    chown -R django:django /docker_app

# Set the working directory
WORKDIR /docker_app

# Switch to non-root user
USER django

# Copy requirements and install dependencies
COPY --chown=django:django requirements.txt .
RUN pip install --user --upgrade pip && \
    pip install --user -r requirements.txt

# Copy the project files
COPY --chown=django:django . .

# Make sure the media and static directories are writable
RUN mkdir -p media static && \
    chmod 755 media static

# Ensure SQLite database directory is writable
RUN mkdir -p /docker_app/data && \
    chmod 777 /docker_app/data

# Expose the port Django runs on
EXPOSE 8000

# Run migrations and load data from fixtures when the container starts
CMD python manage.py migrate && \
    python manage.py loaddata /docker_app/fixtures/* && \
    python manage.py runserver 0.0.0.0:8000
