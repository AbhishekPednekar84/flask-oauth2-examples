from flask import Blueprint, request, redirect, url_for
from requests import get, post
from config import Config
from oauthlib.oauth2 import WebApplicationClient
from models.user import User
from flask_login import login_user
from utilities.create_user import create_user

github_oauth_bp = Blueprint("github", __name__, template_folder="templates")
client = WebApplicationClient(Config.GITHUB_CLIENT_ID)


@github_oauth_bp.route("/login/github/callback")
def callback():
    code = request.args.get("code")
    # print(code)
    github_token_endpoint = Config.GITHUB_TOKEN_URL

    token_url, headers, body = client.prepare_token_request(github_token_endpoint,
                                             authorization_response=request.url,
                                             redirect_url=request.base_url,
                                             code=code)

    token_response = post(token_url,
                          headers=headers,
                          data=body,
                          auth=(Config.GITHUB_CLIENT_ID, Config.GITHUB_CLIENT_SECRET))

    client.parse_request_body_response(token_response.text)

    user_info_endpoint = "https://api.github.com/user"
    uri, headers, body = client.add_token(user_info_endpoint)
    userinfo_response = get(uri, headers=headers, data=body)

    if userinfo_response.json().get("login"):
        unique_id = userinfo_response.json()["id"]
        user_email = userinfo_response.json()["email"]
        profile_pic = userinfo_response.json()["avatar_url"]
        user_name = userinfo_response.json()["name"]
    else:
        return "User not available or not verified by Github.", 400

    user = User(id=unique_id,
                name=user_name,
                email=user_email,
                profile_pic=profile_pic)

    user_created = create_user(user)

    if not user_created:
        return f"An account for {user_email} already exists"

    login_user(user)
    return redirect(url_for("home.success"))