from app import db
from datetime import datetime
import datetime

class Rental(db.Model):
    __tablename__="Rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    due_date = db.Column(db.DateTime)    
    customer_id = db.Column(db.Integer, db.ForeignKey("Customers.customer_id"),nullable=False)
    video_id= db.Column(db.Integer, db.ForeignKey("video.id"),nullable=False)

#new helper functions

    def to_dict_for_check_in(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": self.videos_checked_out_count(self.video_id),
            "available_inventory": self.get_available_inventory(self.video_id)
        }


    def to_dict_for_check_out(self):
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": datetime.datetime.today() - datetime.timedelta(days=7),
            "videos_checked_out_count": self.videos_checked_out_count(self.video_id),
            "available_inventory": self.get_available_inventory(self.video_id)
        }
    
#Was trying to move those to Video but faced issues with imports and video_id
#Because of the way we set up our relationships it makes more sense to leave them here

    def videos_checked_out_count(self,video_id):
        videos = Rental.query.filter_by(video_id=video_id).all()
        return len(videos)


    def rentals_associated(self,video_id):
        rentals = Rental.query.filter_by(video_id=video_id).all()
        return len(rentals)


    def get_available_inventory(self,video_id):
        from app.models.video import Video
        video = Video.query.get(video_id)
        total_inventory = video.total_inventory
        available_inventory_count = total_inventory - self.rentals_associated(video_id)
        return available_inventory_count

#classmethod for fileds check

    @classmethod
    def check_checkout_fields(cls, request_body):

        required = ["customer_id", "video_id"]

        for field in required:
            if field not in request_body:
                return { "details" : f"Request body must include {field}."}, 400