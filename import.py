from models import *
from application import *
import csv

def main():
    with  open("books.csv") as f:
        freader = csv.reader(f)

        next(freader)
        for line in freader:
            book = Books(isbn=line[0],title=line[1],
            author=line[2],pub_year=line[3])
            db.session.add(book)

    db.session.commit()


if __name__=="__main__":
    with app.app_context():
        main()
