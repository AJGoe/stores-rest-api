from db import db


class StoreModel(db.Model): # db.Model > tells the SQLAlchemy entity that these classes are things that we are saving to and retrieving from a database

    # table name:
    __tablename__ = 'stores'

    # columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))

    # Back-reference:
    # allows the store to see which items are in the items database/tales with a store_id equal to its own id
    items = db.relationship('ItemModel',lazy='dynamic') # SQLAlchemy > there is a relationship with ItemModel > what's the relationship? > item.py > finds store_id >> there are one or more items related to that store >> a list of item models; laz='dynamic': self.items no longer is a list of items > now it is a query builder that has the ability to look into the items table > with .all() you can now retrieve all the items in that table

    def __init__(self, name):
        self.name = name

    # return a JSON representation of the model (basically a dictionary)
    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1; LIMIT 1 returrs the first row only; returns item model object that has self.name and self.price

    def save_to_db(self): # with SQLAlchemy: saves and updates model to the database ("up-serting")
        db.session.add(self) # session > a collection of objects that we're going to write to the db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
