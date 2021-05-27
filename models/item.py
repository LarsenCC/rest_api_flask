from db import db


# resources should only contain methods that the API interacts with!
class ItemModel(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    # get id from stores (cannot delete store!) :D
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    # basically join...
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {
            'id': self.id, 
            'name': self.name, 
            'price': self.price, 
            'store_id': self.store_id
            }

    @classmethod
    def find_by_name(cls, name):
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return cls(*row)"""

        # SQLAlchemy
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()"""

        # SQLAlchemy
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        # SQLAlchemy
        db.session.delete(self)
        db.session.commit()
