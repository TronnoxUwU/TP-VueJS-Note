from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
cors = CORS(app, resources={f"/todo/api/v1.0/*": {"origins": "*"}})
app.config["SECRET_KEY"] = "8669704c-504a-4707-aab3-fd8e561ff1bc"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../API/db.sqlite"
db = SQLAlchemy(app)