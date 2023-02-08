from flask import Flask, request, make_response
from pyngrok import ngrok
from utils.utils import *
import utils.settings as settings

public_url = ngrok.connect(8080).public_url
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/github", methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            data = request.json
            clone_url, branch = parse_json(data)
            return make_response("success", 200)
        except:
            return make_response("fail", 400)

if __name__ == "__main__":
    print(run_tests())
    # print(public_url)
    # app.run(port=8080)
