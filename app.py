from flask_jwt_extended import JWTManager
from routes.api import api
from flask import Flask
from routes.pages import pages
from routes.auth import auth
from routes.dashboard import dashboard
from routes.profile import profile
from routes.upload import upload
from routes.python import python


from models import db
import os

app.config["JWT_SECRET_KEY"] = "nktechvision_jwt_secret"
jwt = JWTManager(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "sqlite:///" + os.path.join(BASE_DIR, "database.db")


app.secret_key = "nktechvision"

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(pages)
app.register_blueprint(dashboard)
app.register_blueprint(profile)
app.register_blueprint(upload)
app.register_blueprint(python)
app.register_blueprint(api)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
