from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    id = models.AutoField(primary_key=True)  # تحديد الحقل كـ primary key
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ربط المستخدم بالإشعار
    message = models.TextField()  # نص الرسالة
    note = models.TextField()  # ملاحظة إضافية
    is_read = models.BooleanField(default=False)  # حالة القراءة
    created_at = models.DateTimeField(auto_now_add=True)  # تاريخ الإنشاء

    def __str__(self):
        return f"Notification for {self.user.username} - {self.created_at}"
