from pymongo import MongoClient
import json
import os

client = MongoClient('mongodb://localhost:27017/')
db = client.postdb
collection = db.postlist

def insert_json_data(json_file):
    with open(json_file, 'r', encoding='UTF8') as file:
        data = json.load(file)
        if isinstance(data, dict):
            collection.insert_one(data)
        elif isinstance(data, list):
            collection.insert_many(data)
        else:
            print("Data format not supported for insertion.")

def process_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                insert_json_data(file_path)

def search_data(keyword):
    query = {
        "$or": [
            {"title": {"$regex": keyword, "$options": "i"}},
            {"text": {"$regex": keyword, "$options": "i"}},
            {"description": {"$regex": keyword, "$options": "i"}},
        ]
    }
    results = collection.find(query)
    result_list = []
    for result in results:
        result['_id'] = str(result['_id'])  # Convert ObjectId to string
        result_list.append(result)
    return result_list
# directory = 'C:\\Users\\zia20\\Documents\\GitHub\\darkweb_crawler\\json\\blacksuite'
# process_all_files(directory)

# transfer_network_documents()

search_results = search_data('mysql')
print(search_results)