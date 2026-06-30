from flask import Flask

from routes.pages import pages
from routes.auth import auth
from routes.dashboard import dashboard
from routes.profile import profile
from routes.upload import upload

from models import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = "nktechvision"

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(pages)
app.register_blueprint(dashboard)
app.register_blueprint(profile)
app.register_blueprint(upload)

app.run(debug=True)

