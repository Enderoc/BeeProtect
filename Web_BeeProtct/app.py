from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

@app.route("/")
def index():
    return render_template("company.html")

@app.route("/company")
def company():
    return render_template("company.html")

@app.route("/project")
def project():
    return render_template("project.html")
