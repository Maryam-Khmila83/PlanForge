from flask import (
    Flask, 
    render_template, 
    request,
    send_file
)

from analyzer import analyze_project
from pdf_export import export_pdf

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    project_description = request.form["project"]

    hours_per_day = float(
        request.form["hours_per_day"]
    )

    days_per_week = float(
        request.form["days_per_week"]
    )

    (
        data,
        months_single,
        months_team,
        hours_per_week
    ) = analyze_project(
        project_description,
        hours_per_day,
        days_per_week
    )

    export_pdf(
        data,
        months_single,
        months_team,
        hours_per_week
    )

    return send_file(
        "project_analysis.pdf",
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)