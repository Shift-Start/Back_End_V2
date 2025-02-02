from pymongo import MongoClient
from datetime import datetime

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

