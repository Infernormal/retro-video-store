
from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.video import Video
from app.models.customer import Customer
from app.models.rental import Rental
from datetime import datetime
import datetime


videos_bp = Blueprint("videos", __name__, url_prefix="/videos")
customer_bp = Blueprint("customer_bp", __name__,url_prefix="/customers")
rental_bp = Blueprint("rental_bp", __name__,url_prefix="/rentals")

#VIDEO ROUTES

@videos_bp.route("", methods=["GET", "POST"], strict_slashes=False)
def create_videos():
    if request.method == "POST":
        request_body = request.get_json()
        input_check = validate_video_input(request_body)
        if input_check['error']: 
            return make_response({"details":input_check['details']}), input_check['status_code']
        else:    
            new_video = Video(title=request_body['title'], release_date=request_body['release_date'], total_inventory=request_body['total_inventory'])
            db.session.add(new_video)
            db.session.commit()
            return make_response(new_video.to_dict()), 201
    elif request.method == "GET":
        video_list = Video.query.all()
        response = []
        for my_video in video_list:
            response.append(my_video.to_dict())
        
        return jsonify(response), 200

@videos_bp.route("/<video_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def get_video(video_id):
    try:
        video_id = int(video_id)
    except ValueError:
        return "Error, please provide the integer id of the video", 400
    my_video = Video.query.get(video_id)
    if request.method == "GET":
        if my_video is None:
            return {"message": "Video " + str(video_id) + " was not found"}, 404
        else:
            return make_response(my_video.to_dict()), 200

    elif request.method == "PUT":
        request_body = request.get_json()
        if my_video is None:
            return {"message": "Video " + str(video_id) + " was not found"}, 404
        else:
            input_check = validate_video_input(request_body)
            if input_check['error']: 
                return make_response({"details":input_check['details']}), input_check['status_code']
            else:  
                my_video.title = request_body["title"]
                my_video.release_date = request_body["release_date"]
                my_video.total_inventory =request_body ["total_inventory"]
                db.session.commit()        
                return make_response(my_video.to_dict()), 200


    elif request.method == "DELETE":
        if my_video is None:
            return {"message": "Video 1 was not found"}, 404
        else:        
            db.session.delete(my_video)
            db.session.commit()
            return make_response({"id":video_id}), 200


def validate_video_input(request_body):
    if "title" not in request_body:
        return {"error":True, "details": "Request body must include title.", "status_code": 400}
    elif "release_date" not in request_body:
        return {"error":True, "details": "Request body must include release_date.", "status_code": 400}
    elif "total_inventory" not in request_body:
        return {"error":True, "details": "Request body must include total_inventory.", "status_code": 400}
    else:
        return {"error":False, "details": "", "status_code": 200}


customer_bp = Blueprint("customer_bp", __name__,url_prefix="/customers")

#CUSTOMER ROUTES

@customer_bp.route("",methods =["POST","GET"])
def handle_customers():
    if request.method == "POST":
        request_body = request.get_json()
        if "name" not in request_body:
            return ({
                "details": "Request body must include name."
            }),400
        elif "phone" not in request_body:
            return ({
                "details": "Request body must include phone."
            }),400
        elif "postal_code" not in request_body:
            return ({
                "details": "Request body must include postal_code."
            }),400
        new_customer = Customer(
            name = request_body["name"],
            postal_code = request_body["postal_code"],
            phone = request_body["phone"],
            registered_at = datetime.datetime.utcnow()
        )
        db.session.add(new_customer)
        db.session.commit()
        return (new_customer.to_dict()),201

    elif request.method == "GET":
        customers_response = []
        customers = Customer.query.all()
        for customer in customers:
            customers_response.append(customer.to_dict())
        return jsonify(customers_response)


@customer_bp.route("/<customer_id>", methods = ["GET","PUT","DELETE"])
def handle_customer(customer_id):
    if not customer_id.isnumeric():
        return { "Error": f"{customer_id} must be numeric."}, 400
    customer_id = int(customer_id)
    customer = Customer.query.get(customer_id)
    if not customer:
        return ({"message": f"Customer {customer_id} was not found"}),404

    if request.method == "GET":
        return (customer.to_dict()),200


    elif request.method == "PUT":
        form_data = request.get_json()
        if "name" not in form_data or "postal_code" not in form_data or "phone" not in form_data:
            return ({
                "details": "Invalid data"
            }),400
        customer.name = form_data['name']
        customer.postal_code = form_data['postal_code']
        customer.phone = form_data['phone']

        db.session.commit()

        return ({
            "name": f"{customer.name}",
            "phone": f"{customer.phone}",
            "postal_code": f"{customer.postal_code}"
        }),200

    elif request.method == "DELETE":
        db.session.delete(customer)
        db.session.commit()

        return ({
            "id": customer.customer_id,
            "details": f"Customer {customer.name} successfully deleted"
        }), 200

#RENTAL ROUTES

@rental_bp.route("/check-out", methods = ["POST"])
def handle_checkout():   
    if request.method == "POST":
        request_body = request.get_json()
        if "customer_id" not in request_body:
            return ({
                "details": "Request body must include customer_id."
            }),400
        elif "video_id" not in request_body:
            return ({
                "details": "Request body must include video_id."
            }),400
        

        #check that the video exists before attempting to create the rental
        target_video = Video.query.get(request_body['video_id']) 
        if not target_video:
            return "Video_id doesn't exist",404

        #check that the customer exists before attempting to create the rental
        target_customer = Customer.query.get(request_body['customer_id'])
        if not target_customer:
            return "Customer_id doesn't exist",404

        #check that the video is available in inventory
        if  int(target_video.total_inventory) < 1:
            return ({"message": "Could not perform checkout"}),400

        if target_video.available_inventory is None:
            target_video.available_inventory = 0
        if  int(target_video.available_inventory) < 1:
            return ({"message": "Could not perform checkout"}),400            
    
        #going to set this here in case we need to in the future allow for a customer to 
        #check out more than one video
        num_of_videos_getting_checked_out = 1

        #Now that we are sure the related items exist, we create the rental record
        new_rental = Rental(
            customer_id = request_body["customer_id"],
            video_id = request_body["video_id"],
            due_date = (datetime.datetime.now() + datetime.timedelta(days=7))
        )
        db.session.add(new_rental)

        #Now update the Customer to increment the videos_checked_out_count
        if target_customer.videos_checked_out_count is None:
            target_customer.videos_checked_out_count = 0
        rental_customer_videos_count = int(target_customer.videos_checked_out_count) + num_of_videos_getting_checked_out
        target_customer.videos_checked_out_count = rental_customer_videos_count
        
        #Now update the Video to decrement the available inventory

        rental_video_available_inventory = int(target_video.available_inventory) - num_of_videos_getting_checked_out
        target_video.available_inventory = rental_video_available_inventory

        #Now save all the changes to the db (Rental, Customer, and Video)
        db.session.commit()


        return ({
            "customer_id": new_rental.customer_id,
            "video_id": new_rental.video_id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": target_customer.videos_checked_out_count,
            "available_inventory": target_video.available_inventory

        }),200

@rental_bp.route("/check-in", methods = ["POST"])
def handle_checkin():   
    if request.method == "POST":
        request_body = request.get_json()
        if "customer_id" not in request_body:
            return ({
                "details": "Request body must include customer_id."
            }),400
        elif "video_id" not in request_body:
            return ({
                "details": "Request body must include video_id."
            }),400
        

        #check that the video exists before attempting to return the rental
        target_video = Video.query.get(request_body['video_id']) 
        if not target_video:
            return "Video_id doesn't exist", 404

        #check that the customer exists before attempting to return the rental
        target_customer = Customer.query.get(request_body['customer_id'])
        if not target_customer:
            return "Customer_id doesn't exist", 404

    
        #going to set this here in case we need to in the future allow for a customer to 
        #check in more than one video
        num_of_videos_getting_checked_in = 1

        #Now that we have the foreign keys, we can grab the rental and delete it.
        #If it does not exist, we catch the exception and display a nice message.

        return_rental = Rental.query.filter_by(
            customer_id = request_body["customer_id"],
            video_id = request_body["video_id"]
        ).first()
        if return_rental is None:
            return {"message": f"No outstanding rentals for customer {request_body['customer_id']} and video {request_body['video_id']}"}, 400
        else:
            db.session.delete(return_rental)
            
        #Now update the Customer to decrement the videos_checked_out_count
        # if target_customer.videos_checked_out_count is None:
        #     target_customer.videos_checked_out_count = 0
        rental_customer_videos_count = int(target_customer.videos_checked_out_count) - num_of_videos_getting_checked_in 
        target_customer.videos_checked_out_count = rental_customer_videos_count
        
        #Now update the Video to increment the available inventory

        rental_video_available_inventory = int(target_video.available_inventory) + num_of_videos_getting_checked_in
        target_video.available_inventory = rental_video_available_inventory

        #Now save all the changes to the db (Rental, Customer, and Video)
        db.session.commit()


        return ({
            "customer_id": return_rental.customer_id,
            "video_id": return_rental.video_id,
            "videos_checked_out_count": target_customer.videos_checked_out_count,
            "available_inventory": target_video.available_inventory

        }),200

@videos_bp.route("/<video_id>/rentals", methods = ["GET"])
def handle_rentals_by_id(video_id):
    if not video_id.isnumeric():
        return { "Error": f"{video_id} must be numeric."}, 400
    video_id = int(video_id)
    video = Video.query.get(video_id)
    if not video:
        return ({"message":f"Video {video_id} was not found"}), 404

    rentals_response = []
    for customer in video.customers:
        rentals_response.append({
            "name": customer.name
        })
        print(rentals_response)
    return jsonify(rentals_response)

@customer_bp.route("/<customer_id>/rentals", methods = ["GET"])
def handle_rentals_by_id(customer_id):
    if not customer_id.isnumeric():
        return { "Error": f"{customer_id} must be numeric."}, 400
    customer_id = int(customer_id)
    customer = Customer.query.get(customer_id)
    if not customer:
        return ({"message": f"Customer {customer_id} was not found"}),404

    if request.method == "GET":
        rentals_response = []
        for video in customer.videos:
            rentals_response.append({
                "title": video.title,
                "release_date": video.release_date,
                "due_date":Rental.query.get(customer_id).due_date
            })
            print(rentals_response)
        return jsonify(rentals_response)