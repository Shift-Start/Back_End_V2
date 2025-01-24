from pymongo import MongoClient
from datetime import datetime
import re

# الاتصال بقاعدة البيانات
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client['Shift-Start-db']

# جدول المكافآت (Rewards)
class Reward:
    collection = db['rewards']

    @staticmethod
    def add_reward(data):
        # إضافة مكافأة جديدة إلى جدول المكافآت.
        if not data.get('reward_name') or not re.match("^[A-Za-z\u0600-\u06FF ]*$", data['reward_name']):
            raise ValueError("اسم المكافأة يجب أن يحتوي على حروف فقط (إنجليزية أو عربية).")
        if not isinstance(data.get('points_required'), int) or data['points_required'] <= 0:
            raise ValueError("عدد النقاط المطلوب يجب أن يكون رقمًا صحيحًا أكبر من 0.")

        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        data['achieved'] = False  # القيمة الافتراضية عند إضافة مكافأة جديدة
        data['achievement_date'] = None
        data['tasks_completed'] = 0
        data['progress'] = 0.0
        Reward.collection.insert_one(data)
        return data

    @staticmethod
    def get_reward_by_user(user_id):
        # جلب جميع المكافآت الخاصة بمستخدم معين.
        return list(Reward.collection.find({"user_id": user_id}))

    @staticmethod
    def update_reward(reward_id, data):
        # تحديث بيانات مكافأة معينة.
        if not data.get('reward_name') or not re.match("^[A-Za-z\u0600-\u06FF ]*$", data['reward_name']):
            raise ValueError("اسم المكافأة يجب أن يحتوي على حروف فقط (إنجليزية أو عربية).")
        if not isinstance(data.get('points_required'), int) or data['points_required'] <= 0:
            raise ValueError("عدد النقاط المطلوب يجب أن يكون رقمًا صحيحًا أكبر من 0.")
            
        data['updated_at'] = datetime.utcnow()
        Reward.collection.update_one({"_id": reward_id}, {"$set": data})

    @staticmethod
    def delete_reward(reward_id):
        # حذف مكافأة معينة من الجدول.
        reward = Reward.collection.find_one({"_id": reward_id})
        if not reward:
            raise ValueError("المكافأة غير موجودة.")
        Reward.collection.delete_one({"_id": reward_id})
