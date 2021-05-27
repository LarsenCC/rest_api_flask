from models.user import UserModel

# this is done in User class!
# username_mapping = {user.username: user for user in users}
# id_mapping = {user.id: user for user in users}


# check if username and password match
def authenticate(username, password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user


# JWT returns a payload with user identity!
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
