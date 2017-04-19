from flask import Flask
from tapperWeb import getTapperData
app = Flask(__name__)

@app.route("/")
def home():
    return "home"

@app.route("/ann-arbor")
def annArbor():
    return getTapperData("ann-arbor")

if __name__ == "__main__":
    app.run(debug=True)