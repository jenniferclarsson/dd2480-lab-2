# dd2480-lab-2

## How to run the server

* Run `pip3 install -r requirements.txt` to install required dependencies.
* Run `python3 src/server.py` to run the server and make it visable on the internet. This command will output a public URL `xyz.ngrok.io`.
* Add a webhook on github using this payload URL `xyz.ngrok.io/github`. Content type should be `application/json`, the rest of the settings should be default.