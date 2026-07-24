from flask import Blueprint,render_template,request,redirect,session,flash
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from models import db,User

auth = Blueprint("auth",__name__)

@auth.route("/register", methods=["GET", "POST"])
def register_form():

    if request.method == "POST":

        username = request.form.get("username").strip()
        password = request.form.get("password")

        # Empty validation
        if not username or not password:
            return render_template(
                "register.html",
                error="Username and Password are required."
            )

        # Duplicate username check
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return render_template(
                "register.html",
                error="Username already exists."
            )

        hashed_password = generate_password_hash(password)

        created_at = datetime.now().strftime("%d-%m-%Y %H:%M")

        user = User(
            username=username,
            password=hashed_password,
            created_at=created_at
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")

        return redirect("/login")

    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):

            print("Login Success")

            session["username"] = user.username

            flash("Welcome to NKTechVision!", "success")

            return redirect("/dashboard")

        else:

            flash("Invalid Username or Password!", "danger")

            return redirect("/login")

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

        user = User.query.filter_by(username=username).first()

        if user is None:
            return "❌ User not found"

        user.password = generate_password_hash(new_password)

        db.session.commit()

        return redirect("/login")

    return render_template("forgot_password.html")
