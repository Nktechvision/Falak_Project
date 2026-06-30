from flask import Blueprint,render_template,request,session,redirect
import sqlite3
from werkzeug.utils import secure_filename

profile = Blueprint("profile",__name__)

@profile.route("/profile")
def show_profile():

    if "username" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, created_at,photo  FROM accounts WHERE username = ?",
        (session["username"],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template("profile.html", user=user)


@profile.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "username" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    if request.method == "POST":

        new_username = request.form.get("username")

        cursor.execute(
            """
            UPDATE accounts
            SET username = ?
            WHERE username = ?
            """,
            (new_username, session["username"])
        )

        conn.commit()

        session["username"] = new_username

        conn.close()

        return redirect("/profile")

    cursor.execute(
        """
        SELECT username
        FROM accounts
        WHERE username = ?
        """,
        (session["username"],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template("edit_profile.html", user=user)

@profile.route("/profile/upload", methods=["POST"])
def profile_upload():
    print("PHOTO UPLOAD ROUTE CALLED")
    if "username" not in session:
        return redirect("/login")

    file = request.files["photo"]
    print(file.filename)

    if file.filename == "":
        return redirect("/profile")

    filename = secure_filename(file.filename)

    file.save("uploads/" + filename)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE accounts
        SET photo = ?
        WHERE username = ?
        """,
        (filename, session["username"])
    )

    conn.commit()
    conn.close()

    return redirect("/profile")


