# import bcrypt
# from pymongo import MongoClient
# from datetime import datetime

# # إعداد قاعدة البيانات
# client = MongoClient("mongodb://127.0.0.1:27017/")
# db = client['Shift-Start-db']

# # جدول المستخدمين
# class User:
#     collection = db['users']

#     @staticmethod
#     def create_user(data):
#         data['created_at'] = datetime.utcnow()
#         data['updated_at'] = datetime.utcnow()
#         data['profile_picture'] = data.get('profile_picture', None)  # صورة البروفايل
#         data['points'] = 0  # النقاط الافتراضية
#         User.collection.insert_one(data)
#         return data

#     @staticmethod
#     def get_user_by_id(user_id):
#         return User.collection.find_one({"_id": user_id})

#     @staticmethod
#     def update_user(user_id, updated_data):
#         updated_data['updated_at'] = datetime.utcnow()
#         User.collection.update_one({"_id": user_id}, {"$set": updated_data})

#     @staticmethod
#     def delete_user(user_id):
#         User.collection.delete_one({"_id": user_id})

#     @staticmethod
#     def get_user_by_email(email):
#         return User.collection.find_one({"email": email})

#     @staticmethod
#     def get_user_by_username(username):
#         return User.collection.find_one({"username": username})

#     @staticmethod
#     def check_password(hashed_password, raw_password):
#         return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))

#     @staticmethod
#     def update_user(user_id, updated_data):
#      updated_data['updated_at'] = datetime.utcnow()
#      User.collection.update_one({"_id": user_id}, {"$set": updated_data})
import bcrypt
from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId

# إعداد قاعدة البيانات
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client['Shift-Start-db']

# جدول المستخدمين
class User:
    collection = db['users']

    @staticmethod
    def create_user(data):
        # التحقق من وجود البريد الإلكتروني أو اسم المستخدم
        if User.get_user_by_email(data['email']):
            raise ValueError("Email already exists")
        if User.get_user_by_username(data['username']):
            raise ValueError("Username already exists")
        
        # إضافة تاريخ الإنشاء والتحديث
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        
        #إضافة device_token لكل مستخدم بخصوص الاشعارات
        data['device_token'] = data.get('device_token', None)
        
        # تعيين صورة البروفايل كنظام افتراضي (None) والنقاط (0)
        data['profile_picture'] = None
        data['points'] = 0
        
        # تشفير كلمة المرور
        data['password'] = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # إدخال المستخدم في قاعدة البيانات
        User.collection.insert_one(data)
        return data

    @staticmethod
    def get_user_by_id(user_id):
        return User.collection.find_one({"_id": ObjectId(user_id)})

    @staticmethod
    def get_user_by_email(email):
        return User.collection.find_one({"email": email})

    @staticmethod
    def get_user_by_username(username):
        return User.collection.find_one({"username": username})

    @staticmethod
    def update_user(user_id, updated_data):
        # إضافة تاريخ التحديث
        updated_data['updated_at'] = datetime.utcnow()
        
        # تحديث البيانات في قاعدة البيانات
        User.collection.update_one({"_id": ObjectId(user_id)}, {"$set": updated_data})

    @staticmethod
    def delete_user(user_id):
        User.collection.delete_one({"_id": ObjectId(user_id)})

    @staticmethod
    def check_password(hashed_password, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))

    @staticmethod
    def update_password(user_id, new_password):
        hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        User.update_user(user_id, {'password': hashed_password})

    @staticmethod
    def update_profile(user_id, profile_data):
        # تحديث البيانات الخاصة بالبروفايل مثل الصورة أو النقاط
        User.update_user(user_id, profile_data)




# جدول النشاطات
class ActivityLog:
    collection = db['activity_logs']

    @staticmethod
    def log_action(user_id, action):
        log_data = {
            "user_id": user_id,
            "action": action,
            "timestamp": datetime.utcnow()
        }
        ActivityLog.collection.insert_one(log_data)
        return log_data

    @staticmethod
    def get_logs_by_user(user_id):
        return list(ActivityLog.collection.find({"user_id": user_id}))


# جدول النقاط والترتيب
class Leaderboard:
    collection = db['leaderboard']

    @staticmethod
    def add_points(user_id, points, reason):
        existing_entry = Leaderboard.collection.find_one({"user_id": user_id})
        if existing_entry:
            new_points = existing_entry["points"] + points
            Leaderboard.collection.update_one(
                {"user_id": user_id},
                {"$set": {"points": new_points, "updated_at": datetime.utcnow()}}
            )
        else:
            Leaderboard.collection.insert_one({
                "user_id": user_id,
                "points": points,
                "reason": reason,
                "updated_at": datetime.utcnow(),
                "created_at": datetime.utcnow()
            })

    @staticmethod
    def get_leaderboard():
        return list(Leaderboard.collection.find().sort("points", -1))


# جدول التوصيات
class Recommendations:
    collection = db['recommendations']

    @staticmethod
    def create_recommendation(user_id, content):
        recommendation_data = {
            "user_id": user_id,
            "content": content,
            "created_at": datetime.utcnow()
        }
        Recommendations.collection.insert_one(recommendation_data)
        return recommendation_data

    @staticmethod
    def get_all_recommendations():
        return list(Recommendations.collection.find())


# جدول الإشعارات
class Notifications:
    collection = db['notifications']

    @staticmethod
    def create_notification(user_id, message, note):
        notification_data = {
            "user_id": user_id,
            "message": message,
            "note": note,
            "is_read": False,
            "created_at": datetime.utcnow()
        }
        Notifications.collection.insert_one(notification_data)
        return notification_data

    @staticmethod
    def mark_as_read(notification_id):
        Notifications.collection.update_one({"_id": notification_id}, {"$set": {"is_read": True}})


# جدول المكافآت
class Reward:
    collection = db['rewards']

    @staticmethod
    def create_reward(user_id, reward_name, description, points_required):
        reward_data = {
            "user_id": user_id,
            "reward_name": reward_name,
            "description": description,
            "points_required": points_required,
            "created_at": datetime.utcnow()
        }
        Reward.collection.insert_one(reward_data)
        return reward_data

    @staticmethod
    def get_rewards_by_user(user_id):
        return list(Reward.collection.find({"user_id": user_id}))


# جدول التقارير
class Reports:
    collection = db['reports']  # تحديد قاعدة البيانات المناسبة

    @staticmethod
    def create_report(user_id, report_content):
        """إنشاء تقرير جديد"""
        report_data = {
            "user_id": user_id,  # معرف المستخدم
            "report_content": report_content,  # محتوى التقرير
            "created_at": datetime.utcnow()  # تاريخ الإنشاء (بالتوقيت العالمي)
        }
        Reports.collection.insert_one(report_data)  # إضافة التقرير إلى قاعدة البيانات
        return report_data  # إرجاع التقرير الجديد

    @staticmethod
    def get_reports_by_user(user_id):
        """الحصول على التقارير الخاصة بمستخدم معين"""
        return list(Reports.collection.find({"user_id": user_id}))
