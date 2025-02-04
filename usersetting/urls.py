from django.urls import path
from usersetting.views import UserSettingsView

urlpatterns = [
    path('settings/<str:user_id>/', UserSettingsView.as_view(), name='user-settings'),
]
