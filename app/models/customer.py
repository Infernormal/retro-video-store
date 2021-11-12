from flask import current_app
from app import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = "Customers"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime,nullable=True)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    #videos_checked_out should be an attribute of the customer that gets incremented or decremented during checkout
    videos_checked_out_count = db.Column(db.Integer)    
    videos = db.relationship("Video", secondary="Rentals", cascade="delete", backref=db.backref('Customers', lazy=True), passive_deletes=True)


    def to_dict(self):
        return({
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        })
