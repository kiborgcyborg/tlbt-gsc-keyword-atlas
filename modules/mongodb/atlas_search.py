from pymongo import MongoClient
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv
import os


load_dotenv()

connection_string = os.getenv('MONGO_URI')
database = os.getenv('DB_NAME')
collection = os.getenv('COLLECTION_NAME')
mongo_atlas_search_index = os.getenv('MONGO_ATLAS_SEARCH_INDEX')
index = os.getenv('MONGO_ATLAS_SEARCH_INDEX')

class KeywordSearcher:
    def __init__(
            self, 
            connection_string: Optional[str] = connection_string, 
            database: Optional[str] = database, 
            collection: Optional[str] = collection,
            index: Optional[str] = index
            ):
        """
        Ініціалізація підключення до MongoDB
        
        Args:
            connection_string: MongoDB connection string
            database: Назва бази даних
            collection: Назва колекції
            index: Назва індексу Atlas Search
        
        Raises:
            ValueError: Якщо відсутні обов'язкові параметри підключення
        """
        # Перевірка наявності обов'язкових параметрів
        if not connection_string:
            raise ValueError("MongoDB connection string is required")
        if not database:
            raise ValueError("Database name is required")
        if not collection:
            raise ValueError("Collection name is required")
        if not index:
            raise ValueError("Search index name is required")
            
        self.client = MongoClient(connection_string)
        self.collection = self.client[database][collection]
        self.index = index
    

    def simple_search(
        self, 
        query: str, 
        min_score: float = 0.5,
        limit: int = 10,
        fuzzy_max_edits: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Простий пошук ключових слів
        """
        pipeline = [
            {
                "$search": {
                    "index": self.index,
                    "text": {
                        "query": query,
                        "path": "keyword",
                        "fuzzy": {
                            "maxEdits": fuzzy_max_edits
                        }
                    }
                }
            },
            {
                "$project": {
                    "keyword": 1,
                    "score": {"$meta": "searchScore"},
                    "_id": 0
                }
            },
            {
                "$match": {
                    "score": {"$gte": min_score}
                }
            },
            {
                "$limit": limit
            }
        ]
        
        return list(self.collection.aggregate(pipeline))