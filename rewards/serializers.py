from rest_framework import serializers
from bson import ObjectId

class RewardSerializer(serializers.Serializer):
    reward_name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300, allow_blank=True, required=False)
    points_required = serializers.IntegerField()
    user_id = serializers.CharField(max_length=50)
    user_points = serializers.IntegerField(default=0, required=False)
    achieved = serializers.BooleanField(default=False, read_only=True)
    achievement_date = serializers.DateTimeField(read_only=True, required=False)
    tasks_completed = serializers.IntegerField(default=0, required=False)
    progress = serializers.FloatField(default=0.0, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_points_required(self, value):
        if value <= 0:
            raise serializers.ValidationError("Points required must be greater than zero.")
        return value

    def validate_reward_name(self, value):
        if value.isdigit():
            raise serializers.ValidationError("Reward name cannot contain only numbers.")
        return value
