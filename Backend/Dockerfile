# Use an official Python base image
FROM python:3.11-slim

# Install build tools and ODBC development libraries
RUN apt-get update && apt-get install -y build-essential unixodbc-dev curl gnupg2 && \
    # Install Microsoft ODBC Driver 17 for SQL Server
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Upgrade pip to ensure pre-built wheels are used
RUN pip install --upgrade pip

# Install uv
RUN pip install uv

# Set the working directory in the container
WORKDIR /app

# Copy the project files
COPY . .

# Sync the dependencies (use system Python)
RUN uv sync --python $(which python3)

# Expose the port
EXPOSE 8000

# Run the command to start the server using uv's virtual environment
CMD [".venv/bin/uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]