import requests
from flask import Blueprint, render_template, current_app
from flask_login import login_required, current_user
from models import get_user_kanban

news_bp = Blueprint('news', __name__)

@news_bp.route('/')
@login_required
def index():
    NEWS_API_KEY = current_app.config['NEWS_API_KEY']
    NEWS_API_KEY = "42a144afe912471d84a88d42f718c10b"
    response = requests.get(f'https://newsapi.org/v2/top-headlines?country=us&apiKey={NEWS_API_KEY}')
    news_data = response.json().get("articles", [])

    kanban_data = get_user_kanban(current_user.id)
    return render_template('index.html', kanban=kanban_data, news=news_data)
