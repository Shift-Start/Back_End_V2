from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from datetime import datetime
from team.models import Team, TeamMember
from .models import TeamMember, TeamTask
from team.serializers import TeamSerializer, TeamMemberSerializer, TeamTaskSerializer

# دالة مساعدة لتحويل ObjectId إلى نصوص
def convert_object_id_to_string(data):
    # تحويل جميع الحقول التي تحتوي على ObjectId إلى نصوص.
    if isinstance(data, list):
        for item in data:
            convert_object_id_to_string(item)
    elif isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            elif isinstance(value, (dict, list)):
                convert_object_id_to_string(value)
    return data

# عرض وإنشاء الفرق
class TeamListCreateView(APIView):
    permission_classes = [AllowAny]  # إضافة هنا للسماح للجميع بالوصول
    def post(self, request):
        data = request.data
        serializer = TeamSerializer(data=data)
        if serializer.is_valid():
            team_data = serializer.validated_data
            team_data['created_at'] = datetime.utcnow()
            team_data['updated_at'] = datetime.utcnow()
            created_team = Team.create_team(team_data)
            created_team = convert_object_id_to_string(created_team)  # تحويل ObjectId إلى نصوص
            return Response(created_team, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        teams = Team.collection.find()
        team_list = [convert_object_id_to_string(team) for team in teams]  # تحويل ObjectId إلى نصوص
        return Response(team_list, status=status.HTTP_200_OK)

# عرض وإنشاء أعضاء الفريق
class TeamMemberListCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        serializer = TeamMemberSerializer(data=data)
        if serializer.is_valid():
            member_data = serializer.validated_data
            member_data['created_at'] = datetime.utcnow()
            member_data['updated_at'] = datetime.utcnow()
            created_member = TeamMember.add_team_member(member_data)

            created_member = convert_object_id_to_string(created_member)
            return Response(created_member, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        members = TeamMember.collection.find()
        member_list = [convert_object_id_to_string(member) for member in members]  # تحويل ObjectId إلى نصوص
        return Response(member_list, status=status.HTTP_200_OK)

# تحديث فريق
class TeamUpdateView(APIView):
    def put(self, request, team_id):
        data = request.data
        serializer = TeamSerializer(data=data)
        if serializer.is_valid():
            updated_data = serializer.validated_data
            updated_data['updated_at'] = datetime.utcnow()
            Team.update_team(ObjectId(team_id), updated_data)  # تحديث الفريق باستخدام ObjectId
            updated_team = Team.get_team(ObjectId(team_id))
            updated_team = convert_object_id_to_string(updated_team)
            return Response(updated_team, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# حذف فريق
class TeamDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, team_id):
        print(f"Received request to delete team with ID: {team_id}")  # طباعة الطلب الوارد
        try:
            team_id = ObjectId(team_id)  # تحويل team_id إلى ObjectId إذا كان يستخدم في قاعدة البيانات
        except Exception as e:
            return Response({"error": "Invalid team_id format."}, status=status.HTTP_400_BAD_REQUEST)

        team = Team.get_team(team_id)
        if team:
            Team.delete_team(team_id)
            return Response({"message": "Team and members deleted successfully."}, status=status.HTTP_200_OK)
        return Response({"error": "Team not found."}, status=status.HTTP_404_NOT_FOUND)

# تحديث عضو فريق
class TeamMemberUpdateView(APIView):
    permission_classes = [AllowAny]  # إضافة هنا للسماح للجميع بالوصول
    def put(self, request, member_id):
        data = request.data
        serializer = TeamMemberSerializer(data=data)
        if serializer.is_valid():
            updated_data = serializer.validated_data
            updated_data['updated_at'] = datetime.utcnow()
            TeamMember.update_team_member(ObjectId(member_id), updated_data)  # تحديث عضو الفريق باستخدام ObjectId
            updated_member = TeamMember.get_team_member(ObjectId(member_id))
            updated_member = convert_object_id_to_string(updated_member)
            return Response(updated_member, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# حذف عضو فريق
class TeamMemberDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, user_id, team_id):
        # التحقق من وجود العضو في الفريق
        member = TeamMember.collection.find_one({"user_id": user_id, "team_id": team_id})
        if not member:
            return Response({"error": "Member not found in the specified team."}, status=status.HTTP_404_NOT_FOUND)
        # إزالة العضو من الفريق
        result = TeamMember.collection.delete_one({"user_id": user_id, "team_id": team_id})
        if result.deleted_count == 1:
            return Response({"message": "Member removed from the team."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to remove member."}, status=status.HTTP_400_BAD_REQUEST)
# حذف مهمة لفريق
class TeamTaskDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, team_id, task_id):
        # تأكد من أنك تحصل على المعرفات بشكل صحيح
        task = TeamTask.collection.find_one({"_id": ObjectId(task_id), "team_id": team_id})

        if task:
            # إذا كانت المهمة موجودة، قم بحذفها
            TeamTask.collection.delete_one({"_id": ObjectId(task_id)})
            return Response({"message": "Task deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

class TeamTaskListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, team_id):
        try:
            # عرض المهام
            query = {"team_id": team_id}
            tasks = TeamTask.collection.find(query)
            task_list = [convert_object_id_to_string(task) for task in tasks]
            return Response(task_list, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Failed to fetch tasks: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, team_id):
        data = request.data
        serializer = TeamTaskSerializer(data=data)
        
        if serializer.is_valid():
            task_data = serializer.validated_data
            task_data['team_id'] = team_id
            task_data['created_at'] = datetime.utcnow()
            task_data['updated_at'] = datetime.utcnow()

            assigned_member_id = task_data.get("assigned_member_id", None)
            if assigned_member_id:
                try:
                    member = TeamMember.collection.find_one(
                        {"_id": ObjectId(assigned_member_id), "team_id": team_id}
                    )
                    if not member:
                        return Response(
                            {"error": "Assigned member does not exist in the team."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                except Exception as e:
                    return Response(
                        {"error": "Invalid assigned_member_id.", "details": str(e)},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            task_data["assigned_member_id"] = assigned_member_id or None

            try:
                created_task = TeamTask.create_task(task_data)
                created_task = convert_object_id_to_string(created_task)
                return Response(created_task, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response(
                    {"error": "Failed to create task.", "details": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# تحديث مهمة (إمكانية تعديل إسنادها لعضو أو تركها بدون عضو)
class TeamTaskUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, team_id, task_id):
        # استبدال البيانات بالكامل
        task_data = request.data
        serializer = TeamTaskSerializer(data=task_data)
        if serializer.is_valid():
            # التحقق إذا كانت المهمة موجودة
            task = TeamTask.collection.find_one({"_id": ObjectId(task_id), "team_id": team_id})
            if not task:
                return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)
            # تحديث المهمة
            updated_data = serializer.validated_data
            updated_data["updated_at"] = datetime.utcnow()
            TeamTask.collection.update_one(
                {"_id": ObjectId(task_id), "team_id": team_id},
                {"$set": updated_data}
            )
            return Response({"message": "Task updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, team_id, task_id):
        # تحديث جزئي للبيانات
        task_data = request.data

        # التحقق إذا كانت المهمة موجودة
        task = TeamTask.collection.find_one({"_id": ObjectId(task_id), "team_id": team_id})
        if not task:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        # تحديث البيانات المحددة
        TeamTask.collection.update_one(
            {"_id": ObjectId(task_id), "team_id": team_id},
            {"$set": task_data}
        )
        return Response({"message": "Task updated successfully."}, status=status.HTTP_200_OK)

class MemberTaskListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, member_id):
        # جلب المهام بناءً على `assigned_member_id`
        tasks = TeamTask.collection.find({"assigned_member_id": member_id})
        task_list = [convert_object_id_to_string(task) for task in tasks]

        if not task_list:
            return Response({"message": "No tasks found for the given member ID."}, status=status.HTTP_404_NOT_FOUND)

        return Response(task_list, status=status.HTTP_200_OK)


class TeamTasksByTeamView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, team_id):
        try:
            # إنشاء الاستعلام للحصول على المهام الخاصة بالفريق
            query = {"team_id": team_id}
            tasks = TeamTask.collection.find(query)
            # تحويل البيانات إلى صيغة JSON-friendly
            task_list = [convert_object_id_to_string(task) for task in tasks]
            # إرجاع قائمة المهام
            return Response(task_list, status=status.HTTP_200_OK)
        except Exception as e:
            # معالجة الأخطاء
            return Response(
                {"error": f"Failed to fetch tasks: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserAssignedTasksView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        # البحث عن المهام التي تحتوي على assigned_member_id بدلاً من user_id
        tasks = TeamTask.get_tasks_by_assigned_member(user_id)

        # تحديث المهام بحيث يصبح user_id = assigned_member_id
        updated_tasks = []
        for task in tasks:
            task["user_id"] = task["assigned_member_id"]  # تخزين assigned_member_id في user_id
            TeamTask.update_task_user_id(task["_id"], task["user_id"])  # تحديث في قاعدة البيانات
            updated_tasks.append(convert_object_id_to_string(task))

        return Response(updated_tasks, status=status.HTTP_200_OK)

