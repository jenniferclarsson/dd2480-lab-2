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

# "Build histroy" routes
@app.route("/builds/<build_id>")
def get_build_info_html(build_id):
    try:
        log_relative_path = r"./src/build_logs/" + build_id + ".log"
        with open(log_relative_path) as log:
            log_lines = log.readlines()
            log.close()
    
        log_newline_seperated_string = "\n".join(log_lines)
        log_html_formatted = build_log_html_element(log_newline_seperated_string)

        return log_html_formatted
    except FileNotFoundError:
        return "<p>the build you are trying to access does not exist.<p>"

if __name__ == "__main__":
    print(public_url)
    app.run(port=8080)
