from flask import Flask
from mongo_crud import MongoCRUD
from bson import ObjectId

app = Flask(__name__)

database = MongoCRUD(
    host="localhost",
    port=27017,
    database_name="tax_calculator",
    collection_name="persons",
)


@app.route("/")
def home():
    return "<h1>Enter person ID in link...</h1>"


@app.route(f"/<person_id>")
def user(person_id):
    person = database.find_documents({"_id": ObjectId(person_id)})
    return person


if __name__ == "__main__":
    app.run()
