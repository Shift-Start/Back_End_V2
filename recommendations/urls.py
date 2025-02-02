from django.urls import path
from .views import RecommendationView

urlpatterns = [
    path('recommendations/', RecommendationView.as_view(), name='recommendations'),
    path('recommendations/delete/', RecommendationView.as_view(), name='recommendations'),
]


#http://127.0.0.1:8000/recommendations/recommendations/ استرجاع جميع التوصيات

#http://127.0.0.1:8000/recommendations/recommendations/ ارسال  توصية
#{
#     "UserID": "676313e71c6fa6b40d339c6a",
#     "Content": "You are great for making an app like this."
# }

#http://127.0.0.1:8000/recommendations/recommendations/delete/
# {
#     "RecommendationID":"67913c122e6f360538d6462c"
# }

