from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import (
    create_refresh_token, 
    create_access_token, 
    get_jwt_identity,
    jwt_required,
    get_jwt
)
from blacklist import BLACKLIST


# _varname is a sign that this is a private variable
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!")
_user_parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be left blank!")


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        # check if username already exists!
        if UserModel.find_by_username(data['username']):
            return {'message': "Username already exists. Pick another one!"}, 400

        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # insert new user
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()"""

        # because we have a parser and we ALWAYS get username and password
        user = UserModel(**data)
        user.save_to_db()

        return {'message': "User created successfully."}, 201


class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': f'User with id={user_id} not found'}, 404

        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': f'User with id={user_id} not found'}, 404

        user.delete_from_db()
        return {'message': f'User with id={user_id} deleted'}, 200


class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        # get data form parser
        data = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data['username'])

        # check password
        # this is what the 'authenticate()' function used to do
        if user and user.password == data['password']:
            # create access token
            # identity= is what the 'identity()' function used to do
            access_token = create_access_token(identity=user.id, fresh=True) # NOT fresh
             # create a refresh token!
            refresh_token = create_refresh_token(user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {'message': 'Invalid credentials.'}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        # jwt id...
        jti = get_jwt()["jti"]
        BLACKLIST.add(jti)
        return {'message': 'Successfully logged out.'}


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False) # NOT fresh
        return {'access_token': new_token}, 200