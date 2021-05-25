import sqlite3
from db import db


# internal representation of an entity. Resources = external...
class UserModel(db.Model):
    __tablename__ = 'users'

    # must match the columns in __init__
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):  # we dont use self, but class
        """# init connection and cursor
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        # always in a form of a tuple!!!!
        result = cursor.execute(query, (username,))
        row = result.fetchone()  # returns None if no rows
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)  # it matches
        else:
            user = None

        connection.close()
        return user"""

        # SQLAlchemy
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):  # we dont use self, but class
        """# init connection and cursor
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        # always in a form of a tuple!!!!
        result = cursor.execute(query, (_id,))
        row = result.fetchone()  # returns None if no rows
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)  # it matches
        else:
            user = None

        connection.close()
        return user"""

        # SQLAlchemy
        return cls.query.filter_by(id=_id).first()
