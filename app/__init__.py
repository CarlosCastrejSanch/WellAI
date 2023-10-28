from flask import Flask
from .config import Config,basedir
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from gpt4all import GPT4All


app = Flask(__name__)


GPTJ = GPT4All(model_name="ggml-gpt4all-j-v1.3-groovy",model_path=basedir)

app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db,compare_type=True)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from .views import *
from .models import *
