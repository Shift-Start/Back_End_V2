from django.urls import path
from competitor.views import CompetitorsListAPIView

urlpatterns = [
    path('competitors/', CompetitorsListAPIView.as_view(), name='competitors'),
]


# from django.urls import path
# from habit.views import HabitListCreateView, HabitDetailView , DailyUpdatesView

# urlpatterns = [
#     path('habits/', HabitListCreateView.as_view(), name='habit-list-create'),
#     path('habits/<str:habit_id>/', HabitDetailView.as_view(), name='habit-detail'),
#     path('habits/daily-updates/', DailyUpdatesView.as_view(), name='daily-updates'),
    
# ]
