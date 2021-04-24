from flask import Flask
from inst__tables.books_model import *
link = ""

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:root@localhost/book_store"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)

def index():
    db.create_all()
    print ("Created")

if __name__ == "__main__":
	with app.app_context():
		index()
