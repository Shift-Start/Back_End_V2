from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from datetime import datetime
from .models import Reward

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

# عرض وإنشاء المكافآت
class RewardListCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            created_reward = Reward.add_reward(data)
            created_reward = convert_object_id_to_string(created_reward)
            return Response(created_reward, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        rewards = Reward.collection.find()
        reward_list = [convert_object_id_to_string(reward) for reward in rewards]
        return Response(reward_list, status=status.HTTP_200_OK)

# تحديث المكافآت
class RewardUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, reward_id):
        data = request.data
        try:
            Reward.update_reward(ObjectId(reward_id), data)
            updated_reward = Reward.collection.find_one({"_id": ObjectId(reward_id)})
            updated_reward = convert_object_id_to_string(updated_reward)
            return Response(updated_reward, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# حذف المكافآت
class RewardDeleteView(APIView):
    permission_classes = [AllowAny]
    
    def delete(self, request, reward_id):
        try:
            Reward.delete_reward(ObjectId(reward_id))
            return Response({"message": "Reward deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
