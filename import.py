import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session,sessionmaker

link = "postgresql://cqrlmoqswiquqf:da8d2dcbe9d00c77ad09320c8eb86851b0243599c5b62fa8c280bbedf582b96f@ec2-52-87-107-83.compute-1.amazonaws.com:5432/d4n1i8iase18lm" 

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
  
