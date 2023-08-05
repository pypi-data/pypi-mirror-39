from flask import Flask
from flask_dotenv import DotEnv

app = Flask(__name__)

env = DotEnv()
env.init_app(app)

settings = app.config
