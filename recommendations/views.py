from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Recommendation
from .serializers import RecommendationSerializer
from datetime import datetime

class RecommendationView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # استرجاع جميع التوصيات
        recommendations = Recommendation.get_all_recommendations()
        return Response(recommendations, status=status.HTTP_200_OK)

    def post(self, request):
        # التحقق من صحة البيانات باستخدام الـ Serializer
        serializer = RecommendationSerializer(data=request.data)
        if serializer.is_valid():
            # الحصول على البيانات من الـ Serializer
            validated_data = serializer.validated_data
            # إضافة التوصية إلى قاعدة البيانات
            recommendation = Recommendation.add_recommendation({
                "UserID": validated_data['UserID'],
                "Content": validated_data['Content'],
                "CreatedAt": datetime.now()  # تعيين تاريخ الإنشاء الحالي
            })
            return Response(recommendation, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
