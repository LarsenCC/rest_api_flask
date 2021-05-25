from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!")

    def post(self):
        data = UserRegister.parser.parse_args()

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
