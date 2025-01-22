import firebase_admin
from firebase_admin import credentials

def initialize_firebase():
    """تهيئة Firebase باستخدام google-services.json."""
    cred = credentials.Certificate('notifications/google-services.json')  # المسار إلى الملف
    firebase_admin.initialize_app(cred)
