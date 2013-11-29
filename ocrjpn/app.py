from flask import Flask, render_template, request, jsonify
import create_image
import pdb
import json
import model

app = Flask(__name__)
app.secret_key = "shhhhthisisasecret"

@app.route("/jsontest")
def jsonning():
    results ={ 'results0': 
            {'cand1': 'thing',
            'cand2': 'thing',
            'cand3': 'thing'},
            'results1': 
            {'cand1': 'thing',
            'cand2': 'thing',
            'cand3': 'thing'}}



    return render_template("json_test.html", json=json.dumps(results))

# / has two routing functions. this one is for GET. the form has no action URL so it will just reload the same page it is on.
@app.route("/makeimage", methods=['POST'])
def make_image():
    img_data = request.form.get("dataUrl")
    coords = [request.form.get("x1"), request.form.get("y1"), request.form.get("x2"), request.form.get("y2")]
    results = create_image.img_from_string(img_data, coords)

    # final = {}

    # for i in range(len(results)):
    #     final[ "results" + str(i) ] = results[i]

    return jsonify(candidates=results)

@app.route("/define")
def define():
    lookup = request.args.get("lookup")

    db = model.lookup(lookup)

    return db

@app.route("/drawbox")
def drawbox():
    return render_template("drawbox.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug = True)