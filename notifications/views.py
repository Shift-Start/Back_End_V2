# import firebase_admin
# from rest_framework.permissions import AllowAny
# from firebase_admin import messaging
# from firebase_admin import credentials
# from django.conf import settings
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .models import Notification
# from .serializers import NotificationSerializer
# from pymongo import MongoClient
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import AllowAny

# # تهيئة Firebase
# cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
# firebase_admin.initialize_app(cred)

# client = MongoClient("mongodb://127.0.0.1:27017/")
# db = client["Shift-Start-db"]
# notifications_collection = db["notifications"]


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def send_notification(request):

#     # بيانات الإشعار القادمة من الطلب
#     user_id = request.data.get('user_id')
#     message = request.data.get('message')
#     note = request.data.get('note')

#     # إنشاء إشعار جديد في قاعدة البيانات
#     notification = Notification.objects.create(
#         user_id=user_id,
#         message=message,
#         note=note,
#         is_read=False
#     )

#     # إرسال الإشعار إلى Firebase
#     try:
#         user_device_token = get_user_device_token(user_id)  # الحصول على رمز جهاز المستخدم

#         if not user_device_token:
#             return Response({'status': 'failure', 'error': 'Device token not found for user.'})

#         # بناء رسالة Firebase
#         firebase_message = messaging.Message(
#             notification=messaging.Notification(
#                 title="New Notification",
#                 body=message
#             ),
#             token=user_device_token
#         )

#         # إرسال الإشعار عبر Firebase
#         response = messaging.send(firebase_message)

#         # العودة برد
#         return Response({'status': 'success', 'firebase_response': response})
#     except Exception as e:
#         return Response({'status': 'failure', 'error': str(e)})

# def get_user_device_token(user_id):
# #     دالة للحصول على رمز جهاز Firebase الخاص بالمستخدم من قاعدة البيانات
#     user = db.users.find_one({"user_id": user_id})
#     return user.get("device_token") if user else None


import firebase_admin
from rest_framework.permissions import AllowAny
from firebase_admin import messaging
from firebase_admin import credentials
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Notification
from .serializers import NotificationSerializer
from pymongo import MongoClient
from rest_framework.decorators import permission_classes

# تهيئة Firebase
cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["Shift-Start-db"]
notifications_collection = db["notifications"]

@api_view(['POST'])
@permission_classes([AllowAny])
def send_notification(request):
    # بيانات الإشعار القادمة من الطلب
    user_id = request.data.get('user_id')
    message = request.data.get('message')
    note = request.data.get('note')

    # إنشاء إشعار جديد في قاعدة البيانات
    notification = Notification.objects.create(
        user_id=user_id,
        message=message,
        note=note,
        is_read=False
    )

    # إرسال الإشعار إلى Firebase
    try:
        user_device_token = get_user_device_token(user_id)

        # **إضافة قيمة افتراضية أثناء التجريب**
        if not user_device_token:
            user_device_token = "default-device-token-for-testing"  # قيمة افتراضية لتجاوز الخطأ أثناء التجريب

        # بناء رسالة Firebase
        firebase_message = messaging.Message(
            notification=messaging.Notification(
                title="New Notification",
                body=message
            ),
            token=user_device_token
        )

        # إرسال الإشعار عبر Firebase
        response = messaging.send(firebase_message)

        # العودة برد
        return Response({'status': 'success', 'firebase_response': response})
    except Exception as e:
        return Response({'status': 'failure', 'error': str(e)})

def get_user_device_token(user_id):
    # دالة للحصول على رمز جهاز Firebase الخاص بالمستخدم من قاعدة البيانات
    user = db.users.find_one({"user_id": user_id})
    return user.get("device_token") if user else None
