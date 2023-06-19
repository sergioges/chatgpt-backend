from pymongo.mongo_client import MongoClient
import certifi
from os import getenv
from dotenv import load_dotenv

load_dotenv()
mongodb_access = getenv("MONGODB_ACCESS")
is_local = getenv("IS_LOCAL")

if is_local == "True":
    connection = MongoClient("mongodb://localhost")
else:
    connection = MongoClient(f"mongodb+srv://sergioges:{mongodb_access}@chatgpt-app.xqppbuf.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())

# client = MongoClient("mongodb://localhost:27017/")
# db = client["chatgptDB"]
# collection = db["user"]