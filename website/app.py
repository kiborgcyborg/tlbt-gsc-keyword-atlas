import os
import sys
import csv
from flask import Flask, request, jsonify, render_template, send_file
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile

# Додаємо кореневу директорію проекту до sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modules.mongodb.atlas_search import KeywordSearcher

load_dotenv()

app = Flask(__name__)

# Ініціалізація KeywordSearcher
searcher = KeywordSearcher(
    connection_string=os.getenv('MONGO_URI'),
    database=os.getenv('DB_NAME'),
    collection=os.getenv('COLLECTION_NAME'),
    index=os.getenv('MONGO_ATLAS_SEARCH_INDEX')
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    min_score = float(request.args.get('min_score', 0.5))
    limit = int(request.args.get('limit', 1000))
    fuzzy_max_edits = int(request.args.get('fuzzy_max_edits', 2))
    
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    try:
        results = searcher.simple_search(
            query=query,
            min_score=min_score,
            limit=limit,
            fuzzy_max_edits=fuzzy_max_edits
        )
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['GET'])
def download():
    query = request.args.get('query')
    min_score = float(request.args.get('min_score', 0.5))
    limit = int(request.args.get('limit', 1000))
    fuzzy_max_edits = int(request.args.get('fuzzy_max_edits', 2))
    
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    try:
        results = searcher.simple_search(
            query=query,
            min_score=min_score,
            limit=limit,
            fuzzy_max_edits=fuzzy_max_edits
        )
        
        # Створення тимчасового файлу CSV
        temp_file = NamedTemporaryFile(delete=False, mode='w', newline='', suffix='.csv')
        with open(temp_file.name, 'w', newline='') as csvfile:
            fieldnames = ['keyword', 'score']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in results:
                writer.writerow({'keyword': item['keyword'], 'score': item['score']})
        
        download_name = f'{query}_results.csv'
        return send_file(temp_file.name, as_attachment=True, download_name=download_name)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)