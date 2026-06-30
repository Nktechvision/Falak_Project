from flask import Blueprint, render_template,request
import sqlite3
pages = Blueprint("pages", __name__)

@pages.route("/")
def home():
    return render_template("index.html")

@pages.route("/about")
def about():
    return render_template("about.html")

@pages.route("/services")
def services():
    return render_template("services.html")

@pages.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO contacts(name, email, message) VALUES (?, ?, ?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        return "Message Sent Successfully 🚀"

    return render_template("contact.html")
