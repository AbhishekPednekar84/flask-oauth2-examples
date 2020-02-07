from flask import Blueprint, request, redirect, url_for
from requests import get, exceptions
from config import Config
from flask_login import logout_user
from routes.github_oauth import client as github_client
from routes.google_oauth import client as google_client, get_oauth_json

login_bp = Blueprint("login", __name__, template_folder="templates")


@login_bp.route("/login/<string:name>")
def login(name):

    if name == "google":
        uri = Config.GOOGLE_DISCOVERY_URL
        oauth_endpoint = get_oauth_json(uri)["authorization_endpoint"]
        scope = ["openid", "email", "profile"]
        client = google_client

    elif name == "github":
        oauth_endpoint = Config.GITHUB_DISCOVERY_URL
        scope = ["user"]
        client = github_client

    request_uri = client.prepare_request_uri(
        oauth_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=scope
    )

    return redirect(request_uri)


@login_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home.home"))
