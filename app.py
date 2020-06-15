from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister

from db import db

from resources.item import Item, ItemList

from resources.store import Store, StoreList


app = Flask(__name__)
app.secret_key = 'yves' # keep secret and secure; do not publish with code

# tell SQLAlchemy where to find the data.db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #  The SQLAlchemy db is at the root folder of the project

# specify a config property > turns off the flask SQLAlchemy modification tracker (it does not turn off the SQLAlchemy modification tracker which is better)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app) # allow to add the resources to it
# The API works with resources and every resource has to be a class

# initialising the JWT object >
jwt = JWT(app, authenticate, identity) # /auth; uses app + identity functions > to allow the authentification of the users
# JWT creates a new endpoint >/auth > when called, we send it a username + a password > JWT extension gets that username + password > sends it to the authenticate function > find the correct user object > compare password to the one received through the auth endpoint > if match > return user > becomes sort of the identity
# auth endpoint > returns JW token > send it with the next request > JWT calls the identity function > gets user_id > gets the correct user
# if the JWT token is valid > user authenticated


# Tell App that the resource Item is accessible via the API
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register') # when we execute a post request to /register > calls UserRegister > calls post method

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True) # debug=True > error message > html page with errors
