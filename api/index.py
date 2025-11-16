# api/index.py

from flask import Flask, jsonify
from mangum import Mangum  # adapter to make Flask serverless

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({"message": "Hello from Flask on Vercel!"})

# This wraps your Flask app so Vercel can invoke it as a function
handler = Mangum(app)

