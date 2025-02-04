from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client['Shift-Start-db']

class Settings:
    collection = db['settings']

    @staticmethod
    def create_settings(user_id):
        """ إنشاء إعدادات افتراضية للمستخدم الجديد إذا لم تكن موجودة """
        settings_data = {
            "user_id": ObjectId(user_id),
            "remember_key": None,
            "notification_value": True,
            "default_settings": True,
            "dark_mode": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        Settings.collection.insert_one(settings_data)
        return settings_data

    @staticmethod
    def get_settings_by_user(user_id):
        """ جلب إعدادات المستخدم """
        return Settings.collection.find_one({"user_id": ObjectId(user_id)})

    @staticmethod
    def update_settings(user_id, data):
        """ تحديث إعدادات المستخدم """
        data['updated_at'] = datetime.utcnow()
        Settings.collection.update_one({"user_id": ObjectId(user_id)}, {"$set": data})

    @staticmethod
    def delete_settings(user_id):
        """ حذف إعدادات المستخدم """
        Settings.collection.delete_one({"user_id": ObjectId(user_id)})
