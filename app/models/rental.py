from app import db
from datetime import datetime
from flask import current_app

class Rental(db.Model):
    __tablename__="Rentals"
    id = db.Column(db.Integer, primary_key=True)
    due_date = db.Column(db.DateTime)
    videos_checked_count = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id", primary_key=True, nullable=False))
    video_id= db.Column(db.Integer, db.ForeignKey("video.id", primary_key=True, nullable=False))
    




   
