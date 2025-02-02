from django.urls import path
from .views import (
    RewardCreateView,
    RewardUpdateView,
    RewardDeleteView,
    UserRewardView,
    RewardListView,
    UserRewardHistoryView
)
urlpatterns = [
    #          إنشاء جائزة
    path('rewards/create/', RewardCreateView.as_view(), name='reward-create'),
    #          التعديل على جائزة
    path('rewards/<str:reward_id>/update/', RewardUpdateView.as_view(), name='reward-update'),
    #         حذف جائزة
    path('rewards/<str:reward_id>/delete/', RewardDeleteView.as_view(), name='reward-delete'),
    #          عرض كل الجوائز
    path('rewards/list/', RewardListView.as_view(), name='reward-list'),
    #          المكافأة المعطاو للمستخدم
    path('rewards/grant/', UserRewardView.as_view(), name='grant-reward'),
    #          ارجاع كل الجوائز الخاصة بمستخدم معين
    path('rewards/history/<str:user_id>/', UserRewardHistoryView.as_view(), name='user-reward-history'),

]
# http://127.0.0.1:8000/rewards/rewards/create/ إنشاء جائزة
# {
#     "name": "Daily Login",
#     "description": "Reward for logging in daily.",
#     "points_required": 30
# }

#http://127.0.0.1:8000/rewards/rewards/grant/   ارسال عدد النقاط والتأكد من حصوله على جائزة
# {
#     "user_id": "676313e71c6fa6b40d339c6a",
#     "total_points": 30
# }

#http://127.0.0.1:8000/rewards/rewards/history/676313e71c6fa6b40d339c6a/ استرجاع كل جوائز مستخدم معين

#http://127.0.0.1:8000/rewards/rewards/list/ استرجاع كل الجوائز

#http://127.0.0.1:8000/rewards/rewards/6798d84e78a68cb3d2bee4b2/delete/ حذف جائزة