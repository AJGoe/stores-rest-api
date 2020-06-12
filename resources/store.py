from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    # Return a specific store
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json() # ,200 > default!
        return {'message': 'Store not found'}, 404 # tuple of dictionary and code > Flask and Flask-SQLAlchemy > return the dict in the body and the code in the code status

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store.'}, 500 # 500: internal server error > not the users fault, not sure what caused the error

        return store.json(), 201 # 201: store has been created

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}



class StoreList(Resource):
    def get(self):
        # return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}
        return {'stores': [store.json() for store in StoreModel.query.all()]}
