from flask import Flask, jsonify, render_template, request, redirect, url_for
import json
import pymongo

app = Flask(__name__)

# MongoDB Atlas connection
client = pymongo.MongoClient("MONGODB_CONNECTION_URI")
db = client["flaskdb"]
collection = db["users"]

# API route to read JSON file and return list
@app.route('/api')
def api():
    with open("Data.json", "r") as f:
        data = json.load(f)
    return jsonify(data)

# Route to render form
@app.route('/')
def form():
    return render_template("form.html")

# Handle form submission
@app.route('/submit', methods=["POST"])
def submit():
    try:
        name = request.form['name']
        email = request.form['email']

        # Insert into MongoDB
        collection.insert_one({"name": name, "email": email})

        return redirect(url_for("success"))
    except Exception as e:
        return render_template("form.html", error=str(e))

# Success page
@app.route('/success')
def success():
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
