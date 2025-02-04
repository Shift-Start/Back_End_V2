
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from competitor.serializers import CompetitorSerializer
from account.models import User

class CompetitorsListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # جلب جميع المستخدمين مرتبين حسب النقاط تنازليًا
        users = User.get_all_users_sorted_by_points()
        serializer = CompetitorSerializer(users, many=True)

        # استجابة API مع رسالة تحفيزية
        return Response(
            {
                "message": "Competitors list fetched successfully.",
                "note": "Climb the leaderboard and stay motivated by tracking your progress!",
                "competitors": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
