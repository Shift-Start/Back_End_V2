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
        recommendations = Recommendation.get_all_recommendations()
        return Response(recommendations, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RecommendationSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            recommendation = Recommendation.add_recommendation({
                "UserID": validated_data['UserID'],
                "Content": validated_data['Content'],
                "CreatedAt": datetime.now()
            })
            return Response(recommendation, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        recommendation_id = request.data.get("RecommendationID")
        if not recommendation_id:
            return Response({"error": "RecommendationID is required"}, status=status.HTTP_400_BAD_REQUEST)

        deleted = Recommendation.delete_recommendation(recommendation_id)
        if deleted:
            return Response({"message": "Recommendation deleted successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Recommendation not found or could not be deleted"}, status=status.HTTP_404_NOT_FOUND)
