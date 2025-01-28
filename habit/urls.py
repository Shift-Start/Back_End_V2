from django.urls import path
from .views import HabitListCreateView, DailyUpdatesView,PuzzleProgressView, HabitSortView , HabitDetailView , HabitInteractionView,ChallengeView



urlpatterns = [
    path('habits/', HabitListCreateView.as_view(), name='habit-list-create'),
    path('habits/daily-updates/', DailyUpdatesView.as_view(), name='daily-updates'),
    path('habits/sort/', HabitSortView.as_view(), name='habit-sort'),
    path('habits/<str:habit_id>/', HabitDetailView.as_view(), name='habit-detail'),
    path('habits/<str:habit_id>/interact/', HabitInteractionView.as_view(), name='habit-interact'),
    path('challenges/', ChallengeView.as_view(), name='challenge-list-create'),  # عرض قائمة التحديات وإضافة تحدٍ جديد
    path('challenges/<str:challenge_id>/', ChallengeView.as_view(), name='challenge-detail'),  # تفاصيل أو تعديل أو حذف تحدٍ
    path('habits/<str:habit_id>/puzzle-progress/', PuzzleProgressView.as_view(), name='puzzle-progress'),

    
]


