import os
from flask import Flask, render_template, request
import numpy as np
from skimage import io, color
from sklearn.cluster import KMeans

app = Flask(__name__)

# function to generate palette
def generate_palette(image_path, n_colors=5):
    # Load the image in RGBA format
    rgba_image = io.imread(image_path)

    # Convert the image to RGB format
    rgb_image = color.rgba2rgb(rgba_image)

    # Convert the image to the LAB color space
    lab_image = color.rgb2lab(rgb_image)

    # Reshape the image to a 2D array of pixels
    w, h, d = lab_image.shape
    pixels = np.reshape(lab_image, (w * h, d))

    # Cluster the pixels using K-means clustering
    kmeans = KMeans(n_clusters=n_colors, random_state=42).fit(pixels)

    # Get the center colors of each cluster
    palette = kmeans.cluster_centers_

    # # Convert the palette colors back to the RGB color space
    # palette = color.lab2rgb(palette.reshape(1, -1, 3)).reshape(-1, 3)

    # return palette

    # Convert the color values to integers
    palette = np.round(color.lab2rgb(palette.reshape(1, -1, 3)).reshape(-1, 3) * 255).astype(int)

    return palette.tolist()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/results",methods=["POST"])
def results():
    img_filename = ""
    palette = []
    if request.method=="POST":
        # getting uploaded file
        uploaded_img = request.files["uploaded_img"]
        img_filename = uploaded_img.filename
        # saving it to static/uploads/
        filename = uploaded_img.filename
        file_path = os.path.join(app.root_path, 'static', 'uploads', filename)
        uploaded_img.save(file_path)
        # calculating the palette colors
        palette = generate_palette(file_path)
        # create downloadable json file
        print(palette)

    # return many variables as outputs
    return render_template("results.html", img_filename=img_filename, palette=palette)