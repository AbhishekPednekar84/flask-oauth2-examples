import json
from flask import Blueprint, request, redirect, url_for
from requests import get, post
from config import Config
from oauthlib.oauth2 import WebApplicationClient
from models.user import User
from flask_login import login_user
from utilities.create_user import create_user

linkedin_oauth_bp = Blueprint("linkedin", __name__, template_folder="templates")
client = WebApplicationClient(Config.LINKEDIN_CLIENT_ID)


@linkedin_oauth_bp.route("/login/linkedin/callback")
def callback():
    code = request.args.get("code")
    linkedin_token_endpoint = Config.LINKEDIN_TOKEN_URL

    # LinkedIn requires the client secret in the body
    # It therefore needs to be in the token request
    token_url, headers, body = client.prepare_token_request(linkedin_token_endpoint,
                                             authorization_response=request.url,
                                             redirect_url=request.base_url,
                                             code=code,
                                             client_secret=Config.LINKEDIN_CLIENT_SECRET)

    token_response = post(token_url,
                          headers=headers,
                          data=body,
                          auth=(Config.LINKEDIN_CLIENT_ID, Config.LINKEDIN_CLIENT_SECRET))

    client.parse_request_body_response(json.dumps(token_response.json()))

    user_info_endpoint = "https://api.linkedin.com/v2/me"
    uri, headers, body = client.add_token(user_info_endpoint)
    userinfo_response = get(uri, headers=headers, data=body)

    print(json.dumps(userinfo_response.json(), indent=2))

    if userinfo_response.json().get("id"):
        unique_id = userinfo_response.json()["id"]
        # Email and profile pic are not exposed on the public API
        # (https://business.linkedin.com/marketing-solutions/marketing-partners/become-a-partner/marketing-developer-program)
        user_email = " "
        profile_pic = " "
        user_name = userinfo_response.json()["firstName"]["localized"]["en_US"]
    else:
        return "User not available or not verified by LinkedIn.", 400

    user = User(id=unique_id,
                name=user_name,
                email=user_email,
                profile_pic=profile_pic)

    user_created = create_user(user)

    if not user_created:
        return f"An account for {user_email} already exists"

    login_user(user)
    return redirect(url_for("home.success"))
