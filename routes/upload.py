from flask import Blueprint,render_template,request,send_from_directory
import os

upload = Blueprint("upload",__name__)

@upload.route("/upload", methods=["GET", "POST"])
def upload_file():

    if request.method == "POST":

        file = request.files["file"]

        file.save("uploads/" + file.filename)

        return f"{file.filename} Uploaded Successfully"

    return render_template("upload.html")

@upload.route("/uploads/<filename>")
def uploaded_file(filename):

    return send_from_directory(
        "uploads",
        filename
    )


