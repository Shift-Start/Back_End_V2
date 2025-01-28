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
            reward["_id"] = str(reward["_id"])
            rewards_list.append(reward)
        return rewards_list

class UserReward:
    collection = db["user_rewards"]

    @staticmethod
    def grant_user_reward(user_id, reward_id, points_paid):
        # التحقق إذا كان المستخدم قد حصل على هذه الجائزة من قبل
        existing_reward = UserReward.collection.find_one({"user_id": user_id, "reward_id": reward_id})
        if existing_reward:
            raise ValueError(f"User has already received reward with ID {reward_id}")

        user_reward = {
            "user_id": user_id,
            "reward_id": reward_id,
            "points_paid": points_paid,
            "granted_at": datetime.utcnow(),
        }
        UserReward.collection.insert_one(user_reward)

    @staticmethod
    def check_user_reward(user_id, total_points):
        # المكافآت المتاحة بناءً على النقاط
        rewards = Reward.collection.find({"points_required": {"$lte": total_points}})
        user_rewards = []

        for reward in rewards:
            # التحقق من أن المستخدم لم يحصل على الجائزة مسبقًا
            existing_reward = UserReward.collection.find_one({"user_id": user_id, "reward_id": reward["_id"]})
            if not existing_reward:  # فقط أضف المكافآت التي لم يحصل عليها المستخدم
                reward["_id"] = str(reward["_id"])  # تحويل _id إلى string
                user_rewards.append(reward)

        return user_rewards

    @staticmethod
    def get_rewards_by_user(user_id):
        # جلب كافة الجوائز التي حصل عليها المستخدم.
        user_rewards = UserReward.collection.find({"user_id": user_id})
        rewards_list = []

        for user_reward in user_rewards:
            reward_details = Reward.collection.find_one({"_id": ObjectId(user_reward["reward_id"])})
            if reward_details:
                rewards_list.append({
                    "reward_name": reward_details.get("name"),
                    "description": reward_details.get("description"),
                    "points_required": reward_details.get("points_required"),
                    "granted_at": user_reward["granted_at"]
                })
        return rewards_list
