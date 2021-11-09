from app import db
from app.models.customer import Customer
from flask import Blueprint, jsonify, request
from datetime import datetime
import os
import requests

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
            registered_at = datetime.utcnow()
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