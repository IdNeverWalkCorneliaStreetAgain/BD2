from matplotlib import pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from load_db import db

#BOOK
#Query inserimento libro
def insertBook(book):
    return db.book.insert_one({"isbn": book["isbn"], "book_title": book["titolo"], "book_author":book["autore"], "year_of_publication": book["year"], 
                                "publisher": book["publisher"], "Category": book["category"]})

#Query modifica libro
def updateBook(book):
    return db.book.update_one({"isbn": book["isbn"]},
                        {"$set": {"book_title": book["titolo"], "book_author":book["autore"], "year_of_publication": book["year"], 
                                "publisher": book["publisher"], "Category": book["category"]}})

#Query cancellazione libro
def deleteBook(isbn):
    return db.book.delete_one({"isbn": isbn})

def checkBook(isbnBook):
    found = db.book.find_one({"isbn": isbnBook})
    return found

#RATING
#Query inserimento rating
def insertRating(rating):
    return db.rating.insert_one({"user_id": rating["user_id"], "isbn": rating["isbn"], "rating":rating["rating"]})

#Query modifica rating
def updateRating(rating):
    return db.rating.update_one({"isbn": rating["isbn"],"user_id": rating["user_id"]},
                        {"$set": {"rating":rating["rating"]}})

#Query cancellazione rating
def deleteRatingIsbn(isbn):
     print(isbn)
     return db.rating.delete_many({"isbn": isbn})

def deleteRatingIsbnEUtente(id_utente,isbn):
    print(isbn)
    print(id_utente)
    return db.rating.delete_many({"user_id": id_utente,"isbn": isbn})

def deleteRatingUtente(id_utente):
    return db.rating.delete_many({"user_id": id_utente})

def checkUserRating(id_utente):
    found = db.rating.find_one({"user_id": id_utente})
    return found

def checkIsbnRating(isbnB):
    found = db.rating.find_one({"isbn": isbnB})
    return found

#USER
#Query inserimento utente
def insertUser(user):
    return db.user.insert_one({"user_id": user["user_id"], "age": user["eta"], "city":user["citta"], "country": user["nazione"], 
                                "state": user["stato"]})

#Query modifica utente
def updateUser(user):
    return db.user.update_one({"user_id": user["user_id"]},
                        {"$set": {"age": user["eta"], "city":user["citta"], "country": user["nazione"], 
                                "state": user["stato"]}})

#Query cancellazione utente
def deleteUser(user_id):
    return db.user.delete_one({"user_id": user_id})

def checkUser(idUser):
    found = db.user.find_one({"user_id": idUser})
    return found
