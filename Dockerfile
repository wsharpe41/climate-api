# Use the official Python image as base
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

WORKDIR /app/src/

# Install hatch for managing dependencies
RUN pip install alembic sqlalchemy fastapi pydantic uvicorn psycopg2 kubernetes

# Expose the port
EXPOSE 5000

# Command to run API
CMD ["uvicorn", "climate_api.main:app", "--host", "0.0.0.0", "--port", "5000"]
