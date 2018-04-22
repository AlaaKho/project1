import os

from flask import Flask, session, request, render_template, url_for, redirect
from flask_session import Session
from models import *
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from sqlalchemy import or_, and_
from tempfile import mkdtemp
from flask_migrate import Migrate

app = Flask(__name__)

#configure SQLAlchemy database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

db.init_app(app)
Session(app)
migrate = Migrate(app, db)


# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")



@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

        #check proper usage
        if not request.form.get("field"):
            return render_template("error.html", message="must fill in the required fields.")

        #search
        field = request.form.get("field")

        matches = Books.query.filter(or_(Books.isbn.ilike(f"%{field}%"),
            Books.title.ilike(f"%{field}%"), Books.author.ilike(f"%{field}%"))).all()

        #if no match was found
        if matches != []:
            return render_template("index.html", matches=matches)
        else:
            return render_template("index.html", message="No possible matches")
    else:
        return render_template("index.html")


@app.route("/book/<string:isbn>", methods=["GET", "POST"])
@login_required
def book(isbn):
    book = Books.query.get(isbn)

    #check if book exists
    if book is None:
        return render_template("error.html", message="no such book")

    #POST request
    if request.method == "post":
        #if the user has submitted a review for this book
        #get all reviews for this book
        #reviews = book.review
        #for review in
        pass
    #GET request
    else:
        return render_template("book.html", book=book )



@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    if request.method == "POST":
        print(f"username field is{request.form.get('username')}")
        if not request.form.get("username") or not request.form.get("password"):
            return render_template("error.html", message="Please fill in the required fields")

        #check if the user exists
        user = Users.query.filter_by(name=request.form.get("username")).first()

        print(f"query of the user is{user}")
        #check with username
        if user is None:
            return render_template("error.html", message="no user with these credentials, Please register first!")

        #check with password
        if  not check_password_hash(user.password, request.form.get("password")):
            return render_template("error.html", message="Please provide a valid password!")

        session["user_id"] = user.id
        return redirect(url_for("index"))

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    #forget logined user
    session.clear()
    return redirect(url_for("index"))



@app.route("/register", methods=["POST", "GET"])
def register():

    session.clear()

    if request.method == "POST":

        #check for valid usage if any of the fields is None
        if not request.form.get("username")  or not request.form.get("password"):
            return render_template("error.html", message="Please fill in the required fields")

        #check if user exists
        user = Users.query.filter_by(name=request.form.get("username")).first()

        if user is not None:
            return render_template("error.html", message="username already exists")

        else:
            #encrypte password
            password = generate_password_hash(request.form.get("password"))
            #create user
            user = Users(name=request.form.get("username"), password=password)

            db.session.add(user)
            db.session.commit()

            session["user_id"] = user.id
            return redirect(url_for("search"))
    else:
        return render_template("register.html")
