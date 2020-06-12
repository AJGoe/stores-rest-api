
from werkzeug.security import safe_str_cmp # compares strings returns true if strigns are the same (here to avoid issues with python versions, different systems and servers)
from models.user import UserModel

# set-up database

## Function - authenticate user
# Given a username and a password > select correct user name from the list
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload): # unique to Flask JWT; payload is the content of the JWT Token > extract user
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
