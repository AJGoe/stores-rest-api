from db import db

class UserModel(db.Model): # db.Model > tells the SQLAlchemy entity that these classes are things that we are saving to and retrieving from a database > creates that mapping between the db and these objects
    # tell SQLAlchemy the table name where these models are going to be stored
    __tablename__ = 'users'

    # What columns the table contains
    id = db.Column(db.Integer, primary_key = True) # id as the primary key is auto-incementing > created automatically > no need for def in init
    username = db.Column(db.String(80)) # limit size of username to 80 characters
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    # find user in the database, searching by the users username
    # def find_by_username(self, username):
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()  # SELECT * FROM users

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first() # id(=column name) = _id(=argument name > see: def find_by_id(cls, _id))
