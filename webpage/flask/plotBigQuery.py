from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def plot_bigquery(start_time, end_time):
    # create BigQuery client object
    client = bigquery.Client()

    # define SQL query to retrieve the required data
    query = f"""
            SELECT string_field_0 AS location, 
                   int64_field_1 AS count_likes, 
                   int64_field_2 AS count_sentiment1,
                   int64_field_3 AS count_sentiment0,
                   int64_field_4 AS count_sentiment_1,
                   double_field_5 AS avg_sentiment,
                   timestamp_field_6 AS start_time,
                   timestamp_field_7 AS end_time
            FROM `NBAdataset.result`
            WHERE timestamp_field_6 >= TIMESTAMP("{start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC") AND timestamp_field_6 <= TIMESTAMP("{end_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
            """

    # execute the query and convert the result to a pandas DataFrame
    df = client.query(query).to_dataframe()

    path1 = plot_1(df)
    path2 = plot_2(df)
    path3 = plot_3(df)

    return path1, path2, path3


def plot_1(df):
    # 去除location为No location available.的记录
    df_1 = df[df['location'] != 'No location available.']

    # 统计每个location的count for likes的总和
    counts = df_1.groupby('location')['count_likes'].sum()

    # 绘制饼状图
    plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%')
    plt.title('Count for likes by location')
    plt.savefig("static/figure1.png")
    plt.close()

    return "static/figure1.png"

def plot_2(df):
    # 将时间戳转化为日期格式
    df['start_time'] = pd.to_datetime(df['start_time'], format='%Y-%m-%d %H:%M:%S')
    df['end_time'] = pd.to_datetime(df['end_time'], format='%Y-%m-%d %H:%M:%S')

    # 按照时间排序
    df = df.sort_values('start_time')

    # 绘制点状图
    plt.scatter(df['start_time'], df['avg_sentiment'])
    plt.title('Average sentiment over time')
    plt.xlabel('Time')
    plt.ylabel('Average sentiment')
    plt.savefig("static/figure2.png")
    plt.close()

    return "static/figure2.png"

def plot_3(df):
    # 去除location为No location available.的记录
    df_1 = df[df['location'] != 'No location available.']

    # 统计每个location的count for likes的总和
    counts = df_1.groupby('location')['count_likes'].sum()

    # 绘制饼状图
    plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%')
    plt.title('Count for likes by location')
    plt.savefig("static/figure3.png")
    plt.close()

    return "static/figure3.png"