
import bcrypt
from pymongo import MongoClient
from datetime import datetime

# الاتصال بقاعدة البيانات MongoDB
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client['Shift-Start-db']

class User:
    collection = db['users']  # تحديد مجموعة المستخدمين

    @staticmethod
    def create_user(data):
        """
        إنشاء مستخدم جديد.
        """
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        data['points'] = data.get('points', 0)  # النقاط الافتراضية
        data['profile_image'] = data.get('profile_image', None)  # صورة البروفايل
        User.collection.insert_one(data)
        return data

    @staticmethod
    def get_user_by_email(email):
        """
        البحث عن مستخدم بواسطة البريد الإلكتروني.
        """
        return User.collection.find_one({"email": email})

    @staticmethod
    def get_user_by_username(username):
        """
        البحث عن مستخدم بواسطة اسم المستخدم.
        """
        return User.collection.find_one({"username": username})

    @staticmethod
    def check_password(hashed_password, raw_password):
        """
        التحقق من كلمة المرور باستخدام bcrypt.
        """
        return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def get_all_users_sorted_by_points():
        """
        جلب جميع المستخدمين مرتبين حسب النقاط (تنازليًا).
        """
        return list(User.collection.find({}, {"_id": 0, "username": 1, "points": 1, "profile_image": 1}).sort("points", -1))

    @staticmethod
    def update_user_points(user_id, new_points):
        """
        تحديث نقاط المستخدم.
        """
        return User.collection.update_one(
            {"_id": user_id},
            {"$set": {"points": new_points, "updated_at": datetime.utcnow()}}
        )

    @staticmethod
    def delete_user(user_id):
        """
        حذف مستخدم بناءً على معرف المستخدم.
        """
        return User.collection.delete_one({"_id": user_id})
