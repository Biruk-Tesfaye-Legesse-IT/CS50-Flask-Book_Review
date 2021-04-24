import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

link = "postgresql://postgres:root@localhost/book_store" 

engine = create_engine(link)
db = scoped_session(sessionmaker(bind=engine))


def main():
   fopen = open("books.csv")

   reader = csv.reader(fopen)

   for isbn,tit,auth,yr in reader:
        db.execute("INSERT INTO books (title,author,isbn,year) VALUES (:title,:author,:isbn,:year)",{"title":tit,"author":auth,"isbn":isbn,"year":yr})
        db.commit()
        print (tit , auth , isbn , yr)


if __name__ == "__main__":
  main()
  
