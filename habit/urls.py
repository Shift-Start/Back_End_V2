from django.urls import path
from habit.views import HabitListCreateView, HabitDetailView

urlpatterns = [
    path('habits/', HabitListCreateView.as_view(), name='habit-list-create'),
]

# {
#     "name": "قراءة كتاب",
#     "repetition": 3,
#     "start_date": "2024-12-01",
#     "end_date": "2024-12-15",
#     "status": true
# }
