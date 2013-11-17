from flask import Flask, render_template, request, redirect, url_for
import create_image

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

# / has two routing functions. this one is for GET. the form has no action URL so it will just reload the same page it is on.
@app.route("/makeimage", methods=['POST'])
def make_image():
    img_data = request.form.get("dataUrl")
    coords = [request.form.get("x1"), request.form.get("y1"), request.form.get("x2"), request.form.get("y2")]
    create_image.img_from_string(img_data, coords)
    return "okay"

if __name__ == "__main__":
    app.run(debug = True)