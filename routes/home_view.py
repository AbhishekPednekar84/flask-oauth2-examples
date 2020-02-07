from flask import Blueprint, render_template

home_bp = Blueprint("home", __name__, template_folder="templates")


@home_bp.route("/")
@home_bp.route("/home")
def home():
    return render_template("home.html")


@home_bp.route("/success")
def success():
    return render_template("success.html")
