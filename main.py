import os
from dotenv import load_dotenv
from modules.gsc.gsc_worker import get_gsc_data_16m
from modules.mongodb.mongo_worker import insert_gsc_data
from modules.mongodb.atlas_search import KeywordSearcher

def main():
    # # Load environment variables from .env file
    # load_dotenv()
    # gsc_credentials_file = os.getenv('GSC_CREDENTIALS_FILE')
    # domain = 'sc-domain:casinosnuevos.org'

    # dataset = get_gsc_data_16m(gsc_credentials_file, domain)
    # insert_gsc_data(dataset)


    # Atlas Search
    # Ініціалізація
    searcher = KeywordSearcher()

    # Пошук схожих слів
    results = searcher.simple_search("deposito", min_score=0.2, limit=1000)

    # Вивід результатів
    with open("results.txt", "w", encoding="UTF-8") as f:
        for result in results:
            f.write(f"{result['keyword']},{result['score']}\n")
    for result in results:
        print(f"Keyword: {result['keyword']}, Score: {result['score']}")
    


if __name__ == "__main__":
    main()

