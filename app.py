import os

from flask import Flask
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager

from security import authenticate, identity
from resources.user import UserRegister, User, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)

# where the DB is... it can be postgres, sqlite, mysql...


uri = os.environ.get('DATABASE_URL', 'sqlite:///data.db')  # or other relevant config var
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
# rest of connection code using the connection string `uri`
app.config['SQLALCHEMY_DATABASE_URI'] = uri

# turn off the Flask SQLAlchemy tracker...
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Get the actuall error messages from the API, not server 500...
app.config['PROPAGATE_EXCEPTIONS'] = True

app.secret_key = "larsen" # app.config['JWT_SECRET_KEY']
api = Api(app)

# new endpoint /auth, we send it a username and a password
# jwt = JWT(app, authenticate, identity)

# JWT extended!
jwt = JWTManager(app) # not creating /auth endpoint!


# we dont have to make the decorator ourselves
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/user/<int:user_id>")

api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")

# prevents from executing this line when importing app.py
# if we run this file, this will be main.
# if imported, it wil be app
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)  # nice debug page!

