from django.db import models
from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient


client = MongoClient("mongodb://127.0.0.1:27017/")
db = client['Shift-Start-db']

class Team:
    collection = db['teams']
    collection.create_index("name", unique=True)  # إضافة فهرس لتحسين البحث

    @staticmethod
    def create_team(data):
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        result = Team.collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data

    @staticmethod
    def get_team(team_id):
        if not ObjectId.is_valid(team_id):
            return None
        team = Team.collection.find_one({"_id": ObjectId(team_id)}, {"_id": 0})
        return team

    @staticmethod
    def get_all_teams():
        return list(Team.collection.find({}, {"_id": 0}))

    @staticmethod
    def update_team(team_id, data):
        if not ObjectId.is_valid(team_id):
            return False
        data['updated_at'] = datetime.utcnow()
        result = Team.collection.update_one({"_id": ObjectId(team_id)}, {"$set": data})
        return result.modified_count > 0

    @staticmethod
    def delete_team(team_id):
        if not ObjectId.is_valid(team_id):
            return False
        result = Team.collection.delete_one({"_id": ObjectId(team_id)})
        return result.deleted_count > 0

class TeamMember:
    collection = db['team_members']
    collection.create_index("email", unique=True)  # إضافة فهرس لتحسين البحث

    @staticmethod
    def add_team_member(data):
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        result = TeamMember.collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data

    @staticmethod
    def get_team_member(team_member_id):
        if not ObjectId.is_valid(team_member_id):
            return None
        member = TeamMember.collection.find_one({"_id": ObjectId(team_member_id)}, {"_id": 0})
        return member

    @staticmethod
    def get_all_team_members():
        return list(TeamMember.collection.find({}, {"_id": 0}))

    @staticmethod
    def update_team_member(team_member_id, data):
        if not ObjectId.is_valid(team_member_id):
            return False
        data['updated_at'] = datetime.utcnow()
        result = TeamMember.collection.update_one({"_id": ObjectId(team_member_id)}, {"$set": data})
        return result.modified_count > 0

    @staticmethod
    def delete_team_member(team_member_id):
        if not ObjectId.is_valid(team_member_id):
            return False
        result = TeamMember.collection.delete_one({"_id": ObjectId(team_member_id)})
        return result.deleted_count > 0



# models.py

from pymongo import MongoClient

class Task:
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client["API_Pro"]
    collection = db["tasks"]

    @staticmethod
    def get_all_tasks():
        # استرجاع المهام مع الحقول المطلوبة فقط
        return list(Task.collection.find({}, {"_id": 0, "status": 1, "created_at": 1}))

    @staticmethod
    def get_task_by_id(task_id):
        # استرجاع مهمة واحدة مع الحقول المطلوبة فقط
        return Task.collection.find_one({"task_id": task_id}, {"_id": 0, "status": 1, "created_at": 1})


class TemplateModel:
    client = MongoClient("mongodb://127.0.0.1:27017/")
    db = client["API_Pro"]
    collection = db["templates"]

    @staticmethod
    def get_all_templates():
        templates = list(TemplateModel.collection.find({}, {"_id": 1, "name": 1, "description": 1, "CreatedAt": 1}))
        for template in templates:
            template['_id'] = str(template['_id'])
        return templates

    @staticmethod
    def insert_template(name, description):
        data = {
            "name": name,
            "description": description,
            "CreatedAt": datetime.utcnow()
        }
        result = TemplateModel.collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data

    @staticmethod
    def update_template(template_id, updated_data):
        if not ObjectId.is_valid(template_id):
            return {"error": "Invalid Template ID"}, 400
        result = TemplateModel.collection.update_one({"_id": ObjectId(template_id)}, {"$set": updated_data})
        if result.matched_count > 0:
            return {"message": "Template updated successfully."}, 200
        else:
            return {"error": "Template not found."}, 404

    @staticmethod
    def delete_template_by_id(template_id):
        if not ObjectId.is_valid(template_id):
            return {"error": "Invalid Template ID"}, 400
        result = TemplateModel.collection.delete_one({"_id": ObjectId(template_id)})
        if result.deleted_count > 0:
            return {"message": "Template deleted successfully."}, 200
        else:
            return {"error": "Template not found."}, 404


#####

class Recommendation:
    collection = db['recommendations']
    users_collection = db['users']  # افتراضياً أن المستخدمين مخزنون هنا

    @staticmethod
    def get_all_recommendations():
        try:
            recommendations = Recommendation.collection.find()
            result = []
            for rec in recommendations:
                user = Recommendation.users_collection.find_one({"_id": ObjectId(rec['UserID'])})
                rec['_id'] = str(rec['_id'])
                rec['UserName'] = user['name'] if user else "Unknown"
                result.append(dict(rec))
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve recommendations: {e}")

    @staticmethod
    def add_recommendation(data):
        data['CreatedAt'] = datetime.utcnow()
        data['_id'] = ObjectId()
        try:
            result = Recommendation.collection.insert_one(data)
            data['_id'] = str(result.inserted_id)
            return data
        except Exception as e:
            raise RuntimeError(f"Failed to add recommendation: {e}")

    @staticmethod
    def get_recommendation_by_id(rec_id):
        try:
            if not ObjectId.is_valid(rec_id):
                return {"error": "Invalid Recommendation ID"}, 400
            rec = Recommendation.collection.find_one({"_id": ObjectId(rec_id)})
            if rec:
                rec['_id'] = str(rec['_id'])
                return rec, 200
            else:
                return {"error": "Recommendation not found."}, 404
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def archive_recommendation(rec_id):
        try:
            if not ObjectId.is_valid(rec_id):
                return {"error": "Invalid Recommendation ID"}, 400
            result = Recommendation.collection.update_one(
                {"_id": ObjectId(rec_id)}, {"$set": {"archived": True}}
            )
            if result.matched_count > 0:
                return {"message": "Recommendation archived successfully."}, 200
            else:
                return {"error": "Recommendation not found."}, 404
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def delete_recommendation(rec_id):
        try:
            if not ObjectId.is_valid(rec_id):
                return {"error": "Invalid Recommendation ID"}, 400
            result = Recommendation.collection.delete_one({"_id": ObjectId(rec_id)})
            if result.deleted_count > 0:
                return {"message": "Recommendation deleted successfully."}, 200
            else:
                return {"error": "Recommendation not found."}, 404
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500
        
#########
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pymongo import MongoClient
import pandas as pd
from django.http import HttpResponse

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


##################3

class ActivityLog:
    collection = db['activity_logs']  # تخزين النشاطات هنا

    @staticmethod
    def add_activity(user_id, action_type, details):
        activity = {
            'UserID': user_id,
            'ActionType': action_type,
            'Details': details,
            'Timestamp': datetime.utcnow()
        }
        try:
            result = ActivityLog.collection.insert_one(activity)
            return activity
        except Exception as e:
            raise RuntimeError(f"Failed to add activity: {e}")

    @staticmethod
    def get_activities(filter_conditions=None):
        try:
            activities = ActivityLog.collection.find(filter_conditions) if filter_conditions else ActivityLog.collection.find()
            result = []
            for activity in activities:
                activity['_id'] = str(activity['_id'])
                result.append(activity)
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve activities: {e}")