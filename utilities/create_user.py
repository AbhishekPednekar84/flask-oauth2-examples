from models.user import User


def create_user(user):
    if not User.check_if_user_exists(user.email):
        User.create_user(user)
        return True
    else:
        return False
