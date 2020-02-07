from utilities.db import db
from flask_login import UserMixin
from utilities.login_manager import login_manager


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    profile_pic = db.Column(db.String(1000))

    def __repr__(self):
        return f"User({self.id}, {self.name}, {self.email})"

    @classmethod
    def check_if_user_exists(cls, email):
        return cls.query.filter_by(email=email).first()

    def create_user(user):
        db.session.add(user)
        db.session.commit()


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    return User.query.get(user_id)
