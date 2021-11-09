from flask import Blueprint, jsonify, request, make_response
from flask.globals import session
from app import db
from app.models.video import Video
#from sqlalchemy import asc, desc
from datetime import datetime
import requests
from dotenv import load_dotenv
import os 

load_dotenv()

videos_bp = Blueprint("videos", __name__, url_prefix="/videos")

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