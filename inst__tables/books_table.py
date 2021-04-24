from flask import Flask
from books_model import *
link = ""

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://cqrlmoqswiquqf:da8d2dcbe9d00c77ad09320c8eb86851b0243599c5b62fa8c280bbedf582b96f@ec2-52-87-107-83.compute-1.amazonaws.com:5432/d4n1i8iase18lm"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)

def index():
    db.create_all()
    print ("Created")

if __name__ == "__main__":
	with app.app_context():
		index()
