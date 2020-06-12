from db import db


# ItemModel: internal representation > has to contain the properties of an item as object properties
class ItemModel(db.Model): # db.Model > tells the SQLAlchemy entity that these classes are things that we are saving to and retrieving from a database

    # table name:
    __tablename__ = 'items'

    # columns
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision = 2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # ForeignKey: id in store is a primary_key -> the store_id in item is a foreign_key!; in relational db's, with foreign_key references one cannot delete the object without deleting the items referencing it first > degree of security
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    # return a JSON representation of the model (basically a dictionary)
    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1; LIMIT 1 returrs the first row only; returns item model object that has self.name and self.price

    def save_to_db(self): # with SQLAlchemy: saves and updates model to the database ("up-serting")
        db.session.add(self) # session > a collection of objects that we're going to write to the db
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
