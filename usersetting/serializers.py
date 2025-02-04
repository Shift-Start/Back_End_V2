from rest_framework import serializers

class SettingsSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    remember_key = serializers.CharField(allow_null=True, required=False)
    notification_value = serializers.BooleanField()
    default_settings = serializers.BooleanField()
    dark_mode = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
