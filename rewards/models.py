from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
import re

from notifications.models import Notification

# الاتصال بقاعدة البيانات
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client['Shift-Start-db']

class Reward:
    collection = db["rewards"]  # جدول المكافآت العامة

    @staticmethod
    def create_reward(name, description, points_required):
        reward = {
            "name": name,
            "description": description,
            "points_required": points_required,
            "created_at": datetime.utcnow()
        }
        Reward.collection.insert_one(reward)

    @staticmethod
    def update_reward(reward_id, name=None, description=None, points_required=None):
        # تحقق من وجود المكافأة أولاً
        reward = Reward.collection.find_one({"_id": ObjectId(reward_id)})
        if not reward:
            raise ValueError("Reward not found.")
        
        # تعديل مكافأة موجودة.
        updates = {}
        if name:
            updates["name"] = name
        if description:
            updates["description"] = description
        if points_required:
            updates["points_required"] = points_required

        if not updates:
            raise ValueError("No fields to update.")

        # تطبيق التحديثات
        Reward.collection.update_one({"_id": ObjectId(reward_id)}, {"$set": updates})
        
    @staticmethod
    def delete_reward(reward_id):
        # تحقق من وجود المكافأة قبل الحذف
        reward = Reward.collection.find_one({"_id": ObjectId(reward_id)})
        if not reward:
            raise ValueError("The reward does not exist.")
        
        # حذف المكافأة
        Reward.collection.delete_one({"_id": ObjectId(reward_id)})

    @staticmethod
    def list_rewards():
        # عرض جميع المكافآت.
        rewards = Reward.collection.find({}, {"_id": 1, "name": 1, "description": 1, "points_required": 1})
        rewards_list = []
        for reward in rewards:
            reward["_id"] = str(reward["_id"])  # تحويل ObjectId إلى سلسلة نصية
            rewards_list.append(reward)
        return rewards_list
