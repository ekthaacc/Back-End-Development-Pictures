from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for item in data:
        if item['id'] == id:
            return jsonify(item)
        
    return jsonify(message="Not found"), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    try:
        picture = request.get_json()

        id_exists = any(item['id'] == picture['id'] for item in data)
        if id_exists == True:
            return jsonify(Message=f"picture with id {picture['id']} already present"), 302
        
        data.append(picture)
        return jsonify(picture), 201

    except Exception as e:
        return jsonify(message=f'error occured {e}'), 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    picture = request.get_json()
    for i, item in enumerate(data):
        if item['id'] == id:
            data[i] = picture
            return jsonify(picture)
    return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for i, item in enumerate(data):
        if item['id'] == id:
            del data[i]
            return make_response('', 204)
    return jsonify({"message": "picture not found"}), 404