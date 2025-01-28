from pymongo import MongoClient

def test_mongo_connection():
    try:
        # Replace with your connection string
        client = MongoClient("mongodb+srv://zaghdoudisafe:4T6p7FyUp8DudtEn@cluster0.pgrad.mongodb.net")
        db = client["residency_db"]
        collection = db["residencies"]

        print("Connected to MongoDB.")
        print("Database:", db.name)
        print("Collection:", collection.name)

        # Fetch records
        records = list(collection.find())
        print(f"Number of records retrieved: {len(records)}")
        for record in records:
            print(record)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    print("Testing MongoDB connection and queries...")
    test_mongo_connection()


