from app import app
from db import db


# only creates tables that it sees!
@app.before_first_request
def create_tables():
    db.create_all()


db.init_app(app)
# app.run(port=5000, debug=True)  # nice debug page!