from flask import Blueprint,render_template,request,session,redirect
from werkzeug.utils import secure_filename
from models import db,User

profile = Blueprint("profile",__name__)

@profile.route("/profile")
def show_profile():

    if "username" not in session:
        return redirect("/login")

    user = User.query.filter_by(
        username=session["username"]
    ).first()

    return render_template("profile.html", user=user)

@profile.route("/edit-profile", methods=["GET", "POST"])
def edit_profile():

    if "username" not in session:
        return redirect("/login")

    user = User.query.filter_by(
        username=session["username"]
    ).first()

    if request.method == "POST":

        new_username = request.form.get("username")

        user.username = new_username

        db.session.commit()

        session["username"] = new_username

        return redirect("/profile")

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

    user = User.query.filter_by(username=session["username"]).first()
    user.photo = filename
    db.session.commit()

    return redirect("/profile")

@profile.route("/delete-account", methods=["POST"])

def delete_account():

    if "username" not in session:
        return redirect("/login")

    user = User.query.filter_by(
        username=session["username"]
    ).first()

    if user:

        db.session.delete(user)

        db.session.commit()

    session.clear()

    return redirect("/")
