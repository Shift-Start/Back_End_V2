import bcrypt
from rest_framework import serializers
from account.models import User

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        user = User.get_user_by_email(data['email'])
        if not user:
            raise serializers.ValidationError({"email": "User does not exist."})
        
        # التحقق من كلمة السر باستخدام bcrypt
        if not User.check_password(user['password'], data['password']):
            raise serializers.ValidationError({"password": "Invalid password."})
        
        return data


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    is_admin = serializers.BooleanField(required=False, default=False)
    permissions = serializers.ListField(child=serializers.CharField(), required=False)
    date_of_birth = serializers.DateField(required=False)  # جعل الحقل غير مطلوب
    gender = serializers.ChoiceField(choices=["male", "female"], required=False)  # جعل الحقل غير مطلوب
    profile_image = serializers.CharField(required=False)  # جعل الحقل غير مطلوب

    def validate(self, data):
        # التأكد من أن المستخدم ليس مسجلاً مسبقًا بنفس البريد الإلكتروني أو الاسم
        if User.get_user_by_email(data['email']):
            raise serializers.ValidationError({"email": "Email is already taken."})
        if User.get_user_by_username(data['username']):
            raise serializers.ValidationError({"username": "Username is already taken."})
        return data

    def create(self, validated_data):
        # إعداد البيانات وإنشاء المستخدم
        user_data = validated_data
        # تشفير كلمة المرور باستخدام bcrypt
        hashed_password = bcrypt.hashpw(user_data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user_data['password'] = hashed_password
        
        # إنشاء المستخدم باستخدام الدالة الموجودة في `User`
        User.create_user(user_data)
        return user_data
    

    
