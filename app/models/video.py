from app import db

class Video(db.Model):
    #specifying a tablename that is plural to match everywhere else.
    #__tablename__ = "Videos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    #available_inventory should be an attribute of the video
    available_inventory = db.Column(db.Integer)
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer",secondary = "Rentals", backref = "Videos",passive_deletes=True)


    def to_dict(self):
        return  {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }
