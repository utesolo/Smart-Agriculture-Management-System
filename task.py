from datetime import datetime
from flask import session
from static.huawei_iotda_greenhouse import HuaweiIoTDAEnvironment
from static.util.db_tools import DBTools

huawei = HuaweiIoTDAEnvironment()
db_tools = DBTools()


def job_function():
    g_id = session.get('user_id', {}).get('g_id', None)  # 确保处理可能的None或KeyError
    if g_id:
        print(f"{datetime.now()} - 正在将数据存入数据库...")
        huawei.store_environment_data(db_tools, datetime.now(), g_id)
    else:
        print("用户未登录或用户ID未设置")