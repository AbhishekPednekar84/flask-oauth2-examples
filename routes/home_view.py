from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

home_bp = Blueprint("home", __name__, template_folder="templates")


@home_bp.route("/")
@home_bp.route("/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("home.success"))

    return render_template("home.html")


@home_bp.route("/success")
def success():
    return render_template("success.html")
