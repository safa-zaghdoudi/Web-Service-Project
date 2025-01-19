from flask import current_app
from bson.objectid import ObjectId
from flask_pymongo import PyMongo

mongo = PyMongo()

def get_all_residencies():
    """
    Fetch all residencies from the database.
    Accessible by both admins and students.
    """
    try:
        collection = current_app.db["residencies"]
        residencies = list(collection.find())
        for residency in residencies:
            residency["_id"] = str(residency["_id"])
        return residencies
    except Exception as e:
        current_app.logger.error(f"Error fetching residencies: {e}")
        return []

def get_residency_by_id(residency_id):
    """
    Fetch a specific residency by its ID.
    Accessible by both admins and students.
    """
    try:
        collection = current_app.db["residencies"]
        residency = collection.find_one({"_id": ObjectId(residency_id)})
        if residency:
            residency["_id"] = str(residency["_id"])
        return residency
    except Exception as e:
        current_app.logger.error(f"Error fetching residency by ID: {e}")
        return None

def insert_residency(data):
    """
    Insert a new residency into the database.
    Admins can create new residencies.
    """
    try:
        collection = current_app.db["residencies"]
        return str(collection.insert_one(data).inserted_id)
    except Exception as e:
        current_app.logger.error(f"Error inserting residency: {e}")
        raise RuntimeError("Failed to insert residency")

def update_residency(residency_id, data):
    """
    Update an existing residency.
    Admins can update the details of a residency.
    """
    try:
        collection = current_app.db["residencies"]
        result = collection.update_one({"_id": ObjectId(residency_id)}, {"$set": data})
        return result.matched_count > 0
    except Exception as e:
        current_app.logger.error(f"Error updating residency: {e}")
        return False

def delete_residency(residency_id):
    """
    Delete a residency by its ID.
    Admins can delete a residency.
    """
    try:
        collection = current_app.db["residencies"]
        result = collection.delete_one({"_id": ObjectId(residency_id)})
        return result.deleted_count > 0
    except Exception as e:
        current_app.logger.error(f"Error deleting residency: {e}")
        return False

# Student-related functions for applying to residencies

def get_student_applications(student_id):
    """
    Get all applications submitted by a specific student.
    Accessible by students to view their own applications.
    """
    try:
        collection = current_app.db["student_data"]
        applications = list(collection.find({"student_id": student_id}))
        for application in applications:
            application["_id"] = str(application["_id"])
        return applications
    except Exception as e:
        current_app.logger.error(f"Error fetching student applications: {e}")
        return []

def insert_student_application(application_data):
    """
    Insert a student application for a residency.
    Students can apply for residencies.
    """
    try:
        collection = current_app.db["student_data"]
        return str(collection.insert_one(application_data).inserted_id)
    except Exception as e:
        current_app.logger.error(f"Error inserting student application: {e}")
        raise RuntimeError("Failed to insert application")

from bson import ObjectId

def delete_student_application(student_id, application_id):
    """
    Delete a student's application.
    Students can delete their own applications.
    """
    try:
        collection = current_app.db["student_data"]
        
        # Delete the document based on application_id and username (student_id)
        result = collection.delete_one({"_id": ObjectId(application_id), "username": student_id})
        
        # Log how many applications were deleted
        current_app.logger.info(f"Deleted {result.deleted_count} application(s) for {student_id} with ID: {application_id}")
        
        return result.deleted_count > 0
    except Exception as e:
        current_app.logger.error(f"Error deleting student application: {e}")
        return False

