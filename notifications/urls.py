from django.urls import path
from . import views

urlpatterns = [
    # استبدل هذا بخطوط مسارك الخاصة
    path('send-notification/', views.send_notification, name='send_notification'),
]


# http://127.0.0.1:8000/notifications/send-notification/ إضافة اشعار 
# {
#   "user_id": "676313e71c6fa6b40d339c6a",
#   "message": "Hello, this is a test notification!",
#   "note": "Testing phase"
# }

