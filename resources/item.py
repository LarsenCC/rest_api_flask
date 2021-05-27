import sqlite3
from flask_restful import Resource, reqparse
# from flask_jwt import jwt_required
from flask_jwt_extended import jwt_required
from models.item import ItemModel


# working with resources... Every resource is a CLASS!
# inherit from Resource
# only keep the REST methods! Others should be stored in models...
class Item(Resource):

    # class parser
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id!")

    @jwt_required  # this will tell us to first auth the request!
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200
        return {'message': 'Item not found'}, 404

    @jwt_required
    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': 'Item already exists'}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occured inserting the item.'}, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        """connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()"""
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deleted'}

    @jwt_required
    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = ItemModel(name, **data)

        item.save_to_db()

        return item.json(), 201


class ItemList(Resource):
    @jwt_required
    def get(self):
        # make queries only from the Model, not from Resource, makes it too heavy!
        return {'item': [item.json() for item in ItemModel.find_all()]}
        # return {'item': list(map(lambda x: x.json(), ItemModel.query.all()))}

    """@classmethod
    def get_all_items(cls):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        rows = result.fetchall()
        print(rows)
        connection.close()

        if len(rows) != 0:
            items = [{'item': item[0], 'price': item[1]} for item in rows]
            return {'item': items}"""


