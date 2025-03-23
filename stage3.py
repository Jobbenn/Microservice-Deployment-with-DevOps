from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import requests

app = Flask(__name__)

# MongoDB configuration
client = MongoClient("mongodb://localhost:27017/")
db = client.kanban

# News API configuration
NEWS_API_KEY = "42a144afe912471d84a88d42f718c10b"
NEWS_API_URL = "https://newsapi.org/v2/top-headlines?country=us&apiKey=" + NEWS_API_KEY

@app.route('/')
def index():
    tasks = {
        "todo": list(db.tasks.find({"status": "ToDo"})),
        "in_progress": list(db.tasks.find({"status": "In Progress"})),
        "completed": list(db.tasks.find({"status": "Completed"}))
    }
    return render_template("index.html", tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.json
    task = {
        "title": data['title'],
        "status": "ToDo"
    }
    db.tasks.insert_one(task)
    return jsonify({"message": "Task added successfully!"})

@app.route('/update_task/<task_id>', methods=['PUT'])
def update_task(task_id):
    new_status = request.json.get('status')
    db.tasks.update_one({"_id": task_id}, {"$set": {"status": new_status}})
    return jsonify({"message": "Task updated successfully!"})

@app.route('/delete_task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    db.tasks.delete_one({"_id": task_id})
    return jsonify({"message": "Task deleted successfully!"})

@app.route('/news')
def news():
    response = requests.get(NEWS_API_URL)
    articles = response.json().get("articles", [])
    return render_template("news.html", articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
