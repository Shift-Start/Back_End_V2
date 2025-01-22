from datetime import datetime
import pytz
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from account.models import (
    User,
    ActivityLog,
    Leaderboard,
    Recommendations,
    Notifications,
    Reward,
    Reports,
)
from account.serializers import (
    UserSerializer,
    ActivityLogSerializer,
    LeaderboardSerializer,
    RecommendationsSerializer,
    NotificationsSerializer,
    RewardSerializer,
    ReportSerializer,
)

from rest_framework.permissions import AllowAny



# دالة لتحويل الوقت المحلي المرسل من الجهاز إلى UTC
def convert_to_utc(local_time_str):
    """
    تحويل الوقت المحلي المرسل من الجهاز إلى UTC.
    """
    local_time = datetime.fromisoformat(local_time_str)  # تحويل النص إلى كائن datetime
    local_time = local_time.replace(tzinfo=pytz.UTC)  # ضبط المنطقة الزمنية
    return local_time

# دالة مساعدة لتحويل ObjectId إلى نصوص
def convert_object_ids(data):
    """
    تحويل جميع الحقول التي تحتوي على ObjectId إلى نصوص.
    """
    if isinstance(data, list):
        return [convert_object_ids(item) for item in data]
    elif isinstance(data, dict):
        return {
            key: str(value) if isinstance(value, ObjectId) else convert_object_ids(value)
            for key, value in data.items()
        }
    else:
        return data

### عرض تفاصيل المستخدم ###
class UserDetailView(APIView):
    
    def get(self, request, user_id):
        """عرض تفاصيل المستخدم حسب user_id"""
        user = User.get_user_by_id(ObjectId(user_id))
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(convert_object_ids(user), status=status.HTTP_200_OK)

    def patch(self, request, user_id):
        """تحديث تفاصيل المستخدم"""
        user = User.get_user_by_id(ObjectId(user_id))
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        #خاص بالاشعارات
        if 'device_token' in request.data:
            updated_data['device_token'] = request.data['device_token']

        serializer = UserSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            updated_data = serializer.validated_data

            # تحويل الوقت المحلي إلى UTC إذا تم إرساله
            if 'updated_at' in request.data:
                local_time_str = request.data['updated_at']
                updated_data['updated_at'] = convert_to_utc(local_time_str)

            User.update_user(ObjectId(user_id), updated_data)
            updated_user = User.get_user_by_id(ObjectId(user_id))
            return Response(convert_object_ids(updated_user), status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileView(APIView):
    permission_classes = [AllowAny]  # استخدام AllowAny إذا كانت لا توجد حاجة للتحقق من الهوية

    def get(self, request):
        user_id = request.user.id  # أو من الممكن أن تستخدم طريقة للحصول على مستخدم من MongoDB مباشرة
        user = User.get_user_by_id(user_id)  # الحصول على المستخدم من MongoDB باستخدام دالة موجودة في الكلاس User
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)




### عرض وتسجيل النشاطات ###
class ActivityLogView(APIView):
    def get(self, request, user_id):
        """عرض جميع النشاطات الخاصة بالمستخدم"""
        logs = ActivityLog.get_logs_by_user(ObjectId(user_id))
        return Response(convert_object_ids(logs), status=status.HTTP_200_OK)

    def post(self, request):
        """تسجيل نشاط جديد"""
        serializer = ActivityLogSerializer(data=request.data)
        if serializer.is_valid():
            log_data = serializer.validated_data

            # تحويل الوقت المحلي إلى UTC
            if 'timestamp' in request.data:
                local_time_str = request.data['timestamp']
                log_data['timestamp'] = convert_to_utc(local_time_str)

            log = ActivityLog.log_action(**log_data)
            return Response(convert_object_ids(log), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### لوحة النقاط ###
class LeaderboardView(APIView):
    def get(self, request):
        """عرض لوحة النقاط"""
        leaderboard = Leaderboard.get_leaderboard()
        return Response(convert_object_ids(leaderboard), status=status.HTTP_200_OK)

### توصيات التطبيق ###
class RecommendationsView(APIView):
    def get(self, request):
        """عرض جميع التوصيات"""
        recommendations = Recommendations.get_all_recommendations()
        return Response(convert_object_ids(recommendations), status=status.HTTP_200_OK)

    def post(self, request):
        """إضافة توصية جديدة"""
        # استخدام الـ serializer للتحقق من صحة البيانات
        serializer = RecommendationsSerializer(data=request.data)
        if serializer.is_valid():
            # استخراج البيانات الصالحة من الـ serializer
            user_id = serializer.validated_data['user_id']
            content = serializer.validated_data['content']

            # استدعاء دالة إنشاء التوصية من الـ model
            recommendation = Recommendations.create_recommendation(user_id, content)

            # إرجاع التوصية الجديدة مع تحويل ObjectId إلى نص
            return Response(convert_object_ids(recommendation), status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### الإشعارات ###
class NotificationsView(APIView):
    def get(self, request, user_id):
        """عرض جميع الإشعارات الخاصة بالمستخدم"""
        notifications = Notifications.collection.find({"user_id": ObjectId(user_id)})
        return Response(convert_object_ids(notifications), status=status.HTTP_200_OK)

    def patch(self, request, notification_id):
        """تحديث حالة الإشعار كـ مقروء"""
        Notifications.mark_as_read(ObjectId(notification_id))
        return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)

### المكافآت ###
class RewardView(APIView):
    def get(self, request, user_id):
        """عرض المكافآت الخاصة بالمستخدم"""
        rewards = Reward.get_rewards_by_user(ObjectId(user_id))
        return Response(convert_object_ids(rewards), status=status.HTTP_200_OK)

    def post(self, request):
        """إضافة مكافأة جديدة"""
        serializer = RewardSerializer(data=request.data)
        if serializer.is_valid():
            reward = Reward.create_reward(**serializer.validated_data)
            return Response(convert_object_ids(reward), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportView(APIView):
    def get(self, request, user_id):
        """عرض جميع التقارير الخاصة بالمستخدم"""
        reports = Reports.get_reports_by_user(ObjectId(user_id))  # جلب التقارير من قاعدة البيانات
        if not reports:
            return Response({"message": "No reports found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(convert_object_ids(reports), status=status.HTTP_200_OK)

    def post(self, request, user_id):
        """إضافة تقرير جديد"""
        data = request.data
        data['user_id'] = user_id  # إضافة user_id من المسار (URL)
        
        serializer = ReportSerializer(data=data)
        if serializer.is_valid():
            report_data = serializer.validated_data
            report = Reports.create_report(user_id=user_id, **report_data)
            return Response(convert_object_ids(report), status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ReportView(APIView):
#     def get(self, request, user_id):
#         """عرض التقارير الخاصة بالمستخدم"""
#         reports = Reports.get_reports_by_user(ObjectId(user_id))
#         return Response(convert_object_ids(reports), status=status.HTTP_200_OK)

#     def post(self, request, user_id):
#         """إضافة تقرير جديد"""
#         # استخراج البيانات من الجسم
#         data = request.data
#         data['user_id'] = user_id  # إضافة user_id من المسار (URL)
        
#         serializer = ReportSerializer(data=data)
#         if serializer.is_valid():
#             # إرسال البيانات إلى `Reports.create_report`
#             report_data = serializer.validated_data
#             report = Reports.create_report(user_id=user_id, **report_data)
#             return Response(convert_object_ids(report), status=status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
