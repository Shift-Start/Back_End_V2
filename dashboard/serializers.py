from rest_framework import serializers

class TeamSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    admin_id = serializers.CharField(max_length=50)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    goal = serializers.CharField(max_length=200, allow_blank=True, required=False)
    setting_team = serializers.JSONField(required=False)

class TeamMemberSerializer(serializers.Serializer):
    team_id = serializers.CharField()
    user_id = serializers.CharField()
    role = serializers.CharField(max_length=50)
    joined_at = serializers.DateTimeField(read_only=True)

# serializers.py

from rest_framework import serializers

class TaskSerializer(serializers.Serializer):
    status = serializers.CharField()  # عرض الحالة فقط
    created_at = serializers.DateTimeField()  # عرض تاريخ الإنشاء فقط



class TemplateSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=1024)
    CreatedAt = serializers.DateTimeField(read_only=True)




class RecommendationSerializer(serializers.Serializer):
    _id = serializers.CharField(read_only=True)
    UserID = serializers.CharField(max_length=24, required=True)
    UserName = serializers.CharField(read_only=True)
    Content = serializers.CharField(max_length=500, required=True)
    CreatedAt = serializers.DateTimeField(read_only=True)
    archived = serializers.BooleanField(default=False)