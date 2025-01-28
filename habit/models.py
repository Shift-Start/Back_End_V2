from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId


client = MongoClient("mongodb://127.0.0.1:27017/")
db = client['Shift-Start-db']


class Habit:
    collection = db['habits']

    @staticmethod
    def create_habit(data):
        # تحويل start_date و end_date إلى datetime
        if 'start_date' in data:
            data['start_date'] = datetime.combine(data['start_date'], datetime.min.time())
        if 'end_date' in data:
            data['end_date'] = datetime.combine(data['end_date'], datetime.min.time())

        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        Habit.collection.insert_one(data)
        return data

    @staticmethod
    def get_habit_by_id(habit_id):
        return Habit.collection.find_one({"_id": ObjectId(habit_id)})

    @staticmethod
    def update_habit(habit_id, data):
        data['updated_at'] = datetime.utcnow()
        Habit.collection.update_one({"_id": ObjectId(habit_id)}, {"$set": data})

    @staticmethod
    def delete_habit(habit_id):
        Habit.collection.delete_one({"_id": ObjectId(habit_id)})




class Challenge:
    collection = db['challenges']

    @staticmethod
    def create_challenge(data):
        # تحويل start_date و end_date إلى datetime
        if 'start_date' in data:
            data['start_date'] = datetime.combine(data['start_date'], datetime.min.time())
        if 'end_date' in data:
            data['end_date'] = datetime.combine(data['end_date'], datetime.min.time())

        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        Challenge.collection.insert_one(data)
        return data

    @staticmethod
    def get_challenge_by_id(challenge_id):
        return Challenge.collection.find_one({"_id": ObjectId(challenge_id)})

    @staticmethod
    def update_challenge(challenge_id, data):
        data['updated_at'] = datetime.utcnow()
        Challenge.collection.update_one({"_id": ObjectId(challenge_id)}, {"$set": data})

    @staticmethod
    def delete_challenge(challenge_id):
        Challenge.collection.delete_one({"_id": ObjectId(challenge_id)})
