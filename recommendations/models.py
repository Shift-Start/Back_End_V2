from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import PyMongoError

client = MongoClient("mongodb://127.0.0.1:27017/")
db = client['Shift-Start-db']

class Recommendation:
    collection = db['recommendations']

    @staticmethod
    def add_recommendation(data):
        current_time = datetime.utcnow()
        data['CreatedAt'] = current_time
        data['_id'] = ObjectId()
        try:
            result = Recommendation.collection.insert_one(data)
            data['_id'] = str(result.inserted_id)
            return data
        except PyMongoError as e:
            raise RuntimeError(f"Failed to add recommendation: {e}")

    @staticmethod
    def get_all_recommendations():
        try:
            recommendations = Recommendation.collection.find()
            result = []
            for rec in recommendations:
                rec['_id'] = str(rec['_id'])  # تحويل ObjectId إلى سلسلة نصية
                result.append(dict(rec))
            return result
        except PyMongoError as e:
            raise RuntimeError(f"Failed to retrieve recommendations: {e}")

    @staticmethod
    def delete_recommendation(recommendation_id):
        try:
            result = Recommendation.collection.delete_one({"_id": ObjectId(recommendation_id)})
            return result.deleted_count > 0  # إرجاع True إذا تم الحذف بنجاح، وإلا False
        except PyMongoError as e:
            raise RuntimeError(f"Failed to delete recommendation: {e}")
        except Exception:
            return False  # التعامل مع الأخطاء مثل فشل تحويل ObjectId

