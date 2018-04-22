from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)




class Books(db.Model):

    __tablename__ = "books"
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    pub_year = db.Column(db.String, nullable=False)
    review = db.relationship("Reviews", backref="book", lazy=True)


class Reviews(db.Model):

    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    opinion = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_isbn = db.Column(db.String, db.ForeignKey("books.isbn"), nullable=False)
