from rest_framework import serializers

class HabitSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
<<<<<<< HEAD
    repetition = serializers.ChoiceField(choices=[('daily', 'Daily'), ('weekly', 'Weekly')])
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    status = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
    completion_rate = serializers.FloatField(read_only=True)  # نسبة الإنجاز
    status_color = serializers.CharField(read_only=True)      # لون الحالة
    updated_at = serializers.DateTimeField() 
=======
    repetition = serializers.IntegerField()
    start_date = serializers.DateTimeField()  # تعديل الحقل ليكون DateTimeField
    end_date = serializers.DateTimeField()    # تعديل الحقل ليكون DateTimeField
    status = serializers.BooleanField()
    created_at = serializers.DateTimeField(read_only=True)
>>>>>>> 769b9b4 (Add user features)
