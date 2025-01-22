from django.urls import path
from task.views import (
    TaskDetailView,
    TaskListCreateView,
    UserTasksView,
    TaskDeleteView,
    UpdateTaskView,
    GetAllTasksView,
    TemplateView,
    DeleteTemplateByNameView,
    DeleteTemplateByIdView,
    AddTemplateTaskView,
    DeleteTemplateTaskView,
    UpdateTemplateTaskView,
    AssignTemplateTasksView
)

urlpatterns = [
    # إنشاء وعرض المهام
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    # استرجاع مهمة معينة عن طريق TaskID
    path('tasks/<str:task_id>/', TaskDetailView.as_view(), name='task-detail'),
    # استرجاع جميع المهام الخاصة بمستخدم معين
    path('tasks/user/<str:user_id>/', UserTasksView.as_view(), name='user-tasks'),
    # حذف المهمة عن طريق id المهمة
    path('tasks/delete/<str:task_id>/', TaskDeleteView.as_view(), name='delete_task'),
    # تعديل على مهمة عم طريق id التاسك
    path('tasks/update/<str:task_id>/', UpdateTaskView.as_view(), name='update_task'),
    # استرجاع كافة المهام في قاعدة البيانات
    path('tasks/', GetAllTasksView.as_view(), name='get_all_tasks'),
    # إضافة قالب وعرض القوالب الموجودة
    path('templates/', TemplateView.as_view(), name='template_list_create'),
    #حذف القالب عن طريق الاسم
    path('delete/template/name/<str:template_name>/', DeleteTemplateByNameView.as_view(), name='delete_template_by_name'),
    #حذف القالب عن طريق id القالب
    path('delete/template/id/<str:template_id>/', DeleteTemplateByIdView.as_view(), name='delete_template_by_id'),
    #إضافة تاسك خاص بالقالب
    path('template-tasks/add/', AddTemplateTaskView.as_view(), name='add-template-task'),
    #حذف تاسك حاص بالقالب عن طريق id القالب , id المهمة
    path('template-tasks/delete/', DeleteTemplateTaskView.as_view(), name='delete_template_task'),
    #التعديل على مهمة القالب
    path('template-tasks/update/', UpdateTemplateTaskView.as_view(), name='update_template_task'),
    #نقل التاسكات من جدول تاسكات القوالب الى جدول التاسكات الكلي
    path('assign-template-tasks/<str:template_id>/', AssignTemplateTasksView.as_view(), name='assign-template-tasks'),

]

#  إضافة مهمة جديدة           http://127.0.0.1:8000/api/tasks/tasks/
# {
#   "UserID": "user123",
#   "Title": "Complete Homework",
#   "Description": "Finish math homework before evening",
#   "Date": "2025-01-15",
#   "StartDate": "2025-01-15T09:00:00",
#   "EndDate": "2025-01-15T12:00:00",
#   "repetition": "None",
#   "Status": "Pending"
# }

# http://127.0.0.1:8000/api/tasks/tasks/67869f5351973cc0e6d796a7/ استرجاع مهمة ما عن طريق id المهمة
# http://localhost:8000/api/tasks/tasks/user/64ae23f5cd6d4a1234567890/  استرجاع مهمة ما عن طريق id المستخدم
# http://127.0.0.1:8000/api/tasks/tasks/delete/6786a881ef3345ac72d5a201/ حذف مهمة عن طريق id المهمة
# http://127.0.0.1:8000/api/tasks/tasks/update/6787db08e744c291dc9b199b/ التعديل على مهمة عن طريق id المهمة
# http://127.0.0.1:8000/api/tasks/tasks/ استرجاع جميع المهام من قاعدة البيانات



####################القوالب ###################################
# http://127.0.0.1:8000/api/tasks/templates/ إضافة قالب وعرض القوالب الموجودة
# http://127.0.0.1:8000/api/tasks/delete/template/name/Normal Day/ حذف قالب باستخدام الاسم
# http://127.0.0.1:8000/api/tasks/delete/template/id/6783098111977c36a859d7d3/ حذف القالب باستخدام id القالب


#http://127.0.0.1:8000/api/tasks/template-tasks/add/ إضافة مهمة الى تاسك معين مع الانتباه الى ان المستخدم يجب ان يكون ادمن 
# {
#     "TemplateID": "6788097711977c36a859d7d2",
#     "TaskID": "task456",
#     "Description": "Sample task description",
#     "StartDate": "2025-01-17T08:00:00Z",
#     "EndDate": "2025-01-17T10:00:00Z",
#     "Date": "2025-01-17",
#     "Point": 10.5,
#     "Status": "Pending",
#     "Repetition": "Daily"
# }

#http://127.0.0.1:8000/api/tasks/template-tasks/delete/ حذف تاسك خاص بالقالب بحيث نعطي الbodey معلومات id القالب و _id المهمة
#مثال
# {
#   "TemplateID": "6788097711977c36a859d7d2",
#   "TaskID": "678a8faee4978149c8a26f8b"
# }
#http://127.0.0.1:8000/api/tasks/template-tasks/update/ التعديل على مهام القالب
#{
#     "TemplateID": "67880a49670aa7facb59617a",
#     "_id": "678ab031fe13894c62f1b19b",
#     "UpdatedData": {
#         "Description": "Updated task description",
#         "StartDate": "2025-01-18T09:00:00.000+00:00",
#         "EndDate": "2025-01-18T11:00:00.000+00:00",
#         "Point": 15.0
#     }
# }
#http://127.0.0.1:8000/api/tasks/assign-template-tasks/67880a49670aa7facb59617a/ نقل التاسكات التي اختارها المستخدم من جدول تاسكات القوالب الى جدول التاسكات الكلي مع اعطاءه id المستخدم
#{
#     "user_id": "676313e71c6fa6b40d339c6a"
# }
