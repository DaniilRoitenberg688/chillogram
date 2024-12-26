from config import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String)
    password_hash = db.Column(db.String)

    def __init__(self, login):
        self.login = login


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {'login': self.login}


class Meme(db.Model):
    __tablename__ = 'memes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    description = db.Column(db.String, nullable=True)
    likes = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('memes'))

    def to_dict(self):
        return {'id': self.id,
                'name': self.name,
                'image': self.image,
                'description': self.description,
                'likes': self.likes}


