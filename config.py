import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO: create a database called Academe and replace the name Fyyur with Academe.
SQLALCHEMY_DATABASE_URI = 'postgresql://lujiawen@localhost:5432/Fyyur'
