from django.urls import path
from login.views import LoginAPIView,RegisterAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]


# }
# {
#     "email": "newuser@example.com",
#     "password": "securepassword123"
# }

# {
#     "username": "test_user",
#     "email": "test@example.com",
#     "password": "securepassword123"
# }

# data = {
#     "username": "john_doe",
#     "email": "john@example.com",
#     "password": "securepassword123",
#     "profile_picture": "path/to/profile_picture.jpg"
# }
# new_user = User.create_user(data)
