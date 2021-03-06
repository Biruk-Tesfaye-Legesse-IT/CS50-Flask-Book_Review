import os

from flask import Flask, session,render_template,request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import json

app = Flask(__name__)

# Check for environment variable
# if not os.getenv("postgresql://cqrlmoqswiquqf:da8d2dcbe9d00c77ad09320c8eb86851b0243599c5b62fa8c280bbedf582b96f@ec2-52-87-107-83.compute-1.amazonaws.com:5432/d4n1i8iase18lm"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine("postgresql://cqrlmoqswiquqf:da8d2dcbe9d00c77ad09320c8eb86851b0243599c5b62fa8c280bbedf582b96f@ec2-52-87-107-83.compute-1.amazonaws.com:5432/d4n1i8iase18lm")
db = scoped_session(sessionmaker(bind=engine))


# ===================================================== Default ===========================================================================


@app.route("/")
def index():
    return render_template('index.html')

# ===================================================== Login ===========================================================================



@app.route("/login",methods=["GET","POST"])
def login():
	username = request.form.get("username")
	password = request.form.get("password")


	if request.method == "POST":
		name_query = db.execute("SELECT username FROM register WHERE username=:username",{"username":username}).fetchone()
		db.commit()
		login_query = db.execute("SELECT username,password FROM register WHERE username=:username AND password=:password",{"username":username,"password":password}).fetchone()
		db.commit()
		session["username"] = username
		if login_query:
			return render_template("home.html",name=name_query)
		else:
			username_error ="⚠️ Username or Password Incorrect"
			return render_template("index.html",username_error=username_error)
	else:
		return render_template("index.html") 


# ===================================================== Register ===========================================================================


@app.route("/register",methods=["GET","POST"])
def register():
	name = request.form.get("name")
	username = request.form.get("username")
	email = request.form.get("email")
	password = request.form.get("password")
	confirm = request.form.get("confirm_password")
	
	
	if request.method== "POST":
	
		username_validity_query = db.execute("SELECT username FROM register WHERE username=:username",{"username":username}).fetchone()
		if username_validity_query is not None:
			print("Username Already Existed")
			username_error = "⚠️ Username Already Existed"
			return render_template("index.html",username_error=username_error)

		elif password != confirm:
			print("Password doesn't match!")
			username_error = "⚠️ Password doesn't match"
			return render_template("index.html",username_error=username_error)
    			
		
		else:
			register_query = db.execute("INSERT INTO register (name,username,email,password) VALUES  (:name,:username,:email,:password) ",{"name":name,"username":username,"email":email,"password":password})
			if register_query:
				db.commit()
				print(password)
				print(confirm)
				success = name + " You can Login Now"
				return render_template("index.html",success=success)

	else:
		return render_template("index.html")


# ===================================================== Logout ===========================================================================



@app.route("/logout")
def logout():
	session.clear()
	logout_message = "You Have Successfully Logout"
	return render_template("index.html",logout_message=logout_message)


# ===================================================== Search Results ===========================================================================



@app.route("/result",methods=["GET","POST"])
def result():
	search = request.form.get("search")

	if request.method == "POST":
		search_query=db.execute("SELECT * FROM books WHERE author iLIKE '%"+search+"%' OR title iLIKE '%"+search+"%' OR isbn iLIKE '%"+search+"%'").fetchall()
		
		#search_query = db.execute("SELECT * FROM books WHERE title=:title OR isbn=:isbn OR author=:author",{"title":search,"isbn":search,"author":search}).fetchall()
		db.commit()
		if search_query:
			results = len(search_query)
			return render_template("search.html",search_query=search_query,results=results)
		elif len(search_query) == 0:
			search_error = search + " Not Found"
			return render_template("home.html",search_error=search_error)
	else:
		return render_template("index.html")



# ===================================================== Deatails ===========================================================================


@app.route("/bookpage/<string:isbn>",methods=["GET","POST"])
def details(isbn):
	
	request = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vguAWxSWysSfur23uFOPg", "isbns": isbn})
	

	result_query = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
	average_rating=request.json()['books'][0]['average_rating']
	work_ratings_count=request.json()['books'][0]['work_ratings_count']
	result = db.execute("SELECT * from review where isbn=:isbn",{"isbn":isbn}).fetchall()
	print(result)
	return render_template("details.html",result_query=result_query,average=average_rating,work_ratings_count=work_ratings_count,reviews=result)

# ===================================================== Review ===========================================================================

@app.route("/review/<string:isbn>",methods=["GET","POST"])
def review(isbn):
	username=session['username']
	rating = request.form.get("rating")
	review = request.form.get("review")
 
	
	print(isbn)
	print(session['username'])
	dupp = db.execute("SELECT * FROM review WHERE isbn=:isbn AND username=:username",{"isbn":isbn,"username":session['username']})
 

 

 
	if request.method == "POST":
		print(dupp)
		# if dupp == None:
		if review != None and rating != None:
			print("passed")
			success = db.execute("INSERT INTO review (username,isbn,review,rating) VALUES (:username,:isbn,:review,:rating)",{"username":str(session['username']),"isbn":isbn,"review":review,"rating":rating})
			db.commit()
			if success:
				success_message = "Your review has been added. Thank you for your feedback!"
				return render_template("details.html",success_message=success_message) 
				 
			else:
				error_message="Something went wrong"
				return render_template("details.html",error_message=error_message) 
				
		else:
			error_message="Please enter your Rating and review!"
   			# return redirect("details", error_message=error_message)
  
			return render_template("details.html",error_message=error_message) 
			 
		# else:
		# 	return render_template("details.html",review_error="Your Rating And Review Already Exist")
	else:
		return render_template("details.html") 

# ===================================================== API ===========================================================================



@app.route("/api/<string:isbn>",methods=["GET","POST"])


def api(isbn):
    	# request = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "vguAWxSWysSfur23uFOPg", "isbns": isbn})
	result_query = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
	# average_rating=request.json()['books'][0]['averinst__tables.age_rating']
	# work_ratings_count=request.json()['books'][0]['work_ratings_count']
	api_query = db.execute("SELECT * FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
	if api_query == None:
		return render_template("error.html")
	data = {"title" : api_query.title,"author": api_query.author,"year":api_query.year,"isbn":api_query.isbn}
	dump = json.dumps(data)
	return render_template("api.html",api=dump)





# ===================================================== Running Function ===========================================================================



if __name__=="__main__":
    app.run(debug=True)