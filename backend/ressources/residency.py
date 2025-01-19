from flask import Blueprint, current_app, jsonify, request, abort
from ressources.auth import token_required
from Models.residency import (
    delete_student_application,
    get_all_residencies,
    get_residency_by_id,
    insert_residency,
    update_residency,
    delete_residency,
    insert_student_application
)

# Blueprint for residency routes
ResidencyBlueprint = Blueprint("residency", __name__)


#administrator 

@ResidencyBlueprint.route("/", methods=["GET"])
def get_residencies():
    """
    Administrator: Fetch all residencies.
    """
    residencies = get_all_residencies()
    return jsonify(residencies), 200

@ResidencyBlueprint.route("/<string:residency_id>", methods=["GET"])
def get_residency(residency_id):
    """
    Administrator: Fetch a residency by its ID.
    """
    residency = get_residency_by_id(residency_id)
    if not residency:
        abort(404, description="Residency not found")
    return jsonify(residency), 200

@ResidencyBlueprint.route("/", methods=["POST"])
@token_required
def create_residency():
    """
    Administrator: Create a new residency.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    data = request.json
    if not data:
        abort(400, description="Invalid input")
    try:
        residency_id = insert_residency(data)
        return jsonify({"message": "Residency created", "residency_id": residency_id}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500

@ResidencyBlueprint.route("/<string:residency_id>", methods=["PUT"])
@token_required
def update_residency_by_id(residency_id):
    """
    Administrator: Update residency details by its ID.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    data = request.json
    updated = update_residency(residency_id, data)
    if not updated:
        return jsonify({"message": "Residency not found or update failed"}), 400
    return jsonify({"message": "Residency updated successfully"}), 200

@ResidencyBlueprint.route("/<string:residency_id>", methods=["DELETE"])
@token_required
def delete_residency_by_id(residency_id):
    """
    Administrator: Delete residency by its ID.
    """
    if current_app.user["role"] != "admin":
        return jsonify({"message": "Permission denied"}), 403

    deleted = delete_residency(residency_id)
    if not deleted:
        return jsonify({"message": "Residency not found"}), 404
    return jsonify({"message": "Residency deleted successfully"}), 200


# student: application 

@ResidencyBlueprint.route("/apply", methods=["POST"])
@token_required
def apply_for_residency():
    """
    Student: Apply for a residency.
    """
    if current_app.user["role"] != "student":
        return jsonify({"message": "Admins cannot apply for residencies"}), 403

    data = request.json
    if not data or not all(key in data for key in ("residency_id", "preferred_roommate", "disease_status")):
        return jsonify({"message": "Missing required fields"}), 400

    application_data = {
        "username": current_app.user["username"],
        "residency_id": data["residency_id"],
        "preferred_roommate": data["preferred_roommate"],
        "disease_status": data["disease_status"],
        "status": "pending"
    }

    try:
        application_id = insert_student_application(application_data)
        return jsonify({"message": "Application submitted successfully", "application_id": application_id}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {e}"}), 500


# Student: Delete their own application
@ResidencyBlueprint.route("/applications/<application_id>", methods=["DELETE"])
@token_required
def delete_student_application_route(application_id):
    """
    Students can delete their own application.
    """
    student_id = current_app.user["username"]
    
    # Log to verify if username is being passed correctly
    current_app.logger.info(f"Attempting to delete application with ID: {application_id} for student: {student_id}")
    
    if delete_student_application(student_id, application_id):
        return jsonify({"message": "Application deleted successfully"}), 200
    else:
        return jsonify({"message": "Application not found"}), 404
