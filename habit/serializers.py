from rest_framework import serializers

class HabitSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    repetition = serializers.IntegerField()
    start_date = serializers.DateTimeField()  # تعديل الحقل ليكون DateTimeField
    end_date = serializers.DateTimeField()    # تعديل الحقل ليكون DateTimeField
    status = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
