import pandas as pd
import json
import csv
from pymongo import MongoClient

dbName = "myLibrary"
clientUrl = "mongodb://localhost:27017/"
client = MongoClient(clientUrl)
db = client[dbName]


def popolaDB(csvPath, collectionName):
    print("Popopolando " + collectionName)
    coll = db[collectionName]
    data = pd.read_csv(csvPath)
    payload = json.loads(data.to_json(orient='records'))
    coll.drop()
    coll.insert_many(payload)
    #print(coll.count())


def inizializzaDB():
    # GESTIONE CSV per le collection ATHLETE, EVENT, ACHIEVEMENT
    rootPath = "./dataset/"
    dataAE = pd.read_csv(rootPath + "processed_data.csv")

    # CREAZIONE CSV BOOKS
    print("*** INIZIO Creazione csv BOOKS_INFO ***")
    dfbook = dataAE[['isbn', 'book_title', 'book_author', 'year_of_publication','publisher','Category']].copy()  # Crea dataframe contenente solo le info sui libri
    dfbook = dfbook.drop_duplicates(['isbn'])
    dfbook.to_csv(rootPath + "books_info.csv", index=False)  # Converti dataframe in csv
    print("*** FINE Creazione csv BOOKS_INFO ***")


    print("*** INIZIO Creazione csv USERS_INFO ***")
    dfuser = dataAE[['user_id', 'age', 'city', 'country','state']].copy()  # Crea dataframe contenente solo le info sugli utenti
    dfuser = dfuser.drop_duplicates(['user_id'])
    dfuser.to_csv(rootPath + "users_info.csv", index=False)  # Converti dataframe in csv
    print("*** FINE Creazione csv USERS_INFO ***")

    print("*** INIZIO Creazione csv RATINGS_INFO ***")
    dfrating = dataAE[['user_id', 'isbn', 'rating']].copy()  # Crea dataframe contenente solo le info sui ratings
    dfrating.to_csv(rootPath + "ratings_info.csv", index=False)  # Converti dataframe in csv
    print("*** FINE Creazione csv RATINGS_INFO ***")
    
    
   # CARICAMENTO SU MONGODB
    print("**** Popolamento table Book ***")
    popolaDB(rootPath + "books_info.csv", "book")
    print("**** Fine Popolamento table Book ***")
    print("**** Popolamento table USER ***")
    popolaDB(rootPath + "users_info.csv", "user")
    print("**** FINE Popolamento table User ***")
    print("**** Popolamento table Rating ***")
    popolaDB(rootPath + "ratings_info.csv", "rating")
    print("**** FINE Popolamento table Rating ***")
'''
    creaIndici()

    # Incorpora ACHIEVEMENT in EVENT sotto forma di array
    db.athlete.update_many({}, {"$set": {"Achievements": []}})  # Aggiungi l'attributo Achievements ad Athletes
    firstHalfOfAchievements = db.achievement.find({"IDAthlete": {"$lte": 60000}}, {"_id": 0}).sort("IDAthlete", 1)
    secondHalfOfAchievements = db.achievement.find({"IDAthlete": {"$gt": 60000, "$lte": 120000}}, {"_id": 0}).sort(
        "IDAthlete", 1)
    thirdHalfOfAchievements = db.achievement.find({"IDAthlete": {"$gt": 120000}}, {"_id": 0}).sort("IDAthlete", 1)
    insertAchievement(firstHalfOfAchievements)
    print("inserito first")
    insertAchievement(secondHalfOfAchievements)
    print("inserito second")
    insertAchievement(thirdHalfOfAchievements)
    print("inserito third")

    db.achievement.drop()
    creaIndiciAchievements()


def insertAchievement(achievements):
    for a in achievements:
        db.athlete.update_one({"ID": a["IDAthlete"], "Age": a["AthleteAge"]},
                              {"$push": {
                                  "Achievements": {i: a[i] for i in a if
                                                   i != "IDAthlete" and i != "AthleteAge"}}})


def creaIndici():
    # Indici per Athlete
    db.athlete.create_index([("ID", 1)])
    db.athlete.create_index([("Team", 1)])
    db.athlete.create_index([("Age", 1)])
    db.athlete.create_index([("Sex", 1)])
    db.athlete.create_index([("Name", 1)])

    # Indici per Achievement
    db.achievement.create_index([("IDAthlete", 1)])
    db.achievement.create_index([("IDEvent", 1)])
    db.achievement.create_index([("Sport", 1)])
    db.achievement.create_index([("Medal", 1)])
    db.achievement.create_index([("AthleteAge", 1)])

    # Indici per Event
    db.event.create_index([("EventName", 1)])
    db.event.create_index([("Year", 1)])
    db.event.create_index([("City", 1)])
    db.event.create_index([("IDEvent", 1)])


def creaIndiciAchievements():
    # Indici per Achievement embedded in Athlete
    db.athlete.create_index([("Achievements.Medal", 1)])
    db.athlete.create_index([("Achievements.Sport", 1)])
    db.athlete.create_index([("Achievements.IDEvent", 1)])

'''
def checkInizializza():
    if dbName not in client.list_database_names():  # Se non trova il db, lo crea e carica il dataset
        inizializzaDB()
