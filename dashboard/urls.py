from django.urls import path
from .views import TeamView, TeamMemberView, DashboardTaskListView, DashboardTaskDetailView ,DashboardTemplateView, DashboardTemplateDetailView,RecommendationView, RecommendationDetailView ,ReportView, DownloadReportView,ActivityLogView, UserLoginLogoutView, TemplateEditView                    

urlpatterns = [
    # path('teams-dashboard/', TeamDashboardView.as_view(), name='team_dashboard'),
    # path('teams/', TeamListView.as_view(), name='team-list'),
    path('teams/', TeamView.as_view(), name='team-list'),  # عرض جميع الفرق أو إنشاء فريق
    path('teams/<int:team_id>/', TeamView.as_view(), name='team-detail'),  # عرض تفاصيل فريق معين أو تحديثه أو حذفه

    # URLs الخاصة بعضو الفريق
    path('team_members/', TeamMemberView.as_view(), name='team-member-list'),  # عرض جميع أعضاء الفرق أو إضافة عضو جديد
    path('team_members/<int:member_id>/', TeamMemberView.as_view(), name='team-member-detail'),  # عرض تفاصيل عضو معين أو تحديثه أو حذفه

    path('tasks/', DashboardTaskListView.as_view(), name='dashboard-task-list'),  # عرض قائمة المهام
    path('tasks/<str:task_id>/', DashboardTaskDetailView.as_view(), name='dashboard-task-detail'),  # عرض تفاصيل مهمة واحدة
    path('templates/', DashboardTemplateView.as_view(), name='dashboard-template-list'),
    path('templates/<str:template_id>/', DashboardTemplateDetailView.as_view(), name='dashboard-template-detail'),
    path('recommendations/', RecommendationView.as_view(), name='recommendation-list'),
    path('recommendations/<str:rec_id>/', RecommendationDetailView.as_view(), name='recommendation-detail'),
    path('reports/<str:report_type>/', ReportView.as_view(), name='generate-report'),
    path('reports/<str:report_type>/<str:format>/', DownloadReportView.as_view(), name='download-report'),
    path('activity-log/', ActivityLogView.as_view(), name='activity-log'),
    path('user/login/', UserLoginLogoutView.as_view(), name='user-login'),
    path('user/logout/', UserLoginLogoutView.as_view(), name='user-logout'),
    path('template/edit/', TemplateEditView.as_view(), name='template-edit'),
]


