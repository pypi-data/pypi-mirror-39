from flask import Flask, request
from flask import render_template

app = Flask(__name__)


@app.route("/")
@app.route("/<name>")
def index(name="World"):
    return render_template("index.html", name=name)


@app.route("/about")
def about():
    # Asciinema IDs
    videos = [
      dict(
        id=214436,
        title="Molecule - Ansible 2.6 - Linear strategy"
      ),
      dict(
        id=214438,
        title="Molecule - Ansible 2.6 - Mitogen Linear strategy"
      )
    ]

    video_autoplay = 'true' if request.args.get('autoplay', default='false', type=str) == 'true' else 'false'

    return render_template("about.html", videos=videos, video_autoplay=video_autoplay)
