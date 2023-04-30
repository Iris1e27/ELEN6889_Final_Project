from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_bigquery(start_time, end_time):
    # create BigQuery client object
    client = bigquery.Client()

    # define SQL query to retrieve the required data
    query = f"""
    SELECT string_field_0, int64_field_1, int64_field_2, int64_field_3, int64_field_4, double_field_5, timestamp_field_6, timestamp_field_7
    FROM `NBAdataset.result`
    WHERE timestamp_field_6 >= TIMESTAMP("{start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC") AND timestamp_field_6 <= TIMESTAMP("{end_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    """

    # execute the query and convert the result to a pandas DataFrame
    df = client.query(query).to_dataframe()

    # generate pie chart
    pie_df = df.groupby(["string_field_0"])["int64_field_1"].sum()
    pie_df.plot(kind="pie", autopct='%1.1f%%', startangle=90)
    plt.title("Distribution of int64_field_1 by string_field_0")
    plt.savefig("static/pie.png")
    plt.close()

    # return path of saved image
    return os.path.join("static", "pie.png")
