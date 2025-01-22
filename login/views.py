from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.models import User
from login.serializers import LoginSerializer,RegisterSerializer
from rest_framework.permissions import AllowAny

class LoginAPIView(APIView):
    # السماح لجميع المستخدمين بالوصول دون مصادقة مسبقة
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            # التحقق من وجود المستخدم بناءً على البريد الإلكتروني
            user = User.get_user_by_email(email)
            if not user:
                return Response(
                    {"error": "User does not exist"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # التحقق من كلمة المرور
            if User.check_password(user['password'], password):
                return Response(
                    {
                        "message": "Login successful",
                        "user": {
                            "user_id": str(user['_id']),  # تحويل user_id إلى نص
                            "username": user['username'],
                            "email": user['email'],
                            "is_admin": user.get('is_admin', False),
                        },
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid password"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        # إعادة الأخطاء في حال فشل التحقق من البيانات
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]  # السماح لجميع المستخدمين بالوصول
    def post(self, request):
        # طباعة البيانات المستلمة من العميل
        print(f"Request Data: {request.data}")

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.save()  # حفظ البيانات
            return Response(
                {
                    "message": "User created successfully.",
                    "user": {
                        "user_id": str(user_data['_id']),  # إضافة user_id وتحويله إلى نص
                        "username": user_data['username'],
                        "email": user_data['email'],
                        "is_admin": user_data.get('is_admin', False),  # التعامل مع is_admin بشكل صحيح
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        # في حالة حدوث خطأ في التحقق من البيانات
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









# class LoginAPIView(APIView):
#     def post(self, request):
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             password = serializer.validated_data['password']

#             user = User.get_user_by_email(email)
#             if not user:
#                 return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

#             if User.check_password(user['password'], password):
#                 return Response(
#                     {
#                         "message": "Login successful",
#                         "user": {
#                             "user_id": str(user['_id']),  # إضافة user_id
#                             "username": user['username'],
#                             "email": user['email'],
#                             "is_admin": user.get('is_admin', False),
#                         },
#                     },
#                     status=status.HTTP_200_OK,
#                 )
#             else:
#                 return Response({"error": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RegisterAPIView(APIView):
#     def post(self, request):
#         # طباعة البيانات المستلمة من العميل
#         print(f"Request Data: {request.data}")

#         serializer = RegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             user_data = serializer.save()  # حفظ البيانات
#             return Response(
#                 {
#                     "message": "User created successfully.",
#                     "user": {
#                         "user_id": str(user_data['_id']),  # إضافة user_id وتحويله إلى نص
#                         "username": user_data['username'],
#                         "email": user_data['email'],
#                         "is_admin": user_data.get('is_admin', False),  # التعامل مع is_admin بشكل صحيح
#                     },
#                 },
#                 status=status.HTTP_201_CREATED,
#             )
#         # في حالة حدوث خطأ في التحقق من البيانات
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



