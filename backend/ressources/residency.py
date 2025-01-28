from bson import ObjectId
from flask import Blueprint, jsonify, request, current_app, abort
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, jsonify, request, abort, current_app
from ressources.auth import token_required
from Models.residency import (
    get_all_residencies,
    get_residency_by_id,
    insert_residency,
    update_residency_in_db,
    delete_residency_from_db,
    get_blocks_by_residency,
    get_block_by_id,
    insert_block,
    update_block_by_id,
    delete_block_by_id,
    get_rooms_by_block,
    get_room_by_id,
    insert_room,
    update_room_by_id,
    delete_room_by_id,
    get_all_applications,
    get_application_by_id,
    insert_application,
    delete_application,
    get_all_reviews,
    get_review_by_id,
    insert_review,
    delete_review,
)

ResidencyBlueprint = Blueprint("residency", __name__)

### Residency Endpoints

@ResidencyBlueprint.route("/residencies", methods=["GET"])
def get_residencies():
    """Fetch all residencies (open to everyone)."""
    residencies = get_all_residencies()
    return jsonify(residencies), 200


@ResidencyBlueprint.route("/residencies/<string:residency_id>", methods=["GET"])
def get_residency(residency_id):
    """Fetch a specific residency by its ID (open to everyone)."""
    residency = get_residency_by_id(residency_id)
    if not residency:
        abort(404, description="Residency not found")
    return jsonify(residency), 200


@ResidencyBlueprint.route("/residencies", methods=["POST"])
@token_required
def create_residency():
    """Insert a new residency (admin only)."""
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    data = request.json
    if not data:
        abort(400, description="Invalid input")
    residency_id = insert_residency(data)
    return jsonify({"message": "Residency created", "residency_id": residency_id}), 201


@ResidencyBlueprint.route("/residencies/<string:residency_id>", methods=["PUT"])
@token_required
def update_residency(residency_id):
    """Update a residency (admin only)."""
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    data = request.json
    updated = update_residency_in_db(residency_id, data)
    if not updated:
        abort(404, description="Residency not found or update failed")
    return jsonify({"message": "Residency updated successfully"}), 200


@ResidencyBlueprint.route("/residencies/<string:residency_id>", methods=["DELETE"])
@token_required
def delete_residency(residency_id):
    """Delete a residency (admin only)."""
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    deleted = delete_residency_from_db(residency_id)
    if not deleted:
        abort(404, description="Residency not found")
    return jsonify({"message": "Residency deleted successfully"}), 200


### Block Endpoints

@ResidencyBlueprint.route("/<string:residency_id>/blocks", methods=["GET"])
@token_required
def get_blocks(residency_id):
    """
    Administrator: Fetch all blocks associated with a specific residency.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    try:
        blocks = get_blocks_by_residency(residency_id)
        return jsonify(blocks), 200
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

@ResidencyBlueprint.route("/blocks/<string:block_id>", methods=["GET"])
@token_required
def get_block(block_id):
    """
    Administrator: Fetch a block by its block_id.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    # Convert block_id to ObjectId
    try:
        block = get_block_by_id(block_id)
        if not block:
            return jsonify({"message": "Block not found"}), 404

        return jsonify(block), 200
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500
    
@ResidencyBlueprint.route("/<string:residency_id>/blocks", methods=["POST"])
@token_required
def post_block(residency_id):
    """
    Administrator: Create a new block associated with a specific residency.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    data = request.json
    if not data or not all(key in data for key in ("block_name", "number_of_floors", "total_rooms")):
        return jsonify({"message": "Missing required fields"}), 400

    # Add residency_id to the block data
    data["residency_id"] = ObjectId(residency_id)

    try:
        # Insert the block and use ObjectId as the block ID
        block_id = insert_block(data)
        return jsonify({"message": "Block created successfully", "block_id": block_id}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500


@ResidencyBlueprint.route("/blocks/<string:block_id>", methods=["PUT"])
@token_required
def update_block(block_id):
    """
    Administrator: Update a block by its block_id.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    data = request.json
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    # Update block using block_id
    updated = update_block_by_id(block_id, data)
    if not updated:
        return jsonify({"message": "Block not found or update failed"}), 404

    return jsonify({"message": "Block updated successfully"}), 200


@ResidencyBlueprint.route("/blocks/<string:block_id>", methods=["DELETE"])
@token_required
def delete_block(block_id):
    """
    Administrator: Delete a block by its block_id.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    # Delete block using block_id
    deleted = delete_block_by_id(block_id)
    if not deleted:
        return jsonify({"message": "Block not found or deletion failed"}), 404

    return jsonify({"message": "Block deleted successfully"}), 200


### Room Endpoints

@ResidencyBlueprint.route("/<string:block_id>/rooms", methods=["GET"])
@token_required
def get_rooms(block_id):
    """
    Administrator: Fetch all rooms associated with a specific block.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    try:
        rooms = get_rooms_by_block(block_id)
        return jsonify(rooms), 200
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

@ResidencyBlueprint.route("/rooms/<string:room_id>", methods=["GET"])
@token_required
def get_room(room_id):
    """
    Administrator: Fetch a room by its room_id.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    try:
        room = get_room_by_id(room_id)
        if not room:
            return jsonify({"message": "Room not found"}), 404
        return jsonify(room), 200
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

@ResidencyBlueprint.route("/<string:block_id>/rooms", methods=["POST"])
@token_required
def post_room(block_id):
    """
    Administrator: Create a new room associated with a specific block.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    data = request.json
    if not data or not all(key in data for key in ("room_number", "floor", "capacity", "is_available")):
        return jsonify({"message": "Missing required fields"}), 400

    # Add block_id to the room data
    data["block_id"] = ObjectId(block_id)

    try:
        # Insert the room and use ObjectId as the room ID
        room_id = insert_room(data)
        return jsonify({"message": "Room created successfully", "room_id": room_id}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500


@ResidencyBlueprint.route("/rooms/<string:room_id>", methods=["PUT"])
@token_required
def update_room(room_id):
    """
    Administrator: Update a room by its room_id.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    data = request.json
    if not data:
        return jsonify({"message": "Invalid input"}), 400

    # Update room using room_id
    updated = update_room_by_id(room_id, data)
    if not updated:
        return jsonify({"message": "Room not found or update failed"}), 404

    return jsonify({"message": "Room updated successfully"}), 200

@ResidencyBlueprint.route("/rooms/<string:room_id>", methods=["DELETE"])
@token_required
def delete_room(room_id):
    """
    Administrator: Delete a room by its room_id.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    # Delete room using room_id
    deleted = delete_room_by_id(room_id)
    if not deleted:
        return jsonify({"message": "Room not found or deletion failed"}), 404

    return jsonify({"message": "Room deleted successfully"}), 200


### Application Endpoints

##Admin
@ResidencyBlueprint.route("/applications", methods=["GET"])
@token_required
def get_applications():
    """Fetch all applications (admin only)."""
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    applications = get_all_applications()
    return jsonify(applications), 200


@ResidencyBlueprint.route("/applications/<string:application_id>", methods=["GET"])
@token_required
def get_application(application_id):
    """Fetch a specific application by ID (admin only)."""
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    application = get_application_by_id(application_id)
    if not application:
        abort(404, description="Application not found")
    return jsonify(application), 200



#student-specific application endpoints similarly.

@ResidencyBlueprint.route("/applications", methods=["POST"])
@token_required
def post_application():
    """Submit a new application (student only)."""
    if current_app.user["role"] != "student":
        return jsonify({"message": "Permission denied"}), 403

    data = request.json
    if not data or not all(key in data for key in ("residency_id", "preferred_roommate", "disease_status")):
        return jsonify({"message": "Missing required fields"}), 400

    application_data = {
        "username": current_app.user["username"],
        "residency_id": data["residency_id"],
        "preferred_roommate": data.get("preferred_roommate", ""),
        "disease_status": data.get("disease_status", ""),
        "status": "pending"
    }

    application_id = insert_application(application_data)
    return jsonify({"message": "Application submitted successfully", "application_id": application_id}), 201



@ResidencyBlueprint.route("/applications/<string:application_id>", methods=["DELETE"])
@token_required
def delete_application_route(application_id):
    """Delete an application (student only)."""
    if current_app.user["role"] != "student":
        return jsonify({"message": "Permission denied"}), 403

    username = current_app.user["username"]
    deleted = delete_application(application_id)
    if not deleted:
        abort(404, description="Application not found")
    return jsonify({"message": "Application deleted successfully"}), 200

### Admin Review Endpoints

@ResidencyBlueprint.route("/reviews", methods=["GET"])
@token_required
def get_reviews():
    """Fetch all reviews (admin only)."""
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    reviews = get_all_reviews()
    return jsonify(reviews), 200


@ResidencyBlueprint.route("/reviews/<string:review_id>", methods=["GET"])
@token_required
def get_review(review_id):
    """Fetch a specific review by ID (admin only)."""
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    review = get_review_by_id(review_id)
    if not review:
        abort(404, description="Review not found")
    return jsonify(review), 200





# student review endpoints
@ResidencyBlueprint.route("/reviews", methods=["POST"])
@token_required
def post_review():
    """Submit a new review (student only)."""
    if current_app.user["role"] != "student":
        return jsonify({"message": "Permission denied"}), 403

    data = request.json
    if not data or not all(key in data for key in ("residency_id", "rating", "review_text")):
        return jsonify({"message": "Missing required fields"}), 400

    review_data = {
        "username": current_app.user["username"],
        "residency_id": data["residency_id"],
        "rating": data["rating"],
        "review_text": data["review_text"],
        "timestamp": datetime.now()
    }

    review_id = insert_review(review_data)
    return jsonify({"message": "Review submitted successfully", "review_id": review_id}), 201


@ResidencyBlueprint.route("/reviews/<string:review_id>", methods=["DELETE"])
@token_required
def delete_review_route(review_id):
    """Delete a review (student only)."""
    if current_app.user["role"] != "student":
        return jsonify({"message": "Permission denied"}), 403

    deleted = delete_review(review_id)
    if not deleted:
        abort(404, description="Review not found")
    return jsonify({"message": "Review deleted successfully"}), 200