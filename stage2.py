from flask import Flask, render_template, request, redirect, url_for
import requests
from pymongo import MongoClient

app = Flask(__name__)

NEWS_API_KEY = "42a144afe912471d84a88d42f718c10b"
NEWS_URL = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}"

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client.kanban_db
kanban_collection = db.tasks

@app.route("/")
def index():
    news_response = requests.get(NEWS_URL).json()
    articles = news_response.get("articles", [])[:5]  # Get top 5 news articles

    # Fetch tasks from MongoDB
    tasks = {"ToDo": [], "InProgress": [], "Completed": []}
    for task in kanban_collection.find():
        tasks[task["section"]].append(task["task"])

    return render_template("index.html", tasks=tasks, articles=articles)

@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        kanban_collection.insert_one({"task": task, "section": "ToDo"})
    return redirect(url_for("index"))

@app.route("/move_task", methods=["POST"])
def move_task():
    task = request.form.get("task")
    current_section = request.form.get("current_section")
    next_section = request.form.get("next_section")

    if task and current_section and next_section:
        kanban_collection.update_one(
            {"task": task, "section": current_section},
            {"$set": {"section": next_section}}
        )

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
