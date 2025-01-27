from django.urls import path
from .views import (
    RewardCreateView,
    RewardUpdateView,
    RewardDeleteView,
    # RewardProgressUpdateView
    RewardListView
)
urlpatterns = [
    path('rewards/create/', RewardCreateView.as_view(), name='reward-create'),
    path('rewards/<str:reward_id>/update/', RewardUpdateView.as_view(), name='reward-update'),
    path('rewards/<str:reward_id>/delete/', RewardDeleteView.as_view(), name='reward-delete'),
    path('rewards/list/', RewardListView.as_view(), name='reward-list'),
]
