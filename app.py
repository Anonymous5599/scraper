from flask import Flask, render_template, request
from scraper import dynamic_scrape

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        url = request.form.get("url")
        attr_type = request.form.get("attr_type")
        attr_value = request.form.get("attr_value")
        selections = request.form.getlist("options")
        results = dynamic_scrape(url, attr_type, attr_value, selections)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
