from flask import Blueprint,render_template,request,redirect,session
import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
#from models import db.User

auth = Blueprint("auth",__name__)

@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password)
        created_at = datetime.now().strftime("%d-%m-%Y %H:%M")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO accounts
            (username, password, created_at)
            VALUES (?, ?, ?)
            """,
            (username, hashed_password, created_at)
        )

        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT * FROM accounts
            WHERE username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()

        print("USER =", user)
        print("USERNAME =", username)
        print("PASSWORD =", password)
        conn.close()

        if user and check_password_hash(user[2], password):
            print("login success")

            session["username"] = username

            return redirect("/dashboard")
            print("login failed")

        return "Invalid Username or Password"

    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@auth.route("/change-password", methods=["GET", "POST"])
def change_password():

    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":

        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT password FROM accounts WHERE username = ?",
            (session["username"],)
        )

        user = cursor.fetchone()

        if not check_password_hash(user[0], current_password):
            conn.close()
            return "❌ Current Password is Incorrect"

        if new_password != confirm_password:
            conn.close()
            return "❌ New Passwords do not match"

        hashed_password = generate_password_hash(new_password)

        cursor.execute(
            """
            UPDATE accounts
            SET password = ?
            WHERE username = ?
            """,
            (hashed_password, session["username"])
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("change_password.html")

@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if request.method == "POST":

        username = request.form.get("username")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            return "❌ Passwords do not match"

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM accounts WHERE username = ?",
            (username,)
        )

        user = cursor.fetchone()

        if not user:
            conn.close()
            return "❌ User not found"

        hashed_password = generate_password_hash(new_password)

        cursor.execute(
            """
            UPDATE accounts
            SET password = ?
            WHERE username = ?
            """,
            (hashed_password, username)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("forgot_password.html")
