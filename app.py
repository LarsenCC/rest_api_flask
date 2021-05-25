import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from db import db

app = Flask(__name__)

# where the DB is... it can be postgres, sqlite, mysql...
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')

# turn off the Flask SQLAlchemy tracker...
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.secret_key = "jose"
api = Api(app)

# new endpoint /auth, we send it a username and a password
jwt = JWT(app, authenticate, identity)

# we dont have to make the decorator ourselves
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")

# prevents from executing this line when importing app.py
# if we run this file, this will be main.
# if imported, it wil be app
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)  # nice debug page!

