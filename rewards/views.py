from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from .models import Reward, UserReward

# دالة مساعدة لتحويل ObjectId إلى نصوص
def convert_object_id_to_string(data):
    if isinstance(data, list):
        for item in data:
            convert_object_id_to_string(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, (dict, list)):
                convert_object_id_to_string(value)
    return data

class RewardCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        name = data.get("name")
        description = data.get("description")
        points_required = data.get("points_required")

        if not name or not points_required:
            return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            Reward.create_reward(name, description, points_required)
            return Response({"message": "Reward created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RewardUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, reward_id):
        data = request.data
        name = data.get("name")
        description = data.get("description")
        points_required = data.get("points_required")

        try:
            Reward.update_reward(reward_id, name, description, points_required)
            return Response({"message": "Reward updated successfully"}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RewardDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, reward_id):
        try:
            Reward.delete_reward(reward_id)
            return Response({"message": "Reward deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RewardListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            rewards = Reward.list_rewards()
            return Response({"rewards": rewards}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserRewardView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id")
        total_points = request.data.get("total_points")

        if not user_id or not total_points:
            return Response({"error": "User ID and total points are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # التحقق من المكافآت التي يمكن منحها للمستخدم بناءً على النقاط
            available_rewards = UserReward.check_user_reward(user_id, total_points)
            
            # التحقق من المكافآت التي حصل عليها المستخدم مسبقًا
            claimed_rewards = UserReward.collection.find({"user_id": user_id})
            claimed_reward_ids = {reward["reward_id"] for reward in claimed_rewards}

            # تصفية المكافآت الجديدة فقط
            new_rewards = [
                reward for reward in available_rewards
                if reward["_id"] not in claimed_reward_ids
            ]

            if not new_rewards:
                return Response({"message": "No new rewards available."}, status=status.HTTP_200_OK)

            # منح المكافآت الجديدة فقط
            for reward in new_rewards:
                UserReward.grant_user_reward(user_id, reward["_id"], reward["points_required"])

            return Response({"message": "Rewards granted successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserRewardsListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        try:
            # جلب كافة الجوائز المرتبطة بالمستخدم
            user_rewards = UserReward.collection.find({"user_id": user_id})
            user_rewards_list = []

            for reward in user_rewards:
                # تحويل _id إلى string وإضافة تفاصيل الجائزة إلى القائمة
                reward["_id"] = str(reward["_id"])
                reward_details = Reward.collection.find_one({"_id": ObjectId(reward["reward_id"])})
                if reward_details:
                    reward_details["_id"] = str(reward_details["_id"])
                    user_rewards_list.append({
                        "reward_id": reward["reward_id"],
                        "reward_name": reward_details.get("name"),
                        "description": reward_details.get("description"),
                        "points_paid": reward["points_paid"],
                        "granted_at": reward["granted_at"],
                    })

            return Response({"user_rewards": user_rewards_list}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserRewardHistoryView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        try:
            # جلب كافة الجوائز الخاصة بالمستخدم
            rewards = UserReward.get_rewards_by_user(user_id)
            if not rewards:
                return Response({"message": "No rewards found for this user."}, status=status.HTTP_200_OK)
            
            return Response({"rewards": rewards}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
