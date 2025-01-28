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
