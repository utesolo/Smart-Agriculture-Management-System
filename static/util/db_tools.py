# db_tools.py
import pymysql
import yaml
import os


def load_config(config_file):
    """从 YAML 文件加载配置信息。"""
    # 获取当前文件所在目录的绝对路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 构建配置文件的完整路径
    config_path = os.path.join(current_dir,config_file)

    with open(config_path, 'r',encoding='utf-8') as file:
        config = yaml.safe_load(file)
    return config['database']


class DBTools:
    def __init__(self, config_file='../../configtest.yaml'):
        # 加载配置文件
        self.config = load_config(config_file)
        # 初始化数据库连接
        self.connection = None

    def connect(self):
        """连接到数据库。"""
        try:
            self.connection = pymysql.connect(**self.config)
            print("已连接到 MySQL 数据库")
        except Exception as e:
            print("连接 MySQL 时出错:", e)

    def disconnect(self):
        """断开与数据库的连接。"""
        if self.connection:
            self.connection.close()
            print("MySQL 连接已关闭")

    def execute_query(self, query, params=None):
        """执行 SQL 查询并返回游标对象。"""
        try:
            with self.connection.cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                self.connection.commit()
                print("查询执行成功")
                return cursor  # 返回游标对象
        except Exception as e:
            print(f"执行查询时出错: {e}")
            return None  # 返回 None 表示出错

    def fetch_data(self, query, params=None):
        """从数据库获取数据。"""
        try:
            with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                result = cursor.fetchall()
                return result
        except Exception as e:
            print(f"获取数据时出错: {e}")
