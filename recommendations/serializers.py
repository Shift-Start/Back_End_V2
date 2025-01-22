from rest_framework import serializers

class RecommendationSerializer(serializers.Serializer):
    RecommendationID = serializers.CharField(max_length=24, required=False)  # معرف التوصية
    UserID = serializers.CharField(max_length=24, required=True)  # معرف المستخدم
    Content = serializers.CharField(max_length=500, required=True)  # محتوى التوصية
    CreatedAt = serializers.DateTimeField(read_only=True)  # تاريخ الإنشاء
