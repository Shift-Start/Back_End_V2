



















from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Team, TeamMember
from .serializers import TeamSerializer, TeamMemberSerializer
from rest_framework.permissions import AllowAny
from datetime import datetime

from bson import ObjectId
from .serializers import TaskSerializer
from .models import Task
from pymongo import MongoClient
from .models import ActivityLog
from .models import TemplateModel
from .serializers import TemplateSerializer
from .models import Recommendation
from .serializers import RecommendationSerializer
from pymongo import MongoClient
from .models import ActivityLog
from pymongo import MongoClient
import pandas as pd
from django.http import HttpResponse



class TeamView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            team = Team.create_team(serializer.validated_data)
            return Response(team, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, team_id=None):
        if team_id:
            team = Team.get_team(team_id)
            if team:
                return Response(team, status=status.HTTP_200_OK)
            return Response({"error": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
        teams = Team.get_all_teams()
        return Response(teams, status=status.HTTP_200_OK)

    def put(self, request, team_id):
        serializer = TeamSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            updated = Team.update_team(team_id, serializer.validated_data)
            if updated:
                return Response({"message": "Team updated successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Update failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, team_id):
        deleted = Team.delete_team(team_id)
        if deleted:
            return Response({"message": "Team deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Delete failed"}, status=status.HTTP_400_BAD_REQUEST)

class TeamMemberView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TeamMemberSerializer(data=request.data)
        if serializer.is_valid():
            member = TeamMember.add_team_member(serializer.validated_data)
            return Response(member, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, member_id=None):
        if member_id:
            member = TeamMember.get_team_member(member_id)
            if member:
                return Response(member, status=status.HTTP_200_OK)
            return Response({"error": "Team member not found"}, status=status.HTTP_404_NOT_FOUND)
        members = TeamMember.get_all_team_members()
        return Response(members, status=status.HTTP_200_OK)

    def put(self, request, member_id):
        serializer = TeamMemberSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            updated = TeamMember.update_team_member(member_id, serializer.validated_data)
            if updated:
                return Response({"message": "Team member updated successfully"}, status=status.HTTP_200_OK)
            return Response({"error": "Update failed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, member_id):
        deleted = TeamMember.delete_team_member(member_id)
        if deleted:
            return Response({"message": "Team member deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Delete failed"}, status=status.HTTP_400_BAD_REQUEST)


# views.py



class DashboardTaskListView(APIView):
    permission_classes = [AllowAny]
    """
    عرض قائمة المهام مع الحالة وتاريخ الإنشاء فقط
    """
    def get(self, request):
        tasks = Task.get_all_tasks()  # استدعاء المهام من MongoDB
        serializer = TaskSerializer(tasks, many=True)  # تحويل البيانات
        return Response(serializer.data, status=status.HTTP_200_OK)

class DashboardTaskDetailView(APIView):
    permission_classes = [AllowAny]
    """
    عرض تفاصيل مهمة واحدة مع الحالة وتاريخ الإنشاء فقط
    """
    def get(self, request, task_id):
        task = Task.get_task_by_id(task_id)  # استدعاء مهمة واحدة
        if task:
            serializer = TaskSerializer(task)  # تحويل البيانات
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)




###


class DashboardTemplateView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        templates = TemplateModel.get_all_templates()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = TemplateSerializer(data=request.data)
        if serializer.is_valid():
            template = TemplateModel.insert_template(
                name=serializer.validated_data['name'],
                description=serializer.validated_data['description']
            )
            return Response(template, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DashboardTemplateDetailView(APIView):
    def put(self, request, template_id):
        updated_data = request.data
        result, code = TemplateModel.update_template(template_id, updated_data)
        return Response(result, status=code)
    
    def delete(self, request, template_id):
        result, code = TemplateModel.delete_template_by_id(template_id)
        return Response(result, status=code)


###########3


class RecommendationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        recommendations = Recommendation.get_all_recommendations()
        return Response(recommendations, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RecommendationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            recommendation = Recommendation.add_recommendation({
                "UserID": validated_data['UserID'],
                "Content": validated_data['Content'],
                "CreatedAt": datetime.utcnow()
            })
            return Response(recommendation, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RecommendationDetailView(APIView):
    def get(self, request, rec_id):
        result, code = Recommendation.get_recommendation_by_id(rec_id)
        return Response(result, status=code)

    def delete(self, request, rec_id):
        result, code = Recommendation.delete_recommendation(rec_id)
        return Response(result, status=code)

    def put(self, request, rec_id):
        result, code = Recommendation.archive_recommendation(rec_id)
        return Response(result, status=code)


#############


client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["Shift-Start-db"]

class ReportView(APIView):
    def get(self, request, report_type):
        if report_type == "user_performance":
            data = list(db['users'].find({}, {"_id": 0, "name": 1, "performance_score": 1}))
        elif report_type == "active_teams":
            data = list(db['teams'].find({"active": True}, {"_id": 0, "name": 1, "members_count": 1}))
        elif report_type == "popular_templates":
            data = list(db['templates'].find({}, {"_id": 0, "name": 1, "usage_count": 1}))
        else:
            return Response({"error": "Invalid report type"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(data, status=status.HTTP_200_OK)

class DownloadReportView(APIView):
    def get(self, request, report_type, format):
        if report_type == "user_performance":
            data = list(db['users'].find({}, {"_id": 0, "name": 1, "performance_score": 1}))
        elif report_type == "active_teams":
            data = list(db['teams'].find({"active": True}, {"_id": 0, "name": 1, "members_count": 1}))
        elif report_type == "popular_templates":
            data = list(db['templates'].find({}, {"_id": 0, "name": 1, "usage_count": 1}))
        else:
            return Response({"error": "Invalid report type"}, status=status.HTTP_400_BAD_REQUEST)
        
        df = pd.DataFrame(data)
        
        if format == "pdf":
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{report_type}.pdf"'
            df.to_string(buf=response, index=False)
        elif format == "excel":
            response = HttpResponse(content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = f'attachment; filename="{report_type}.xlsx"'
            df.to_excel(response, index=False)
        else:
            return Response({"error": "Invalid format"}, status=status.HTTP_400_BAD_REQUEST)
        
        return response









#####



client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["Shift-Start-db"]

class ActivityLogView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user_id = request.query_params.get('user_id', None)
        action_type = request.query_params.get('action_type', None)
        date_from = request.query_params.get('date_from', None)
        date_to = request.query_params.get('date_to', None)

        filter_conditions = {}

        if user_id:
            filter_conditions['UserID'] = user_id
        if action_type:
            filter_conditions['ActionType'] = action_type
        if date_from and date_to:
            filter_conditions['Timestamp'] = {
                '$gte': datetime.strptime(date_from, "%Y-%m-%d"),
                '$lte': datetime.strptime(date_to, "%Y-%m-%d")
            }

        activities = ActivityLog.get_activities(filter_conditions)
        return Response(activities, status=status.HTTP_200_OK)

class UserLoginLogoutView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        action_type = "login"
        ActivityLog.add_activity(user_id, action_type, "User logged in.")
        return Response({"message": "Login successful."}, status=status.HTTP_200_OK)

    def delete(self, request):
        user_id = request.data.get('user_id')
        action_type = "logout"
        ActivityLog.add_activity(user_id, action_type, "User logged out.")
        return Response({"message": "Logout successful."}, status=status.HTTP_200_OK)

class TemplateEditView(APIView):
    def put(self, request):
        user_id = request.data.get('user_id')
        action_type = "edit_template"
        template_name = request.data.get('template_name')
        ActivityLog.add_activity(user_id, action_type, f"Edited template: {template_name}.")
        return Response({"message": "Template edited successfully."}, status=status.HTTP_200_OK)




########################

