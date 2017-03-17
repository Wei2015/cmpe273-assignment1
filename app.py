from flask import Flask
from github import Github
import sys
import yaml
import json


app = Flask(__name__)


url = sys.argv[1]
args = url.split('/')
user = args[-2]
repo_name = args[-1]

@app.route("/")
def hello():
    return "Hello from Dockerized Flask App!!"


@app.route("/v1/<filename>")
def get_config(filename):
    g = Github()
    repo = g.get_user(user).get_repo(repo_name)

    isJson = False

    if filename.endswith(".json"):
        filename = filename.replace(".json", ".yml")
        isJson = True

    try:
        result = repo.get_file_contents(filename).content.decode('base64')
    except Exception as e:
        return "No such file!"
    
    if isJson:
        return json.dumps(yaml.load(result))
    else:
        return result


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

