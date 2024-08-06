# login.py
from static.util.db_tools import DBTools
from ulid import new


class AuthService:
    def __init__(self, db_tools):
        self.db_tools = db_tools

    def login(self, username, password):

        """登录验证"""
        query = "SELECT * FROM user WHERE name = %s AND password = %s"
        user = self.db_tools.fetch_data(query, (username, password))

        if user:
            return {"success": True}
        else:
            return {"success": False}

    def register(self, username, password):
        """注册新用户"""
        # 检查用户是否存在
        query = "SELECT * FROM user WHERE name = %s"
        existing_user = self.db_tools.fetch_data(query, (username))

        if existing_user:
            return {"success": False, "message": "用户名已存在"}

        # 插入新用户
        new_ulid = new()  #生成ulid
        insert_query = "INSERT INTO user (g_id,name, password) VALUES (%s,%s, %s)"
        self.db_tools.execute_query(insert_query, (new_ulid, username, password))
        return {"success": True}

    def get_user_id(self,username):
        """查找用户g_id"""
        query = "SELECT g_id FROM user WHERE name = %s"
        existing_user = self.db_tools.fetch_data(query, (username))

        return existing_user

    def change_password(self,username,password):
        """修改密码"""
        query = "UPDATE user SET password = %s WHERE name = %s"
        back_information = self.db_tools.fetch_data(query, (password, username))

        return back_information

    def get_user_name(self,g_id):
        """查询用户名称"""
        query = "SELECT name FROM user WHERE g_id = %s"
        existing_user = self.db_tools.fetch_data(query, (g_id))
        return existing_user
