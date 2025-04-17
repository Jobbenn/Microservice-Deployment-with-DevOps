from flask import Flask
from flask_login import LoginManager
from models import mongo, get_user_by_email
from news import news_bp
from kanban import kanban_bp
from auth import auth_bp

app = Flask(__name__)
app.secret_key = 'supersecretdevkey123'

# ✅ Set this BEFORE initializing mongo
app.config['MONGO_URI'] = 'mongodb://localhost:27017/devsecops'
app.config['NEWS_API_KEY'] = '42a144afe912471d84a88d42f718c10b'

# ✅ Init mongo after config is set
mongo.init_app(app)

# ✅ Flask-Login setup
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
from models import get_user_by_id

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

# ✅ Register blueprints
app.register_blueprint(news_bp)
app.register_blueprint(kanban_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)
