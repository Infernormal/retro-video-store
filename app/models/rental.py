from app import db
from datetime import datetime
from flask import current_app

class Rental(db.Model):
    __tablename__="Rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    due_date = db.Column(db.DateTime)    
    customer_id = db.Column(db.Integer, db.ForeignKey("Customers.customer_id"),nullable=False)
    video_id= db.Column(db.Integer, db.ForeignKey("Videos.video_id"),nullable=False)
    #Do we want to delete rentals when a video or customer associated with it is deleted?  If so, un-comment (I think):
    # parent_video = db.relationship("Video", backref=db.backref("videos", cascade="delete"))
    # parent_customer = db.relationship("Customer", backref=db.backref("customers", cascade="delete"))