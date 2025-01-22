from django.urls import path
from .views import (
    UserDetailView, ActivityLogView, LeaderboardView,
    RecommendationsView, NotificationsView, RewardView, ReportView,UserProfileView
)


urlpatterns = [
    path('user/<str:user_id>/', UserDetailView.as_view(), name='user_detail'),
    path('activity-log/<str:user_id>/', ActivityLogView.as_view(), name='activity_log'),  # تعديل الاسم هنا
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('recommendations/', RecommendationsView.as_view(), name='recommendations'),
    path('notifications/<str:user_id>/', NotificationsView.as_view(), name='notifications'),
    path('rewards/<str:user_id>/', RewardView.as_view(), name='rewards'),
    path('reports/<str:user_id>/', ReportView.as_view(), name='reports'),
     path('api/user/profile/', UserProfileView.as_view(), name='user-profile'),

]



# PATCH /user/<user_id>/
# {
#     "username": "new_username",
#     "email": "new_email@example.com",
#     "profile_picture": "https://example.com/new_picture.jpg"
# }



# {
#   "user_id": "1234567890abcdef12345678",
#   "content": "هذه هي التوصية الجديدة التي أريد إضافتها."
# }



# {
#   "report_content": ["تقرير الأداء الشهري", "التقرير حول أداء المستخدم في الشهر الماضي"]
# }
