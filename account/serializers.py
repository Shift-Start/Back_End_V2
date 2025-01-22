from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    username = serializers.CharField()
    email = serializers.EmailField()
    profile_picture = serializers.URLField(required=False, allow_null=True)
    points = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    birth_date = serializers.DateTimeField(required=False, allow_null=True)
    account_creation_date = serializers.DateTimeField(required=False, allow_null=True)
    gender = serializers.CharField(required=False, allow_null=True)
    device_token = serializers.CharField(required=False, allow_null=True)





# class UserSerializer(serializers.Serializer):
#     id = serializers.CharField(source='_id', read_only=True)
#     username = serializers.CharField()
#     email = serializers.EmailField()
#     profile_picture = serializers.URLField(required=False, allow_null=True)
#     points = serializers.IntegerField(read_only=True)
#     created_at = serializers.DateTimeField(read_only=True)
#     updated_at = serializers.DateTimeField(read_only=True)


class ActivityLogSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.CharField()
    action = serializers.CharField()
    timestamp = serializers.DateTimeField()


class LeaderboardSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.CharField()
    points = serializers.IntegerField()
    reason = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField()


class RecommendationsSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.CharField()
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)


class NotificationsSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.CharField()
    message = serializers.CharField()
    note = serializers.CharField()
    is_read = serializers.BooleanField()
    created_at = serializers.DateTimeField()


class RewardSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.CharField()
    reward_name = serializers.CharField()
    description = serializers.CharField()
    points_required = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)


class ReportSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    report_content = serializers.ListField(
        child=serializers.CharField()  # المصفوفة تحتوي على اسم التقرير ووصفه
    )
    created_at = serializers.DateTimeField(read_only=True)


