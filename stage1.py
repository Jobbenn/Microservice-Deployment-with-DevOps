from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

NEWS_API_KEY = '42a144afe912471d84a88d42f718c10b'
NEWS_API_URL = 'https://newsapi.org/v2/top-headlines?country=us&apiKey='

kanban_data = {
    "todo": [],
    "in_progress": [],
    "completed": []
}

@app.route('/')
def index():
    news_response = requests.get(NEWS_API_URL + NEWS_API_KEY)
    news_data = news_response.json().get("articles", [])
    return render_template('index.html', kanban=kanban_data, news=news_data)

@app.route('/add_task', methods=['POST'])
def add_task():
    task = request.json.get('task')
    kanban_data['todo'].append(task)
    return jsonify(kanban_data)

@app.route('/move_task', methods=['POST'])
def move_task():
    task = request.json.get('task')
    from_section = request.json.get('from')
    to_section = request.json.get('to')

    if task in kanban_data[from_section]:
        kanban_data[from_section].remove(task)
        kanban_data[to_section].append(task)

    return jsonify(kanban_data)

if __name__ == '__main__':
    app.run(debug=True)
