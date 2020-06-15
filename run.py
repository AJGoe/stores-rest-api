from app import app
from db import db

db.init_app(app)

# Flask decorator
@ app.before_first_request # runs the method below before the first request into this app is made
def create_tables():
    db.create_all()
