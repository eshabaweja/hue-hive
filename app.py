import os
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/results",methods=["POST"])
def results():
    if request.method=="POST":
        # getting uploaded file
        uploaded_img = request.files["uploaded_img"]
        img_filename = uploaded_img.filename
        # saving it to static/uploads/
        filename = uploaded_img.filename
        file_path = os.path.join(app.root_path, 'static', 'uploads', filename)
        uploaded_img.save(file_path)

    return render_template("results.html", img_filename=img_filename)