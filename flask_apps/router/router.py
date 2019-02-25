import os
from flask import Flask, redirect
app = Flask(__name__)

@app.route("/")
def index():
    return "add /hello after ip:port"

@app.route("/hello")
def hello():
    return redirect("http://95.216.170.95:5000")



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

