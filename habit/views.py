from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from habit.models import Habit  # نستورد الكلاس الخاص بالموديل
from habit.serializers import HabitSerializer  # نستورد السيريالايزر

class HabitListCreateView(APIView):
    """
    عرض جميع العادات أو إنشاء عادة جديدة
    """
    def get(self, request):
        habits = Habit.collection.find()
        serialized_habits = [HabitSerializer(habit).data for habit in habits]
        return Response(serialized_habits, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            Habit.create_habit(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HabitDetailView(APIView):
    """
    عرض، تعديل أو حذف عادة بناءً على الـ ID
    """
    def get_object(self, habit_id):
        habit = Habit.collection.find_one({"_id": ObjectId(habit_id)})
        if not habit:
            return None
        return habit

    def get(self, request, habit_id):
        habit = self.get_object(habit_id)
        if not habit:
            return Response({"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND)
        serialized_habit = HabitSerializer(habit).data
        return Response(serialized_habit, status=status.HTTP_200_OK)

    def put(self, request, habit_id):
        habit = self.get_object(habit_id)
        if not habit:
            return Response({"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            Habit.update_habit(ObjectId(habit_id), serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, habit_id):
        habit = self.get_object(habit_id)
        if not habit:
            return Response({"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND)
        Habit.delete_habit(ObjectId(habit_id))
        return Response({"message": "Habit deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
