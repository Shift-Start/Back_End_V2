import firebase_admin
from firebase_admin import messaging
from firebase_admin import credentials
import os
from dotenv import load_dotenv

# تحميل إعدادات البيئة من ملف .env
load_dotenv()

# تحميل ملف google-services.json
cred = credentials.Certificate(os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY"))
firebase_admin.initialize_app(cred)

def send_notification(token, title, body):
    """إرسال إشعار إلى جهاز معين باستخدام FCM token."""
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,
    )
    
    # إرسال الإشعار
    try:
        response = messaging.send(message)
        print("Successfully sent message:", response)
    except Exception as e:
        print(f"Error sending message: {e}")

# مثال على كيفية استخدام الدالة
# send_notification("<device_token>", "Task Reminder", "Your task is about to start!")
