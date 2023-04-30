from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import plotly.express as px

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
    plt.figure(figsize=(12, 8))
    plt.pie(counts.values, labels=counts.index, autopct='%1.1f%%')
    plt.title('Count for likes by location')
    plt.savefig("static/figure1.png")
    plt.close()

    return "static/figure1.png"

# def plot_2(df):
#     # Convert start_time to 30-minute intervals and calculate the average sentiment
#     hourly_sentiment = df.groupby(pd.Grouper(key='start_time', freq='30T'))['avg_sentiment'].mean()
#
#     # Create a scatter plot with a single point for every interval
#     plt.scatter(hourly_sentiment.index, hourly_sentiment)
#     plt.title('Average sentiment over time')
#     plt.xlabel('Time')
#     plt.ylabel('Average sentiment')
#     plt.savefig("static/figure2.png")
#     plt.close()
#
#     return "static/figure2.png"


def plot_2(df):
    # Convert start_time to hourly intervals and calculate the average sentiment
    hourly_sentiment = df.groupby(pd.Grouper(key='start_time', freq='15T'))['avg_sentiment'].mean()

    # Create a scatter plot with a single point for every hour
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.scatter(hourly_sentiment.index, hourly_sentiment)
    ax.set_title('Average sentiment over time')
    ax.set_xlabel('Time')
    ax.set_ylabel('Average sentiment')
    fig.savefig("static/figure2.png")
    plt.close()

    return "static/figure2.png"


def plot_3(df):
    # Filter out records where the location field is equal to 'No location available.'
    df_1 = df[df['location'] != 'No location available.']

    # Extract the state abbreviation from the location field (assuming the location field is in the format "City, State, Country")
    df_1['state'] = df_1['location'].apply(lambda x: x.split(', ')[-2])

    # Group the data by state and sum the count_likes field for each group
    counts = df_1.groupby('state')['count_likes'].sum().reset_index()

    # Sort the data by count_likes in descending order
    counts = counts.sort_values('count_likes', ascending=False)

    # Create a bar chart showing the count of likes for each state
    plt.figure(figsize=(12, 8))
    sns.barplot(x='state', y='count_likes', data=counts, color='b')
    plt.title('Total count of likes by state')
    plt.xlabel('State')
    plt.ylabel('Total count of likes')
    plt.savefig("static/figure3.png")
    plt.close()

    return "static/figure3.png"