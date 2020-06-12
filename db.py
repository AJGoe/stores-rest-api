from flask_sqlalchemy import SQLAlchemy


# SQLAlchemy object > links to the flask-app > looks at all the object that we tell it to > allows us to map those objects to rows in a database
# e.g. when we create an item model object that has a column called name and a column called price > allows to put that object into a database
# Saving the objects properties into a db

db = SQLAlchemy()
