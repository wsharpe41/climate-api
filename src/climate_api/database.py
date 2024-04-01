"""This module contains the database configuration for the application."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from kubernetes import client, config

#SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://postgres:{os.environ.get('pg_pass')}@localhost:5432/climate_api"

#engine = create_engine(
#    SQLALCHEMY_DATABASE_URL,
#)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()

# Load Kubernetes configuration
config.load_kube_config()

# Specify the namespace and secret name
namespace = "climate-api"
secret_name = "postgres-secret"

# Retrieve the PostgreSQL password from the Kubernetes secret
v1 = client.CoreV1Api()
secret = v1.read_namespaced_secret(name=secret_name, namespace=namespace)
pg_pass = secret.data["pg_pass"].decode("utf-8")

# Construct the database URL with the retrieved password
db_url = f"postgresql+psycopg2://postgres:{pg_pass}@localhost:5432/climate_api"

# Create the SQLAlchemy engine
engine = create_engine(db_url)

# Create a sessionmaker to create session objects
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative ORM models
Base = declarative_base()