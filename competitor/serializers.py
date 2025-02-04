# from rest_framework import serializers
# from account.models import User

# class CompetitorSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=50)
#     points = serializers.IntegerField()
#     profile_image = serializers.CharField(required=False)  # حقل الصورة (يمكن أن يكون URL)
from rest_framework import serializers

class CompetitorSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    points = serializers.IntegerField()
    profile_image = serializers.CharField(required=False)  # صورة المستخدم (يمكن أن تكون URL)
