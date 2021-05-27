import os

from flask import Flask, jsonify
from flask_restful import Api
# from flask_jwt import JWT
from flask_jwt_extended import JWTManager
# https://flask-jwt-extended.readthedocs.io/en/stable/api/

# from security import authenticate, identity
from resources.user import (
    UserRegister, 
    User, 
    UserLogin, 
    TokenRefresh,
    UserLogout
    )
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

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

# enable blacklists for access and refresh tokens!
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

app.secret_key = "larsen" # app.config['JWT_SECRET_KEY']
api = Api(app)

# new endpoint /auth, we send it a username and a password
# jwt = JWT(app, authenticate, identity)

# JWT extended!
jwt = JWTManager(app) # not creating /auth endpoint!


# everytime we create a token, add something
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    # value of user id in identity
    print(identity)
    if identity == 1: # instead of hardcoding, use from DB instead!
        return {'is_admin': True}
    return {'is_admin': False}


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(header, payload):
    print(header, payload)
    # check if user is on blacklist/logged out
    return payload['jti'] in BLACKLIST


# This decorator sets the callback function for returning a custom 
# response when an expired JWT is encountered.
@jwt.expired_token_loader
def expired_token_callback(header, payload):
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


# This decorator sets the callback function for returning a custom response 
# when a valid and non-fresh token is used on an endpoint that is marked as fresh=True.
@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(header, payload):
    print(args)
    return jsonify({
        'description': 'This token is not fresh. Log in again to gain fresh token.',
        'error': 'needs_fresh_token'
    }), 401


# This decorator sets the callback function for returning a 
# custom response when an invalid JWT is encountered.
@jwt.invalid_token_loader
def invalid_token_callback(header, payload):
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


# This decorator sets the callback function for returning 
# a custom response when a revoked token is encountered.
@jwt.revoked_token_loader
def revoked_token_callback(header, payload):
    return jsonify({
        'description': 'The token has been revoked. You logged out.',
        'error': 'revoked_token'
    }), 401


# we dont have to make the decorator ourselves
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(User, "/user/<int:user_id>")

# user Resources
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")


# prevents from executing this line when importing app.py
# if we run this file, this will be main.
# if imported, it wil be app
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)  # nice debug page!

