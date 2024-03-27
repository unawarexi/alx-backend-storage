#!/usr/bin/env python3
""" Log stats """

from pymongo import MongoClient

def log_stats():
    """ Log stats """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    total_logs = logs_collection.count_documents({})
    print("{} logs".format(total_logs))

    methods = logs_collection.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}}
    ])
    print("Methods:")
    for method in methods:
        print("\tmethod {}: {}".format(method["_id"], method["count"]))

    status_check = logs_collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status_check))

    ips = logs_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    print("IPs:")
    for ip in ips:
        print("\t{}: {}".format(ip["_id"], ip["count"]))

if __name__ == "__main__":
    log_stats()
