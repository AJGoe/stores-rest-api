from flask_restful import Resource, reqparse# Resource: sth. that the API represents, usually mapped into database tables
from flask_jwt import jwt_required
from models.item import ItemModel

# Resources:
class Item(Resource): # class Students that inherits from the class Resources
    # initialises a new object > used to parse the request
    # the parser now belongs to the item class itself and not to a method or one specific item resource
    parser = reqparse.RequestParser()
    # define arguments - the parsing > checks JSON payload (or form payloads)
    parser.add_argument('price',
        type=float,
        required=True, # to make sure that no request can come through with no price
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True, # to make sure that no request can come through with no price
        help="Every item needs a store id."
    )

    @jwt_required() # decorator > you have to authenticate before you can use the get method
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json() # returns the item itself
        return {'message': 'Item not found'}, 400 # no else statement needed, because the line above breaks flow with return

    def post(self, name): # same set of parameters as Get
        if ItemModel.find_by_name(name):
            return {'message': "An item with the name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data) # data['price']: access the price key of the data dictionary; **data: data['price'], data['store_id']

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500 # 500: internal server error

        return item.json(), 201 # 201: http status for creating; item form above is in JSON format! as we cannot return an object here

    def delete(self, name): # the name will be deleted
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': 'Item deleted'}

        return {'message': 'Item not found.'}, 404

    def put(self, name):
        data = Item.parser.parse_args() # parses the arguments that come through the JSON payload > puts the valid args (here only: price) in data < other args will be deleted
        # print(data['another']) # a field inside data that have not been added an argument for >> output key error (data does not have a key "another")

        item = ItemModel.find_by_name(name)

        if item: # if the item is none, meaning not found in the database
            item.price = data['price']
        else:
            item = ItemModel(name, **data) # data['price'], data['store_id']

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        # return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))} # only use map if also programming in other languages or if working with people programming in other languages,  too
        return {'items': [item.json() for item in ItemModel.query.all()]} # .all(): returns all objects in the db;
