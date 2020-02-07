import json
from flask import Blueprint, request, redirect, url_for
from requests import get, post, exceptions
from config import Config
from oauthlib.oauth2 import WebApplicationClient
from models.user import User
from flask_login import login_user
from utilities.create_user import create_user

google_oauth_bp = Blueprint("google", __name__, template_folder="templates")
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)


def get_oauth_json(uri):
    try:
        return get(uri).json()
    except (exceptions.HTTPError, exceptions.ConnectionError, exceptions.ConnectTimeout):
        return {"message": "Error while calling the Google OAuth URL"}, 500


@google_oauth_bp.route("/login/google/callback")
def callback():
    code = request.args.get("code")
    google_token_endpoint = get_oauth_json(Config.GOOGLE_DISCOVERY_URL)["token_endpoint"]

    token_url, headers, body = client.prepare_token_request(google_token_endpoint,
                                             authorization_response=request.url,
                                             redirect_url=request.base_url,
                                             code=code)
    print(f"request.url = {request.url}, headers = {headers}, body = {body}")
    token_response = post(token_url,
                          headers=headers,
                          data=body,
                          auth=(Config.GOOGLE_CLIENT_ID, Config.GOOGLE_CLIENT_SECRET))

    client.parse_request_body_response(json.dumps(token_response.json()))

    user_info_endpoint = get_oauth_json(Config.GOOGLE_DISCOVERY_URL)["userinfo_endpoint"]
    uri, headers, body = client.add_token(user_info_endpoint)
    userinfo_response = get(uri, headers=headers, data=body)

    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        user_email = userinfo_response.json()["email"]
        profile_pic = userinfo_response.json()["picture"]
        user_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    user = User(id=unique_id,
                name=user_name,
                email=user_email,
                profile_pic=profile_pic)

    user_created = create_user(user)

    if not user_created:
        return f"An account for {user_email} already exists"

    login_user(user)
    return redirect(url_for("home.success"))