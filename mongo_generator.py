import datetime
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from typing import Dict
import random, names
from faker import Faker

fake = Faker()


def connect_to_mongodb(host: str, port: int, db_name: str) -> Database:
    client = MongoClient(host, port)
    database = client[db_name]
    return database


def insert_document(collection: Collection, document: Dict) -> str:
    result = collection.insert_one(document)
    return str(result.inserted_id)


if __name__ == "__main__":
    mongodb_host = "localhost"
    mongodb_port = 27017
    database_name = "hangman"
    collection_name = "random_words"

    db = connect_to_mongodb(mongodb_host, mongodb_port, database_name)

    collection = db[collection_name]

    for _ in range(500):
        birthdate = fake.date_between(start_date="-65y", end_date="-18y")
        age_days = datetime.date.today() - birthdate
        age = round(age_days.days / 365.2425)
        document = {
            "name": names.get_first_name(),
            "surname": names.get_last_name(),
            "birthdate": birthdate.strftime("%Y-%m-%d"),
            "age": age,
            "anual_salary": random.randint(12000, 120000),
        }

        inserted_id = insert_document(collection, document)
        print(document)


# Generate at least 500 documents , with fields: name, surname, date of birth ,
# age (determined from date of birth), anual salary before tax (EUR, round to 2 numbers after comma)
