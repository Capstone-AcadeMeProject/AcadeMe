import os
SECRET_KEY = 'secret'
SESSION_TYPE = 'filesystem'
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO: create a database called Academe and replace the name Fyyur with Academe.
# SQLALCHEMY_DATABASE_URI = 'postgresql://myuser@127.0.0.1:5432/academe'


# Get configuration from environment when using vagrant
DATABASE_URI = os.getenv(
    "DATABASE_URI",
    "postgresql://postgres:postgres@127.0.0.1:5432/postgres"
)

# # Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False