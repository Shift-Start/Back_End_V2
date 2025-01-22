from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from bson.errors import InvalidId
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from bson import ObjectId
from rest_framework.permissions import AllowAny
from .serializers import AddTemplateTaskSerializer, TaskSerializer, TemplateSerializer
from .models import Task, TemplateModel, TemplateTask
from django.views.decorators.csrf import csrf_exempt

def convert_object_id_to_string(task):
    task['_id'] = str(task['_id'])
    return task

class TaskListCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        try:
            data['Date'] = datetime.combine(datetime.strptime(data['Date'], '%Y-%m-%d'), datetime.min.time())
            data['StartDate'] = datetime.fromisoformat(data['StartDate'])
            data['EndDate'] = datetime.fromisoformat(data['EndDate'])
        except (ValueError, KeyError) as e:
            return Response({"error": "Invalid date format. Use 'YYYY-MM-DDTHH:MM:SS'."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = TaskSerializer(data=data)

        if serializer.is_valid():
            task_data = serializer.validated_data
            task_data['created_at'] = datetime.utcnow()
            task_data['updated_at'] = datetime.utcnow()

            created_task = Task.collection.insert_one(task_data)
            task_data['_id'] = str(created_task.inserted_id)
            return Response(task_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        tasks = list(Task.collection.find())
        task_list = [convert_object_id_to_string(task) for task in tasks]
        return Response(task_list, status=status.HTTP_200_OK)

#استرجاع مهمة معينة باستخدام معرف المهمة.
class TaskDetailView(APIView):
    def get(self, request, task_id):
        try:
            task = Task.get_task_by_id(task_id)
            if task:
                return Response(task, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# استرجاع جميع المهام الخاصة بمستخدم معين
class UserTasksView(APIView):
    def get(self, request, user_id):
        tasks, status_code = Task.get_tasks_by_user_id(user_id)
        if status_code == 200:
            return Response(tasks, status=status.HTTP_200_OK)
        return Response(tasks, status=status.HTTP_404_NOT_FOUND if status_code == 404 else status.HTTP_500_INTERNAL_SERVER_ERROR)

# حذف التاسك
class TaskDeleteView(APIView):
    def delete(self, request, task_id):
        if not ObjectId.is_valid(task_id):
            return Response({"error": "Invalid Task ID"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            result, http_status = Task.delete_task(task_id)
            return Response(result, status=http_status)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# تعديل التاسك
class UpdateTaskView(APIView):
    def put(self, request, task_id):
        try:
            task_data = request.data
            result, code = Task.update_task(task_id, task_data)
            return Response(result, status=code)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# استدعاء الدالة لاسترجاع جميع المهام
class GetAllTasksView(APIView):
    def get(self, request):
        try:
            tasks = Task.get_all_tasks()
            return Response({"tasks": tasks}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

          #عرض القوالب وإضافتها
class TemplateView(APIView):
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

class DeleteTemplateByNameView(APIView):
    @csrf_exempt  # تعطيل التحقق من CSRF لهذا المستخدم
    def delete(self, request, template_name):
        try:
            result = TemplateModel.collection.delete_one({"name": template_name})
            if result.deleted_count > 0:
                return JsonResponse({"message": f"Template '{template_name}' deleted successfully."}, status=200)
            else:
                return JsonResponse({"error": f"No template found with name '{template_name}'."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

class DeleteTemplateByIdView(APIView):
    @csrf_exempt  # تعطيل التحقق من CSRF لهذا المستخدم
    def delete(self, request, template_id):
        try:
            if not ObjectId.is_valid(template_id):
                return JsonResponse({"error": "Invalid Template ID"}, status=400)
            result = TemplateModel.collection.delete_one({"_id": ObjectId(template_id)})
            if result.deleted_count > 0:
                return JsonResponse({"message": f"Template with ID '{template_id}' deleted successfully."}, status=200)
            else:
                return JsonResponse({"error": f"No template found with ID '{template_id}'."}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

class AddTemplateTaskView(APIView):
    permission_classes = [AllowAny]
#      permission_classes = [IsAdminUser] يجب تبديله الى ان تكون ادمن فقط من يستطيع الوصول

    #  لإضافة مهام جديدة إلى جدول template_task
    def post(self, request):
        #(الاصلي موجود تحته للتجريب فقطططططط)
        user = request.user
        if not user.is_authenticated:
            user.is_admin = True  # تحديد هذا يدويًا فقط للتجربة

        # التحقق من صلاحية المستخدم كأدمن
        if not getattr(user, 'is_admin', False):  # تحقق من أن المستخدم هو المسؤول
            return Response({"error": "Permission denied. Admins only."}, status=status.HTTP_403_FORBIDDEN)

        #(هذه من اجل المستخد يجب تسجيل دخوله )
        # التحقق من أن المستخدم مسجل الدخول وأنه مسؤول
        # user = request.user
        # if not user.is_authenticated:
        #     return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

        # if not getattr(user, 'is_admin', False):  # تحقق من أن المستخدم هو المسؤول
        #     return Response({"error": "Permission denied. Admins only."}, status=status.HTTP_403_FORBIDDEN)

        # استلام البيانات والتحقق من صحتها
        serializer = AddTemplateTaskSerializer(data=request.data)
        if serializer.is_valid():
            try:
                # تمرير البيانات للتحقق
                task_data = serializer.validated_data
                result = TemplateTask.add_task_to_template(task_data)
                # تحويل الحقول التي تحتوي على ObjectId إلى نصوص قبل الإرجاع
                result['_id'] = str(result['_id'])
                result['TemplateID'] = str(result['TemplateID'])

                return Response(
                    {"message": "Task added to template successfully", "task": result},
                    status=status.HTTP_201_CREATED
                )
            except ValueError as ve:
                return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # في حالة كانت البيانات غير صحيحة
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTemplateTaskView(APIView):
    permission_classes = [AllowAny]
#      permission_classes = [IsAdminUser] يجب تبديله الى ان تكون ادمن فقط من يستطيع الوصول

    def delete(self, request):
        # استلام TemplateID و TaskID والتحقق من وجودهما
        template_id, task_id = request.data.get("TemplateID"), request.data.get("TaskID")
        if not template_id or not task_id:
            return Response({"error": "TemplateID and TaskID are required."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # تحويل TemplateID و TaskID إلى ObjectId
            template_id, task_id = ObjectId(template_id), ObjectId(task_id)
            # البحث عن المهمة
            task = TemplateTask.collection.find_one({"_id": task_id, "TemplateID": template_id})
            if not task:
                return Response({"error": "Task not found in the template."}, status=status.HTTP_404_NOT_FOUND)
            # حذف المهمة
            TemplateTask.collection.delete_one({"_id": task_id})
            return Response({"message": "Task deleted successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateTemplateTaskView(APIView):
    permission_classes = [AllowAny]

    def put(self, request):
        # التحقق من الحقول المطلوبة
        required_fields = ["TemplateID", "_id", "UpdatedData"]
        missing_fields = [field for field in required_fields if not request.data.get(field)]
        if missing_fields:
            return Response({"error": f"Missing required fields: {', '.join(missing_fields)}"}, status=status.HTTP_400_BAD_REQUEST)

        template_id = request.data["TemplateID"]
        task_id = request.data["_id"]
        updated_data = request.data["UpdatedData"]

        if not isinstance(updated_data, dict) or not updated_data:
            return Response({"error": "UpdatedData must be a non-empty dictionary."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # تحويل TemplateID و _id إلى ObjectId
            template_id, task_id = ObjectId(template_id), ObjectId(task_id)
            # البحث عن المهمة
            task = TemplateTask.collection.find_one({"_id": task_id, "TemplateID": template_id})
            if not task:
                return Response({"error": "Task not found in the template."}, status=status.HTTP_404_NOT_FOUND)
            # تحديث المهمة
            TemplateTask.collection.update_one({"_id": task_id}, {"$set": updated_data})
            # جلب المهمة المحدثة وتحويل ObjectId إلى نص
            updated_task = TemplateTask.collection.find_one({"_id": task_id})
            updated_task['_id'], updated_task['TemplateID'] = str(updated_task['_id']), str(updated_task['TemplateID'])
            return Response({"message": "Task updated successfully.", "task": updated_task}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class AssignTemplateTasksView(APIView):
    #لنقل المهام من قالب إلى جدول المهام للمستخدم المحدد.
    permission_classes = [AllowAny]
    def post(self, request, template_id):
        try:
            # الحصول على user_id من الطلب
            user_id = request.data.get("user_id")
            if not user_id:
                return Response({"error": "User ID is required"}, status=400)
            try:
                ObjectId(template_id)
            except InvalidId:
                return Response({"error": "Invalid template ID format"}, status=400)
            # استدعاء الوظيفة لنقل المهام
            result = TemplateTask.transfer_template_tasks_to_user(template_id, user_id)
            return Response(result, status=201)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=400)
        except Exception as e:
            return Response({"error": f"Unexpected error: {str(e)}"}, status=500)
