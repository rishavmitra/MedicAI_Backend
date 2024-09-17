import os
import pymongo
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("MONGO_DB")

client = pymongo.MongoClient(url)

db = client['MedicAI']