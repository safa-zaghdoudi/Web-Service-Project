from flask import current_app
from bson.objectid import ObjectId
from flask_pymongo import PyMongo



mongo = PyMongo()


# Residency-related functions
def get_all_residencies():
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
    try:
        collection = current_app.db["residencies"]
        return str(collection.insert_one(data).inserted_id)
    except Exception as e:
        current_app.logger.error(f"Error inserting residency: {e}")
        raise RuntimeError("Failed to insert residency")

def update_residency_in_db(residency_id, data):
    try:
        collection = current_app.db["residencies"]
        result = collection.update_one({"_id": ObjectId(residency_id)}, {"$set": data})
        return result.matched_count > 0
    except Exception as e:
        current_app.logger.error(f"Error updating residency: {e}")
        return False

def delete_residency_from_db(residency_id):
    try:
        collection = current_app.db["residencies"]
        result = collection.delete_one({"_id": ObjectId(residency_id)})
        return result.deleted_count > 0
    except Exception as e:
        current_app.logger.error(f"Error deleting residency: {e}")
        return False


# Block-related functions

def get_blocks_by_residency(residency_id):
    """
    Fetch all blocks associated with a specific residency.
    """
    try:
        collection = current_app.db["blocks"]
        blocks = list(collection.find({"residency_id": ObjectId(residency_id)}))
        for block in blocks:
            block["block_id"] = str(block["_id"])  # Use block_id instead of _id
            del block["_id"]  # Remove the original _id field
            block["residency_id"] = str(block["residency_id"])
        return blocks
    except Exception as e:
        current_app.logger.error(f"Error fetching blocks by residency: {e}")
        return []



def get_block_by_id(block_id):
    """
    Fetch a block by its block_id.
    """
    try:
        collection = current_app.db["blocks"]
        block = collection.find_one({"_id": ObjectId(block_id)})
        if block:
            block["block_id"] = str(block["_id"])  # Use block_id instead of _id
            del block["_id"]  # Remove the original _id field
            block["residency_id"] = str(block["residency_id"])
        return block
    except Exception as e:
        current_app.logger.error(f"Error fetching block by block_id: {e}")
        return None


def insert_block(data):
    """
    Insert a new block into the database.
    """
    try:
        collection = current_app.db["blocks"]
        result = collection.insert_one(data)
        return str(result.inserted_id)
    except Exception as e:
        current_app.logger.error(f"Error inserting block: {e}")
        raise RuntimeError("Failed to insert block")


def update_block_by_id(block_id, data):
    """
    Update a block by its block_id.
    """
    try:
        collection = current_app.db["blocks"]
        result = collection.update_one({"_id": ObjectId(block_id)}, {"$set": data})
        return result.matched_count > 0
    except Exception as e:
        current_app.logger.error(f"Error updating block by block_id: {e}")
        return False


def delete_block_by_id(block_id):
    """
    Delete a block by its block_id.
    """
    try:
        collection = current_app.db["blocks"]
        result = collection.delete_one({"_id": ObjectId(block_id)})
        return result.deleted_count > 0
    except Exception as e:
        current_app.logger.error(f"Error deleting block by block_id: {e}")
        return False


# Room-related functions

def get_rooms_by_block(block_id):
    """
    Fetch all rooms associated with a specific block.
    """
    try:
        collection = current_app.db["rooms"]
        rooms = list(collection.find({"block_id": ObjectId(block_id)}))
        for room in rooms:
            room["room_id"] = str(room["_id"])  # Use room_id instead of _id
            del room["_id"]  # Remove the original _id field
            room["block_id"] = str(room["block_id"])
        return rooms
    except Exception as e:
        current_app.logger.error(f"Error fetching rooms by block: {e}")
        return []

def get_room_by_id(room_id):
    """
    Fetch a room by its room_id.
    """
    try:
        collection = current_app.db["rooms"]
        room = collection.find_one({"_id": ObjectId(room_id)})
        if room:
            room["room_id"] = str(room["_id"])  # Use room_id instead of _id
            del room["_id"]  # Remove the original _id field
            room["block_id"] = str(room["block_id"])
        return room
    except Exception as e:
        current_app.logger.error(f"Error fetching room by room_id: {e}")
        return None

def insert_room(data):
    """
    Insert a new room into the database (with block_id as foreign key).
    """
    try:
        collection = current_app.db["rooms"]
        result = collection.insert_one(data)
        return str(result.inserted_id)
    except Exception as e:
        current_app.logger.error(f"Error inserting room: {e}")
        raise RuntimeError("Failed to insert room")

def update_room_by_id(room_id, data):
    """
    Update a room by its room_id.
    """
    try:
        collection = current_app.db["rooms"]
        result = collection.update_one({"_id": ObjectId(room_id)}, {"$set": data})
        return result.matched_count > 0
    except Exception as e:
        current_app.logger.error(f"Error updating room by room_id: {e}")
        return False

def delete_room_by_id(room_id):
    """
    Delete a room by its room_id.
    """
    try:
        collection = current_app.db["rooms"]
        result = collection.delete_one({"_id": ObjectId(room_id)})
        return result.deleted_count > 0
    except Exception as e:
        current_app.logger.error(f"Error deleting room by room_id: {e}")
        return False

# Application-related functions
def get_all_applications():
    try:
        collection = current_app.db["applications"]
        applications = list(collection.find())
        for application in applications:
            application["_id"] = str(application["_id"])
        return applications
    except Exception as e:
        current_app.logger.error(f"Error fetching applications: {e}")
        return []

def get_application_by_id(application_id):
    try:
        collection = current_app.db["applications"]
        application = collection.find_one({"_id": ObjectId(application_id)})
        if application:
            application["_id"] = str(application["_id"])
        return application
    except Exception as e:
        current_app.logger.error(f"Error fetching application by ID: {e}")
        return None

def insert_application(data):
    try:
        collection = current_app.db["applications"]
        # Assign a custom application_id instead of using MongoDB's default _id
        application_id = str(ObjectId())  # generate a custom ID if needed
        data["application_id"] = application_id  # Set the custom ID in the document
        collection.insert_one(data)
        return application_id
    except Exception as e:
        current_app.logger.error(f"Error inserting application: {e}")
        raise RuntimeError("Failed to insert application")

def delete_application(application_id):
    try:
        collection = current_app.db["applications"]
        # Log the application_id to ensure it's being passed correctly
        current_app.logger.info(f"Attempting to delete application with ID: {application_id}")
        result = collection.delete_one({"application_id": application_id})
        if result.deleted_count == 0:
            current_app.logger.warning(f"No application found with ID: {application_id}")
        return result.deleted_count > 0
    except Exception as e:
        current_app.logger.error(f"Error deleting application: {e}")
        raise RuntimeError("Failed to delete application")
    
# Review-related functions
def get_all_reviews():
    try:
        collection = current_app.db["reviews"]
        reviews = list(collection.find())
        for review in reviews:
            review["_id"] = str(review["_id"])
        return reviews
    except Exception as e:
        current_app.logger.error(f"Error fetching reviews: {e}")
        return []

def get_review_by_id(review_id):
    try:
        collection = current_app.db["reviews"]
        review = collection.find_one({"_id": ObjectId(review_id)})
        if review:
            review["_id"] = str(review["_id"])
        return review
    except Exception as e:
        current_app.logger.error(f"Error fetching review by ID: {e}")
        return None

def insert_review(data):
    try:
        collection = current_app.db["reviews"]
        # Assign a custom review_id instead of using MongoDB's default _id
        review_id = str(ObjectId())  # generate a custom ID if needed
        data["review_id"] = review_id  # Set the custom ID in the document
        collection.insert_one(data)
        return review_id
    except Exception as e:
        current_app.logger.error(f"Error inserting review: {e}")
        raise RuntimeError("Failed to insert review")

def delete_review(review_id):
    try:
        collection = current_app.db["reviews"]
        # Log the review_id to ensure it's being passed correctly
        current_app.logger.info(f"Attempting to delete review with ID: {review_id}")
        result = collection.delete_one({"review_id": review_id})
        if result.deleted_count == 0:
            current_app.logger.warning(f"No review found with ID: {review_id}")
        return result.deleted_count > 0
    except Exception as e:
        current_app.logger.error(f"Error deleting review: {e}")
        raise RuntimeError("Failed to delete review")