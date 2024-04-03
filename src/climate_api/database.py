"""This module contains the database configuration for the application."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#from kubernetes import client, config
import os

database_url = os.environ.get("HEROKU_DATABASE_URL")
database_url = database_url.replace("postgres://", "postgresql://", 1)
if not database_url:
    raise ValueError("HEROKU_DATABASE_URL environment variable is not set.")

engine = create_engine(
    database_url,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Load Kubernetes configuration
# config.load_kube_config()

# Specify the namespace and secret name
# namespace = "climate-api"
# secret_name = "postgres-secret"

# Retrieve the PostgreSQL password from the Kubernetes secret
# v1 = client.CoreV1Api()
# secret = v1.read_namespaced_secret(name=secret_name, namespace=namespace)
# pg_pass = secret.data["pg_pass"].decode("utf-8")

# Construct the database URL with the retrieved password
# db_url = f"postgresql+psycopg2://postgres:{pg_pass}@localhost:5432/climate_api"

# Create the SQLAlchemy engine
#engine = create_engine(db_url)

# Create a sessionmaker to create session objects
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative ORM models
#Base = declarative_base()