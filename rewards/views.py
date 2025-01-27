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