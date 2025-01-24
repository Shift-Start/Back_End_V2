from django.urls import path
from .views import (
    RewardListCreateView,
    RewardUpdateView,
    RewardDeleteView
)

urlpatterns = [
    # إنشاء وعرض المكافآت
    path('rewards/', RewardListCreateView.as_view(), name='reward-list-create'),

    # تحديث مكافأة معينة
    path('rewards/<str:reward_id>/', RewardUpdateView.as_view(), name='reward-update'),

    # حذف مكافأة معينة
    path('rewards/<str:reward_id>/delete/', RewardDeleteView.as_view(), name='reward-delete'),
]