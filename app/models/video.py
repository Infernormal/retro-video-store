from app import db

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)