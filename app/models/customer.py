from app import db

class Customer(db.Model):
    __tablename__ = "Customers"
    customer_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)
    registered_at = db.Column(db.DateTime,nullable=True)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)
    videos = db.relationship("Video", secondary = "Rentals", backref = "Customers",passive_deletes=True)


    def to_dict(self):
        return({
            "id": self.customer_id,
            "name": self.name,
            "registered_at": self.registered_at,
            "postal_code": self.postal_code,
            "phone": self.phone
        })

#new helper functions

    def create_customer_to_dict(self):
         return ({
            "name": f"{self.name}",
            "phone": f"{self.phone}",
            "postal_code": f"{self.postal_code}"
         })
   
    def delete_customer_to_dict(self):
       return ({
            "id": self.customer_id,
            "details": f"Customer {self.name} successfully deleted"
        })
    
    #classmethod for fileds check

    @classmethod
    def check_customer_fields(cls, request_body):

        required = ["name", "postal_code", "phone"]

        for field in required:
            if field not in request_body:
                return { "details" : f"Request body must include {field}."}, 400