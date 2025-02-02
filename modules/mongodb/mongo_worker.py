from pymongo import MongoClient
from pymongo.operations import UpdateOne
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'))
db = client[os.getenv('DB_NAME')]
collection = db[os.getenv('COLLECTION_NAME')]

# Видаляємо старий індекс якщо є
collection.drop_indexes()

# Створюємо правильний індекс
collection.create_index([("keyword", 1)], unique=True)

def insert_gsc_data(dataset):
    try:
        bulk_ops = []
        for item in dataset:
            if not item["keys"]:  # Пропускаємо записи без дати
                continue
                
            doc = {
                "keyword": item["keys"][0],
                "clicks": item.get("clicks", 0),
                "impressions": item.get("impressions", 0),
                "ctr": item.get("ctr", 0),
                "position": item.get("position", 0)
            }
            
            bulk_ops.append(
                UpdateOne(
                    {"keyword": item["keys"][0]},
                    {"$set": doc},
                    upsert=True
                )
            )
            
        if bulk_ops:
            result = collection.bulk_write(bulk_ops)
            print(f"{1} ► Modified: {result.modified_count}, Upserted: {result.upserted_count}, nMatched {result.matched_count}")
            return True
            
    except Exception as e:
        print(f"Error: {e}")
        return False