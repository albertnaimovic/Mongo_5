# Create an income tax calculator:
# - Generate at least 500 documents , with fields: name, surname, date of birth , age (determined from date of birth), anual salary before tax (EUR, round to 2 numbers after comma)
# - Create a CLI application that would let us get first 10 people from database within the age bracket [min_age, max_age]
# - Those people name surname and age should be shown as an option to choose.
# - When one of ten options is chosen, there should be calculated tax return (it should be created a document as a tax card, values taken from database). Lets say GPM tax is 20% and HealtTax is 15% from 90% of the income left after GPM deduction.
# - The final values should be show and wrriten to database (like a generated data and taxes paid, take home pay etc.) and portrayed in a web page (use flask and docker, show the url were to click )


from bson import ObjectId
import click
from mongo_crud import MongoCRUD
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import (
    PyMongoError,
    ConnectionFailure,
    ConfigurationError,
    CollectionInvalid,
)
from typing import Dict, List, Optional


class MongoCRUD:
    def __init__(
        self, host: str, port: int, database_name: str, collection_name: str
    ) -> None:
        self.host = host
        self.port = port
        self.database_name = database_name
        try:
            self.collection = self.__connect_to_mongodb()[collection_name]
        except CollectionInvalid as err:
            print(f"Collection creation error: {err}")

    def __connect_to_mongodb(self) -> Optional[Database]:
        try:
            client = MongoClient(self.host, self.port)
            database = client[self.database_name]
            return database
        except ConnectionFailure as err:
            print(f"Connection failure: {err}")
        except ConfigurationError as err:
            print(f"Configuration error: {err}")

    def find_documents(self, query: Dict) -> Optional[List[Dict]]:
        try:
            documents = self.collection.find(query)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def find_10_documents(self, query: Dict) -> Optional[List[Dict]]:
        try:
            documents = self.collection.find(query).limit(10)
            return list(documents)
        except PyMongoError as err:
            print(f"An error occured: {err}")

    def update_one_document(self, query: Dict, update: Dict) -> Optional[int]:
        try:
            result = self.collection.update_one(query, {"$set": update})
            return result.modified_count
        except PyMongoError as err:
            print(f"An error occured: {err}")


database = MongoCRUD(
    host="localhost",
    port=27017,
    database_name="tax_calculator",
    collection_name="persons",
)


@click.command()
@click.option("--min_age", type=int, prompt="Enter min age", help="Min age")
@click.option("--max_age", type=int, prompt="Enter max age", help="Max age")
def cli_app(min_age: int, max_age: int) -> Optional[str]:
    persons = database.find_10_documents({"age": {"$gte": min_age, "$lt": max_age}})
    if persons:
        counter = 1
        for person in persons:
            click.echo(
                f"{counter}. {person['name']} {person['surname']}, Age: {person['age']}"
            )
            counter += 1
    else:
        print("There is no people in the given age range...")
        return

    selected_number = click.prompt(
        text="Enter number of person from the list", type=int
    )
    selected_person = persons[selected_number - 1]
    click.echo(
        f"Selected person: {selected_person['name']} {selected_person['surname']} {selected_person['_id']}"
    )
    return selected_person["_id"]


def get_tax_return(person_id: str) -> None:
    person = database.find_documents({"_id": person_id})[0]
    anual_salary = person["anual_salary"]
    gpm = round(anual_salary * 0.2, 2)
    health_tax = round(((anual_salary * 0.8) * 0.9) * 0.15, 2)
    income_after_taxes = round(anual_salary - gpm - health_tax, 2)

    update = {
        "gpm": gpm,
        "health_tax": health_tax,
        "icome_after_taxes": income_after_taxes,
    }
    database.update_one_document({"_id": person_id}, update=update)
    person = database.find_documents({"_id": person_id})
    print(person)


get_tax_return(cli_app())

# https://github.com/WTR-GITHUB/MongoDB_Lesons/tree/main/income_calculator
