from datetime import datetime
from rest_framework import serializers
from bson import ObjectId

class TaskSerializer(serializers.Serializer):
    TaskID = serializers.CharField(max_length=50, required=False)
    UserID = serializers.CharField(max_length=24,required=True)
    Title = serializers.CharField(max_length=200, required=True)
    Description = serializers.CharField(max_length=500, allow_blank=True, required=False)
    Date = serializers.DateTimeField(required=True)  # تاريخ المهمة
    StartDate = serializers.DateTimeField(required=True)  # تاريخ البدء
    EndDate = serializers.DateTimeField(required=True)  # تاريخ الانتهاء
    repetition = serializers.CharField(max_length=50, required=False, allow_blank=True)
    Status = serializers.CharField(max_length=50, required=True)  # حالة المهمة

class TemplateSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1024)
    CreatedAt = serializers.DateTimeField(read_only=True)

class TemplateTaskSerializer(serializers.Serializer):
    Templates = serializers.CharField(max_length=255)
    TaskID = serializers.CharField(max_length=255, required=True)
    Description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    TemplateID = serializers.CharField(max_length=255)
    StartDate = serializers.DateTimeField()
    EndDate = serializers.DateTimeField()
    Date = serializers.DateField()
    Point = serializers.FloatField()
    Status = serializers.CharField(max_length=50)
    Repetition = serializers.CharField(max_length=50)

class AddTemplateTaskSerializer(serializers.Serializer):
    TemplateID = serializers.CharField(max_length=24, required=True)  # ObjectId بطول 24 حرفًا
    # TaskID = serializers.CharField(max_length=255, required=True)
    TaskName=serializers.CharField(max_length=1000, required=False)
    Description = serializers.CharField(max_length=1000, required=False, allow_blank=True)
    StartDate = serializers.DateTimeField(required=True)
    EndDate = serializers.DateTimeField(required=True)
    Date = serializers.DateField(required=True, input_formats=['%Y-%m-%d', '%d/%m/%Y', '%Y/%m/%d'])
    Point = serializers.FloatField(required=True)
    Status = serializers.CharField(max_length=50, required=True)
    Repetition = serializers.CharField(max_length=50, required=True)

    def validate_TemplateID(self, value):
        # التحقق من أن TemplateID صالح
        try:
            ObjectId(value)  # محاولة تحويل النص إلى ObjectId
        except Exception:
            raise serializers.ValidationError("Invalid TemplateID format.")
        return value
