from flask import Flask, render_template, request, redirect, url_for, session, flash
from dotenv import load_dotenv
from auth import auth, login_required
from models import (
    init_db, create_application, get_applications,
    get_application_by_id, update_application,
    delete_application, get_stats
)
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

app.register_blueprint(auth)

with app.app_context():
    init_db()

@app.route("/")
@login_required
def dashboard():
    user_id = session["user_id"]
    username = session["username"]

    status_filter = request.args.get("status", "all")

    applications = get_applications(user_id, status_filter)
    stats = get_stats(user_id)

    return render_template(
        "dashboard.html",
        applications=applications,
        stats=stats,
        username=username,
        current_filter=status_filter
    )

@app.route("/add_application", methods=["GET", "POST"])
@login_required
def add_application():
    if request.method == "POST":
        user_id = session["user_id"]
        company_name = request.form["company_name"]
        role = request.form["role"]
        status = request.form["status"]
        applied_date = request.form["applied_date"]
        notes = request.form["notes"]
        job_link = request.form["job_link"]

        create_application(user_id, company_name, role, status, applied_date, notes, job_link)

        flash("Application added!", "success")
        return redirect(url_for("dashboard"))

    return render_template("application_form.html", application=None)

@app.route("/edit_application/<int:app_id>", methods=["GET", "POST"])
@login_required
def edit_application(app_id):
    application = get_application_by_id(app_id)

    if request.method == "POST":
        company_name = request.form["company_name"]
        role = request.form["role"]
        status = request.form["status"]
        applied_date = request.form["applied_date"]
        notes = request.form["notes"]
        job_link = request.form["job_link"]

        update_application(app_id, company_name, role, status, applied_date, notes, job_link)

        flash("Application updated!", "success")
        return redirect(url_for("dashboard"))

    return render_template("application_form.html", application=application)

@app.route("/delete_application/<int:app_id>")
@login_required
def delete_application_route(app_id):
    delete_application(app_id)
    flash("Application deleted!", "success")
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
