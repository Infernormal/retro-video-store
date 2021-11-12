from app import db
#from app import current_app

class Video(db.Model):
    #specifying a tablename that is plural to match everywhere else.
    __tablename__ = "Videos"
    video_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.DateTime)
    #available_inventory should be an attribute of the video
    available_inventory = db.Column(db.Integer)
    total_inventory = db.Column(db.Integer)
    customers = db.relationship("Customer", secondary="Rentals", cascade="delete", backref=db.backref('Videos', lazy=True), passive_deletes=True)


    def to_dict(self):
        return  {
            "id": self.video_id,
            "title": self.title,
            "release_date": self.release_date,
            "total_inventory": self.total_inventory
        }
