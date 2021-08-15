from pymongo import MongoClient
from decouple import config
import copy


DB_HOST = config("DB_HOST", default="localhost")
DB_PORT = config("DB_PORT", default="27017")

client = MongoClient(host=DB_HOST, port=int(DB_PORT))
db = client.approved_candidates


def create(data):
    col = db['candidates']
    col.drop()
    db.candidates.insert_many(copy.deepcopy(data))
