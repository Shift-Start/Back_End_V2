# import bcrypt
# from pymongo import MongoClient
# from datetime import datetime

# client = MongoClient("mongodb://127.0.0.1:27017/")
# db = client['Shift-Start-db']

# class User:
#     collection = db['users']

#     @staticmethod
#     def create_user(data):
#         data['created_at'] = datetime.utcnow()
#         data['updated_at'] = datetime.utcnow()
#         User.collection.insert_one(data)  # إضافة المستخدم إلى collection
#         return data  # هنا نقوم بإرجاع البيانات المُدخلة

#     @staticmethod
#     def get_user_by_email(email):
#         return User.collection.find_one({"email": email})

#     @staticmethod
#     def get_user_by_username(username):
#         return User.collection.find_one({"username": username})

#     @staticmethod
#     def check_password(hashed_password, raw_password):
#         return bcrypt.checkpw(raw_password.encode('utf-8'), hashed_password.encode('utf-8'))

