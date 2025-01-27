from rest_framework import serializers

class RewardSerializer(serializers.Serializer):
    reward_name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=300, allow_blank=True, required=False)
    points_required = serializers.IntegerField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def validate_points_required(self, value):
        # التحقق من أن النقاط المطلوبة أكبر من صفر.
        if value <= 0:
            raise serializers.ValidationError("Points required must be greater than zero.")
        return value

    def validate_reward_name(self, value):
        # التحقق من أن اسم المكافأة ليس رقمًا فقط.
        if value.isdigit():
            raise serializers.ValidationError("Reward name cannot contain only numbers.")
        return value
