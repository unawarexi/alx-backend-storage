def top_students(mongo_collection):
    students = mongo_collection.aggregate([
        {"$unwind": "$topics"},
        {"$group": {
            "_id": "$name",
            "averageScore": {"$avg": "$topics.score"}
        }},
        {"$sort": {"averageScore": -1}}
    ])
    return list(students)
