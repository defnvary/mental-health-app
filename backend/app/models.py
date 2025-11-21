from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # hash and store the password
    def set_password(self, password):
        self.password = generate_password_hash(password)

    # check / verify given password matches the hashed one
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    # Flask-Login requires these four methods, UserMixin provides them automatically
    # is_authenticated, is_active, is_anonymous, get_id

    def __repr__(self):
        return f"<User {self.email}>"