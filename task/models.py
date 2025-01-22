from datetime import datetime, date
from bson import ObjectId
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# الاتصال بقاعدة البيانات
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client['Shift-Start-db']

class Task:
    collection = db['tasks']

    @staticmethod
    def add_task(data):
        # تحويل التاريخ إذا كان من نوع date إلى datetime
        for key, value in data.items():
            if isinstance(value, date) and not isinstance(value, datetime):
                data[key] = datetime.combine(value, datetime.min.time())
        current_time = datetime.utcnow()
        data['created_at'] = current_time
        data['updated_at'] = current_time
        try:
            result = Task.collection.insert_one(data)
            data['_id'] = str(result.inserted_id)
            return data
        except PyMongoError as e:
            raise RuntimeError(f"Failed to add task: {e}")

    @staticmethod
    def get_task_by_id(task_id):
#         استرجاع مهمة باستخدام معرف المهمة.
        try:
            if not ObjectId.is_valid(task_id):
                raise ValueError(f"Invalid Task ID: {task_id} is not a valid ObjectId")
            task = Task.collection.find_one({"_id": ObjectId(task_id)})
            if task:
                task["_id"] = str(task["_id"])
                return dict(task)
            else:
                return {"error": "Task not found"}, 404
        except ValueError as ve:
            return {"error": str(ve)}, 400
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500
    @staticmethod
    def get_tasks_by_user_id(user_id):
        try:
            tasks_collection = db['tasks']
            tasks_cursor = tasks_collection.find({"UserID": user_id})
            tasks_list = []
            for task in tasks_cursor:
                task["_id"] = str(task["_id"])
                tasks_list.append(task)
            if not tasks_list:
                return {"error": "No tasks found for this user"}, 404
            return tasks_list, 200
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def delete_task(task_id):
        try:
            if not ObjectId.is_valid(task_id):
                return {"error": "Invalid Task ID"}, 400
            result = Task.collection.delete_one({"_id": ObjectId(task_id)})
            if result.deleted_count > 0:
                return {"message": "Task deleted successfully"}, 200
            else:
                return {"error": "Task not found"}, 404
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @staticmethod
    def update_task(task_id, data):
        # تحديث بيانات المهمة باستخدام معرف المهمة
        try:
            if not ObjectId.is_valid(task_id):
                return {"error": "Invalid Task ID"}, 400
            data['updated_at'] = datetime.utcnow()
            result = Task.collection.update_one({"_id": ObjectId(task_id)}, {"$set": data})
            if result.matched_count == 0:
                return {"error": "Task not found"}, 404
            elif result.modified_count > 0:
                return {"message": "Task updated successfully"}, 200
            else:
                return {"message": "No changes made to the task"}, 304
        except Exception as e:
            return {"error": f"Error while updating task: {str(e)}"}, 500

    @staticmethod
    def get_all_tasks():
        try:
            tasks_cursor = Task.collection.find()
            tasks_list = []
            for task in tasks_cursor:
                task["_id"] = str(task["_id"])
                tasks_list.append(task)
            return tasks_list
        except Exception as e:
            raise ValueError(f"Error while retrieving tasks: {e}")


# اسماء القوالب
class TemplateModel:
    collection = db['Template_name']
#إضافة قالب
    @staticmethod
    def insert_template(name, description):
        data = {
            "name": name,
            "description": description,
            "CreatedAt": datetime.utcnow()
        }
        result = TemplateModel.collection.insert_one(data)
        data['_id'] = str(result.inserted_id)
        return data

    @staticmethod
    def get_all_templates():
        templates = list(TemplateModel.collection.find())
        for template in templates:
            template['_id'] = str(template['_id'])
        return templates

    @staticmethod
    def delete_template_by_name(template_name):
        try:
            result = TemplateModel.collection.delete_one({"name": template_name})
            if result.deleted_count > 0:
                return {"message": f"Template '{template_name}' deleted successfully."}, 200
            else:
                return {"error": f"No template found with name '{template_name}'."}, 404
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500

    @staticmethod
    def delete_template_by_id(template_id):
        try:
            if not ObjectId.is_valid(template_id):
                return {"error": "Invalid Template ID"}, 400
            result = TemplateModel.collection.delete_one({"_id": ObjectId(template_id)})
            if result.deleted_count > 0:
                return {"message": f"Template with ID '{template_id}' deleted successfully."}, 200
            else:
                return {"error": f"No template found with ID '{template_id}'."}, 404
        except Exception as e:
            return {"error": f"An error occurred: {str(e)}"}, 500

class TemplateTask:
    collection = db['template_task']  # مجموعة المهام الخاصة بالقوالب

    @staticmethod
    def add_task_to_template(data):
        # إضافة مهمة جديدة إلى جدول template_task
        try:
            # التحقق من الحقول المطلوبة
            required_fields = ["TemplateID", "TaskName", "Description", "StartDate", "EndDate", "Date", "Point", "Status", "Repetition"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")

            if 'TemplateID' in data and isinstance(data['TemplateID'], str):
                try:
                    data['TemplateID'] = ObjectId(data['TemplateID'])
                except Exception as e:
                    raise ValueError(f"Invalid TemplateID format: {e}")
            # التحقق من وجود القالب في جدول القوالب
            template_exists = TemplateModel.collection.find_one({"_id": data['TemplateID']})
            if not template_exists:
               raise ValueError(f"Template with ID {data['TemplateID']} does not exist.")
            # تحويل الحقل Date إذا كان من النوع datetime.date
            if 'Date' in data:
                date_value = data['Date']
                if isinstance(date_value, date):  # التحقق مما إذا كان التاريخ من نوع date
                   data['Date'] = datetime.combine(date_value, datetime.min.time())

            # إضافة الوقت الحالي كوقت الإنشاء والتحديث
            current_time = datetime.utcnow()
            data['created_at'] = current_time
            data['updated_at'] = current_time

            # إدخال البيانات إلى جدول template_task
            result = TemplateTask.collection.insert_one(data)
            data['_id'] = str(result.inserted_id)
            return data
        except PyMongoError as e:
            raise RuntimeError(f"Failed to add task to template: {e}")
        except ValueError as e:
            raise e

    @staticmethod
    def delete_task_from_template(template_id, task_id):
        try:
            # التأكد من تحويل الحقول إلى ObjectId
            template_id = ObjectId(template_id)
            task_id = ObjectId(task_id)
            # حذف المهمة بناءً على TemplateID و TaskID
            result = TemplateTask.collection.delete_one({
                "TemplateID": template_id,
                "TaskID": task_id
            })
            # التحقق مما إذا تم حذف المهمة بنجاح
            if result.deleted_count > 0:
                return {"message": "Task deleted successfully"}
            else:
                return {"error": "Task not found"}, 404
        except Exception as e:
            raise RuntimeError(f"Failed to delete task from template: {e}")

    @staticmethod
    def update_task_in_template(template_id, task_id, updated_data):
        try:
        # التأكد من تحويل الحقول إلى ObjectId
            template_id = ObjectId(template_id)
            task_id = ObjectId(task_id)
        # التحقق من وجود المهمة قبل التحديث
            task = TemplateTask.collection.find_one({
                "_id": task_id,
                "TemplateID": template_id
            })
            if not task:
                return {"error": "Task not found"}, 404
        # تحديث بيانات المهمة باستخدام $set
            result = TemplateTask.collection.update_one(
                {"_id": task_id, "TemplateID": template_id},
                {"$set": updated_data}
            )
        # التحقق من نجاح التحديث
            if result.modified_count > 0:
            # جلب المهمة بعد التحديث لإعادتها كاستجابة
                updated_task = TemplateTask.collection.find_one({"_id": task_id})
                updated_task["_id"] = str(updated_task["_id"])  # تحويل ObjectId إلى نص
                updated_task["TemplateID"] = str(updated_task["TemplateID"])  # تحويل ObjectId إلى نص
                return {"message": "Task updated successfully", "task": updated_task}
            else:
                return {"error": "No changes were made to the task"}, 400
        except Exception as e:
            raise RuntimeError(f"Failed to update task in template: {e}")

    @staticmethod
    def transfer_template_tasks_to_user(template_id, user_id):
        """
        # نقل المهام المرتبطة بالقالب المحدد إلى جدول المهام للمستخدم المحدد.
        """
        # جلب المهام من مجموعة template_task
        template_tasks = TemplateTask.collection.find({"TemplateID": ObjectId(template_id)})

        if TemplateTask.collection.count_documents({"TemplateID": ObjectId(template_id)}) == 0:
            raise ValueError("No tasks found for the selected template.")

        # إعداد المهام الجديدة لإضافتها إلى مجموعة tasks
        new_tasks = []
        for task in template_tasks:
            new_task = {
                "TemplateID": str(task["TemplateID"]),
                "UserID": str(user_id),
                "TaskName": task.get("TaskName", ""),
                "StartDate": task.get("StartDate"),
                "Description": task.get("Description", ""),
                "EndDate": task.get("EndDate"),
                "Repetition": task.get("Repetition", ""),
                "Point": task.get("Point", 0),
                "Status": "Pending",
                "CreatedAt": datetime.utcnow(),
                "UpdatedAt": datetime.utcnow(),
            }
            new_tasks.append(new_task)

        # إدخال المهام في مجموعة tasks
        tasks_collection = db["tasks"]
        result = tasks_collection.insert_many(new_tasks)

        return {
            "message": "Tasks transferred successfully",
            "transferred_task_count": len(result.inserted_ids),
            "task_ids": [str(task_id) for task_id in result.inserted_ids],
        }











