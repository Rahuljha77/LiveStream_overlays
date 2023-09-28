from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson import ObjectId
from flask_cors import CORS 

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/liveact"
mongo = PyMongo(app)

CORS(app)
@app.route("/overlays", methods=["POST"])
def create_overlay():
    data = request.json  
    overlay_id = mongo.db.overlays.insert_one(data).inserted_id

    return jsonify({"message": "Overlay created successfully", "overlay_id": str(overlay_id)}), 201
@app.route("/overlays", methods=["GET"])
def get_all_overlays():
    overlays = mongo.db.overlays.find()
    overlay_list = [{"_id": str(overlay["_id"]), **overlay} for overlay in overlays]
    return jsonify(overlay_list), 200

@app.route("/overlays/<string:overlay_id>", methods=["PUT"])
def update_overlay(overlay_id):
    data = request.json 

 
    result = mongo.db.overlays.update_one(
        {"_id": ObjectId(overlay_id)},
        {"$set": data}
    )

    if result.modified_count == 1:
        return jsonify({"message": "Overlay updated successfully"}), 200
    else:
        return jsonify({"message": "Overlay not found or not updated"}), 404

@app.route("/overlays/<string:overlay_id>", methods=["DELETE"])
def delete_overlay(overlay_id):
    result = mongo.db.overlays.delete_one({"_id": ObjectId(overlay_id)})

    if result.deleted_count == 1:
        return jsonify({"message": "Overlay deleted successfully"}), 200
    else:
        return jsonify({"message": "Overlay not found or not deleted"}), 404

if __name__ == "__main__":
    app.run(debug=True)
