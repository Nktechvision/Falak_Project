from flask import Blueprint, render_template

python = Blueprint("python", __name__)

@python.route("/python")
def python_home():
    return render_template("python/index.html")

@python.route("/python/packing-unpacking")
def packing_unpacking():
    return render_template("python/packing-unpacking.html")
