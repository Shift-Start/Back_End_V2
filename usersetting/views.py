from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from usersetting.models import Settings
from usersetting.serializers import SettingsSerializer

class UserSettingsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        """ جلب إعدادات المستخدم، وإن لم تكن موجودة يتم إنشاؤها """
        settings = Settings.get_settings_by_user(user_id)

        if not settings:
            # إنشاء إعدادات افتراضية إذا لم تكن موجودة
            settings = Settings.create_settings(user_id)

        serialized_settings = SettingsSerializer(settings).data
        return Response(serialized_settings, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        """ تحديث إعدادات المستخدم """
        settings = Settings.get_settings_by_user(user_id)
        if not settings:
            return Response({"error": "Settings not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = SettingsSerializer(data=request.data)
        if serializer.is_valid():
            Settings.update_settings(user_id, serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
