from flask import Flask
from github_webhook import Webhook

app = Flask(__name__)
webhook = Webhook(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@webhook.hook()
def on_push(data):
    print("Got push with: {0}".format(data))

if __name__ == "__main__":
    app.run(port=8080)