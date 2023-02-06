from flask import Flask, request, make_response
from pyngrok import ngrok
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
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
            return make_response("success", 200)
        except:
            return make_response("fail", 400)

if __name__ == "__main__":
    print(public_url)
    app.run(port=8080)