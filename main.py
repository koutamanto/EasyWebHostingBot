import json
from flask import Flask, render_template, send_file, send_from_directory
import subprocess

app = Flask(__name__, subdomain_matching=True)

with open("json/infos.json", "r") as f:
    infos = json.load(f)
for subdomain in infos.keys():
    subdomain = infos[subdomain]["subdomain"]
    # app.add_url_rule('/<path:filename>',
    #                 endpoint=subdomain,
    #                 subdomain=subdomain,
    #                 view_func=app.send_static_file,
    #                 )

@app.route("/<string:subdomain>/<path:path>")
def users_page(subdomain, path):
    print(path)
    return send_file(f"templates/datas/{subdomain}/{path}")

@app.route("/")
def index():
    return render_template("index.html")

if "__main__" == __name__:
    app.debug = True
    # subprocess.Popen("run_scripts.bat")
    app.run(host="0.0.0.0", port=80)