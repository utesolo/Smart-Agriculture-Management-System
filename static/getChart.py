#getChart.py
import os

import pandas as pd
import plotly.graph_objects as go
from static.util.db_tools import DBTools


def getchart(startdate, enddate):
    db_tools = DBTools()
    db_tools.connect()
    query = ("SELECT farm_date, temp, humi, light, smoke, soil, carbon_dioxide FROM data_farm "
             "WHERE DATE(farm_date) BETWEEN %s AND %s")

    cursor = db_tools.execute_query(query, (startdate, enddate))
    columns = [desc[0] for desc in cursor.description]

    df = pd.DataFrame(cursor.fetchall(), columns=columns)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['farm_date'], y=df['temp'], name='温度'))
    fig.add_trace(go.Scatter(x=df['farm_date'], y=df['humi'], name='湿度'))
    fig.add_trace(go.Scatter(x=df['farm_date'], y=df['light'], name='光照'))
    fig.add_trace(go.Scatter(x=df['farm_date'], y=df['smoke'], name='空气质量'))
    fig.add_trace(go.Scatter(x=df['farm_date'], y=df['soil'], name='土壤湿度'))
    fig.add_trace(go.Scatter(x=df['farm_date'], y=df['carbon_dioxide'], name='二氧化碳浓度'))

    fig.update_layout(title='近期数据变换', xaxis_title='日期', yaxis_title='数值')

    chart = fig.to_html(full_html=False)

    return chart


def export_to_excel(startdate, enddate):
    db_tools = DBTools()
    db_tools.connect()
    filename = f'{startdate}-{enddate}.xlsx'
    if os.path.exists(filename) and os.path.isfile(filename):
        query = ("SELECT farm_date, temp, humi, light, smoke, soil, carbon_dioxide FROM data_farm "
                 "WHERE DATE(farm_date) BETWEEN %s AND %s")

        cursor = db_tools.execute_query(query, (startdate, enddate))
        columns = [desc[0] for desc in cursor.description]

        df = pd.DataFrame(cursor.fetchall(), columns=columns)

        # 导出到Excel文件
        df.to_excel(filename, index=False)
    return filename
