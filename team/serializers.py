from rest_framework import serializers
from bson import ObjectId
from rest_framework import serializers
from team.models import TeamMember

class TeamSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    admin_id = serializers.CharField(max_length=50)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    goal = serializers.CharField(max_length=200, allow_blank=True, required=False)
    setting_team = serializers.JSONField(required=False)

class TeamMemberSerializer(serializers.Serializer):
    team_id = serializers.CharField(max_length=50)
    user_id = serializers.CharField(max_length=50)
    permissions = serializers.JSONField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class TeamTaskSerializer(serializers.Serializer):
    team_task_id = serializers.CharField(read_only=True)  # يتم إنشاؤه تلقائيًا
    team_id = serializers.CharField(required=True)  # ID الفريق الذي تنتمي إليه المهمة
    description = serializers.CharField(required=True, max_length=500)  # وصف المهمة
    start_date = serializers.DateTimeField(required=True)  # تاريخ البدء
    end_date = serializers.DateTimeField(required=True)  # تاريخ الانتهاء
    status = serializers.ChoiceField(choices=["Pending", "In Progress", "Completed"], default="Pending")  # حالة المهمة
    created_by = serializers.CharField(read_only=True)  # يتم تعبئتها تلقائيًا من المستخدم الحالي
    assigned_member_id = serializers.CharField(required=False, allow_null=True)

    def validate(self, data):        # التحقق من صحة البيانات بما في ذلك التواريخ والعلاقة بين الحقول
        if data["start_date"] >= data["end_date"]:        # التحقق من أن تاريخ البدء أقل من تاريخ الانتهاء
            raise serializers.ValidationError("Start date must be earlier than end date.")

        if "assigned_member_id" in data and data["assigned_member_id"]:        # التحقق من صحة حقل assigned_to (يمكن أن يكون غير موجود أو فارغ)
            assigned_member_id = data["assigned_member_id"]
            team_id = data["team_id"]
            member = TeamMember.collection.find_one({"_id": ObjectId(assigned_member_id), "team_id": team_id})
            if not member:
                raise serializers.ValidationError("The assigned member does not exist in the team.")
        return data
