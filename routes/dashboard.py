from flask import Blueprint
from flask import Blueprint,render_template,session,redirect
import sqlite3

dashboard = Blueprint("dashboard",__name__)

@dashboard.route("/dashboard")
def dashboard_home():

    if "username" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Total Users
    cursor.execute("SELECT COUNT(*) FROM accounts")
    total_users = cursor.fetchone()[0]

    # Total Messages
    cursor.execute("SELECT COUNT(*) FROM contacts")
    total_messages = cursor.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        total_users=total_users,
        total_messages=total_messages
    )

@dashboard.route("/admin/messages")
def admin_messages():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contacts")

    messages = cursor.fetchall()

    conn.close()

    return render_template(
        "messages.html",
        messages=messages
    )




