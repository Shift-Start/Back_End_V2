from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
<<<<<<< HEAD
from habit.models import Habit ,Challenge  # نستورد الكلاس الخاص بالموديل
from habit.serializers import HabitSerializer  # نستورد السيريالايزر
from rest_framework.permissions import AllowAny
from datetime import datetime


class HabitListCreateView(APIView):
    permission_classes = [AllowAny]
    """
    عرض جميع العادات أو إنشاء عادة جديدة
    """

    def get(self, request):
        habits = Habit.collection.find()
        serialized_habits = []
        now = datetime.utcnow()  # الوقت الحالي
        
        for habit in habits:
            # حساب إجمالي المدة الزمنية
            total_days = (habit['end_date'] - habit['start_date']).days + 1
            # حساب المدة الزمنية المنقضية منذ بداية العادة وحتى الآن
            elapsed_days = (now - habit['start_date']).days

            # حساب نسبة الإنجاز بناءً على المدة المنقضية
            if elapsed_days >= total_days:
                completion_rate = "100%"  # العادة اكتملت بالكامل
            else:
                completion_rate = f"{(elapsed_days / total_days) * 100:.2f}%"  # إضافة الـ% مع تنسيق الرقم

            # إضافة لون الحالة
            habit_status_color = "green" if habit['status'] else "yellow"

            # إضافة البيانات إلى المسلسل
            habit_data = HabitSerializer(habit).data
            habit_data['completion_rate'] = completion_rate
            habit_data['status_color'] = habit_status_color
            serialized_habits.append(habit_data)

=======
from habit.models import Habit  # نستورد الكلاس الخاص بالموديل
from habit.serializers import HabitSerializer  # نستورد السيريالايزر

class HabitListCreateView(APIView):
    """
    عرض جميع العادات أو إنشاء عادة جديدة
    """
    def get(self, request):
        habits = Habit.collection.find()
        serialized_habits = [HabitSerializer(habit).data for habit in habits]
>>>>>>> 769b9b4 (Add user features)
        return Response(serialized_habits, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
<<<<<<< HEAD
            # إنشاء العادة باستخدام البيانات المرسلة
=======
>>>>>>> 769b9b4 (Add user features)
            Habit.create_habit(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


<<<<<<< HEAD

class DailyUpdatesView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        now = datetime.utcnow()  # الوقت الحالي
        start_of_day = datetime(now.year, now.month, now.day)  # بداية اليوم
        end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)  # نهاية اليوم

        # البحث عن العادات التي تم تحديثها اليوم وتخص المستخدم الحالي
        habits = Habit.collection.find({
            "updated_at": {"$gte": start_of_day, "$lte": end_of_day},
            "user_id": request.user.id  # تصفية حسب المستخدم
        })

        # تسلسل البيانات
        serialized_habits = []
        for habit in habits:
            habit_data = HabitSerializer(habit).data
            serialized_habits.append(habit_data)

        return Response(serialized_habits, status=status.HTTP_200_OK)

class HabitSortView(APIView):
    permission_classes = [AllowAny]
    """
    API مستقل لفرز العادات بناءً على معايير محددة.
    """

    def get(self, request):
        # الحصول على معيار الفرز واتجاهه من معاملات الطلب
        sort_by = request.query_params.get('sort_by', 'priority')  # افتراضيًا: الأولوية
        order = request.query_params.get('order', 'asc')  # افتراضيًا: تصاعدي

        # جلب جميع العادات من قاعدة البيانات
        habits = Habit.collection.find()

        # تطبيق عملية الفرز بناءً على المعيار المطلوب
        if sort_by == 'priority':
            habits = sorted(habits, key=lambda h: h.get('priority', 0), reverse=(order == 'desc'))
        elif sort_by == 'status':
            habits = sorted(habits, key=lambda h: h.get('status', False), reverse=(order == 'desc'))
        elif sort_by == 'completion_rate':
            def calculate_completion_rate(h):
                total_days = (h['end_date'] - h['start_date']).days + 1
                elapsed_days = (datetime.utcnow() - h['start_date']).days
                return min(elapsed_days / total_days, 1.0) if total_days > 0 else 0.0

            habits = sorted(habits, key=calculate_completion_rate, reverse=(order == 'desc'))
        else:
            return Response({"error": "Invalid sort_by parameter"}, status=status.HTTP_400_BAD_REQUEST)

        # تسلسل البيانات وإرجاعها
        serialized_habits = []
        for habit in habits:
            habit_data = HabitSerializer(habit).data
            serialized_habits.append(habit_data)

        return Response(serialized_habits, status=status.HTTP_200_OK)

class HabitDetailView(APIView):
    permission_classes = [AllowAny]
    """
    عرض تقدم المستخدم وإحصائيات العادة مع وظائف تعديل وحذف.
=======
class HabitDetailView(APIView):
    """
    عرض، تعديل أو حذف عادة بناءً على الـ ID
>>>>>>> 769b9b4 (Add user features)
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
<<<<<<< HEAD

        # حساب نسبة الإنجاز
        total_days = (habit['end_date'] - habit['start_date']).days + 1
        elapsed_days = (datetime.utcnow() - habit['start_date']).days
        completed_days = min(elapsed_days, total_days) if elapsed_days > 0 else 0
        completion_rate = (completed_days / total_days) * 100 if total_days > 0 else 0

        # إنشاء رسالة تحفيزية بناءً على نسبة الإنجاز
        if completion_rate == 100:
            motivational_message = "عمل رائع جدًا! لقد أكملت العادة!"
        elif completion_rate >= 75:
            motivational_message = "ممتاز! استمر بنفس العزيمة."
        elif completion_rate >= 50:
            motivational_message = "أنت في منتصف الطريق، واصل التقدم!"
        else:
            motivational_message = "بداية جيدة! يمكنك تحقيق المزيد."

        # تسلسل البيانات
        serialized_habit = HabitSerializer(habit).data
        serialized_habit['completion_rate'] = f"{completion_rate:.2f}%"
        serialized_habit['completed_days'] = completed_days
        serialized_habit['total_days'] = total_days
        serialized_habit['motivational_message'] = motivational_message

=======
        serialized_habit = HabitSerializer(habit).data
>>>>>>> 769b9b4 (Add user features)
        return Response(serialized_habit, status=status.HTTP_200_OK)

    def put(self, request, habit_id):
        habit = self.get_object(habit_id)
        if not habit:
            return Response({"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = HabitSerializer(data=request.data)
        if serializer.is_valid():
            Habit.update_habit(ObjectId(habit_id), serializer.validated_data)
<<<<<<< HEAD
            return Response({"message": "Habit updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
=======
            return Response(serializer.data, status=status.HTTP_200_OK)
>>>>>>> 769b9b4 (Add user features)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, habit_id):
        habit = self.get_object(habit_id)
        if not habit:
            return Response({"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND)
        Habit.delete_habit(ObjectId(habit_id))
        return Response({"message": "Habit deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
<<<<<<< HEAD


class HabitInteractionView(APIView):
    permission_classes = [AllowAny]
    """
    واجهة تشجيع المستخدم على التفاعل مع العادة من خلال أسئلة يومية ومكافآت.
    """

    def get_object(self, habit_id):
        habit = Habit.collection.find_one({"_id": ObjectId(habit_id)})
        if not habit:
            return None
        return habit

    def post(self, request, habit_id):
        habit = self.get_object(habit_id)
        if not habit:
            return Response({"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND)

        # الأسئلة اليومية
        question = "هل مارست العادة اليوم؟"
        answer = request.data.get("answer")  # الإجابة (نعم/لا)

        # التحقق من الإجابة وتقديم رسالة تحفيزية
        if answer == "yes":
            motivational_message = "عمل رائع! استمر على هذا المنوال."
            # إضافة نقاط الإنجاز
            habit['points'] = habit.get('points', 0) + 10
        elif answer == "no":
            motivational_message = "لا بأس، غدًا فرصة جديدة!"
        else:
            return Response({"error": "Invalid answer. Please respond with 'yes' or 'no'."}, status=status.HTTP_400_BAD_REQUEST)

        # تحديث قاعدة البيانات
        Habit.collection.update_one({"_id": ObjectId(habit_id)}, {"$set": {"points": habit.get('points', 0)}})

        return Response({
            "question": question,
            "answer": answer,
            "motivational_message": motivational_message,
            "points": habit.get('points', 0)
        }, status=status.HTTP_200_OK)


class ChallengeView(APIView):
    permission_classes = [AllowAny]
    """
    واجهة عرض التحديات المرتبطة بالعادات مع وظائف إضافة، قبول، وإكمال التحديات.
    """

    def get(self, request):
        """
        عرض قائمة التحديات مع شريط التقدم لكل تحدٍ.
        """
        challenges = Habit.collection.find({"type": "challenge"})  # البحث عن التحديات
        serialized_challenges = []

        for challenge in challenges:
            # حساب شريط التقدم
            total_days = (challenge['end_date'] - challenge['start_date']).days + 1
            elapsed_days = (datetime.utcnow() - challenge['start_date']).days
            progress = min((elapsed_days / total_days) * 100, 100) if total_days > 0 else 0

            # تسلسل البيانات
            challenge_data = {
                "id": str(challenge['_id']),
                "name": challenge.get('name', 'تحدٍ بدون اسم'),
                "description": challenge.get('description', 'لا توجد تفاصيل'),
                "progress": f"{progress:.2f}%",
                "status": "مكتمل" if progress == 100 else "قيد التنفيذ",
            }
            serialized_challenges.append(challenge_data)

        return Response(serialized_challenges, status=status.HTTP_200_OK)

    def post(self, request):
        """
        إضافة تحدٍ جديد (إذا كانت الميزة مدعومة).
        """
        data = request.data
        required_fields = ['name', 'description', 'start_date', 'end_date']

        # التحقق من الحقول المطلوبة
        if not all(field in data for field in required_fields):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        # إنشاء التحدي
        challenge = {
            "type": "challenge",
            "name": data['name'],
            "description": data['description'],
            "start_date": datetime.strptime(data['start_date'], "%Y-%m-%d"),
            "end_date": datetime.strptime(data['end_date'], "%Y-%m-%d"),
            "status": False,  # التحدي قيد التنفيذ افتراضيًا
            "created_at": datetime.utcnow(),
        }

        # حفظ التحدي في قاعدة البيانات
        Habit.collection.insert_one(challenge)
        return Response({"message": "Challenge added successfully."}, status=status.HTTP_201_CREATED)

    def put(self, request, challenge_id):
        """
        قبول أو إكمال التحدي.
        """
        challenge = Habit.collection.find_one({"_id": ObjectId(challenge_id), "type": "challenge"})
        if not challenge:
            return Response({"error": "Challenge not found."}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get("action")
        if action == "accept":
            Habit.collection.update_one({"_id": ObjectId(challenge_id)}, {"$set": {"status": True}})
            return Response({"message": "Challenge accepted."}, status=status.HTTP_200_OK)
        elif action == "complete":
            Habit.collection.update_one({"_id": ObjectId(challenge_id)}, {"$set": {"status": "completed"}})
            return Response({"message": "Challenge marked as completed."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid action. Use 'accept' or 'complete'."}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, challenge_id):
        """
        حذف تحدٍ موجود.
        """
        challenge = Habit.collection.find_one({"_id": ObjectId(challenge_id), "type": "challenge"})
        if not challenge:
            return Response({"error": "Challenge not found."}, status=status.HTTP_404_NOT_FOUND)

        Habit.collection.delete_one({"_id": ObjectId(challenge_id)})
        return Response({"message": "Challenge deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



class PuzzleProgressView(APIView):
    permission_classes = [AllowAny]
    """
    عرض تقدم المستخدم في شكل لعبة لوحة بازل
    """

    def get(self, request, habit_id):
        habit = Habit.collection.find_one({"_id": ObjectId(habit_id)})
        if not habit:
            return Response({"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND)

        # حساب التقدم بناءً على الإنجاز
        total_days = (habit['end_date'] - habit['start_date']).days + 1
        elapsed_days = (datetime.utcnow() - habit['start_date']).days
        completion_rate = (elapsed_days / total_days) * 100 if total_days > 0 else 0

        # تحديد عدد الأجزاء التي سيتم إضاءتها في البازل بناءً على التقدم
        puzzle_parts = 10  # نفترض أن لدينا 10 أجزاء في البازل
        completed_parts = int((completion_rate / 100) * puzzle_parts)

        # إنشاء تمثيل لواجهة البازل (مربعات مضيئة أو غير مضيئة)
        puzzle = [{"part": i+1, "status": "completed" if i < completed_parts else "incomplete"} for i in range(puzzle_parts)]

        # رسالة تحفيزية بناءً على التقدم
        if completion_rate == 100:
            motivational_message = "لقد أكملت العادة! ممتاز!"
        elif completion_rate >= 75:
            motivational_message = "ممتاز! استمر بنفس الزخم!"
        elif completion_rate >= 50:
            motivational_message = "أنت في منتصف الطريق!"
        else:
            motivational_message = "استمر في التقدم!"

        return Response({
            "puzzle": puzzle,
            "completion_rate": f"{completion_rate:.2f}%",
            "motivational_message": motivational_message
        }, status=status.HTTP_200_OK)

    def post(self, request, habit_id):
        habit = Habit.collection.find_one({"_id": ObjectId(habit_id)})
        if not habit:
            return Response({"error": "Habit not found"}, status=status.HTTP_404_NOT_FOUND)

        # إعادة تعيين التقدم
        Habit.collection.update_one({"_id": ObjectId(habit_id)}, {"$set": {"progress": 0}})

        return Response({"message": "Progress reset successfully."}, status=status.HTTP_200_OK)




=======
>>>>>>> 769b9b4 (Add user features)
