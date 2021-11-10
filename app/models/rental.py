from app import db
from datetime import datetime
from flask import current_app

class Rental(db.Model):
    __tablename__="Rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    due_date = db.Column(db.DateTime)
    videos_checked_out_count = db.Column(db.Integer)
    available_inventory = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("Customers.customer_id"),nullable=False)
    video_id= db.Column(db.Integer, db.ForeignKey("video.id"),nullable=False)
    



   
