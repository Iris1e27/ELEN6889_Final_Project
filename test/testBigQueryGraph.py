# from google.cloud import bigquery
# import pandas as pd
# import matplotlib.pyplot as plt
#
# # set up BigQuery client
# client = bigquery.Client()
#
# # define query to filter rows with timestamp_field_6=2023-04-15 01:00:00 UTC
# query = """
# SELECT *
# FROM NBAdataset.result
# WHERE timestamp_field_6 = '2023-04-15 01:00:00 UTC'
# """
#
# # run the query and load the results into a Pandas DataFrame
# df = client.query(query).to_dataframe()
#
# # Pie chart showing count of int64_field_1 for each string_field_0
# pie_data = df.groupby('string_field_0').agg({'int64_field_1': 'count'}).reset_index()
# pie_data.plot(kind='pie', y='int64_field_1', labels=pie_data['string_field_0'], legend=None)
# plt.title('Count of int64_field_1 for each string_field_0')
# plt.show()
#
# # Bar chart showing int64_field_2, int64_field_3, and int64_field_4 for each string_field_0
# bar_data = df.groupby('string_field_0').agg({'int64_field_2': 'sum', 'int64_field_3': 'sum', 'int64_field_4': 'sum'}).reset_index()
# bar_data.plot(kind='bar', x='string_field_0', stacked=True)
# plt.title('Total int64_field_2, int64_field_3, and int64_field_4 for each string_field_0')
# plt.show()
#
# # Line chart showing trend of double_field_5 over time
# line_data = df[['timestamp_field_6', 'double_field_5']]
# line_data.plot(x='timestamp_field_6', y='double_field_5')
# plt.title('Trend of double_field_5 over time')
# plt.show()
#

from google.cloud import bigquery
import pandas as pd
import matplotlib.pyplot as plt

# define the timestamp range
start_time = "2023-04-13 00:00:00 UTC"
end_time = "2023-04-21 23:59:59 UTC"

# create BigQuery client object
client = bigquery.Client()

# define SQL query to retrieve the required data
query = f"""
SELECT string_field_0, int64_field_1, int64_field_2, int64_field_3, int64_field_4, double_field_5, timestamp_field_6, timestamp_field_7
FROM `NBAdataset.result`
WHERE timestamp_field_6 >= TIMESTAMP("{start_time}") AND timestamp_field_6 <= TIMESTAMP("{end_time}")
"""

# execute the query and convert the result to a pandas DataFrame
df = client.query(query).to_dataframe()

# # Pie chart for int64_field_1 distribution by string_field_0
# pie_df = df.groupby(["string_field_0"])["int64_field_1"].sum()
# pie_df.plot(kind="pie", autopct='%1.1f%%', startangle=90)
# plt.title("Distribution of int64_field_1 by string_field_0")
# plt.show()
# # plt.savefig("result/pie.png")
#
# # Bar chart for int64_field_2, int64_field_3, and int64_field_4 by string_field_0
# bar_df = df.groupby(["string_field_0"]).sum()[["int64_field_2", "int64_field_3", "int64_field_4"]]
# bar_df.plot(kind="bar")
# plt.title("Aggregated int64_field_2, int64_field_3, and int64_field_4 by string_field_0")
# plt.show()
# plt.savefig("result/bar.png")

# Line chart for double_field_5 over time
line_df = df[["double_field_5", "timestamp_field_6"]]
line_df = line_df.sort_values(by="timestamp_field_6")
line_df.plot(x="timestamp_field_6", y="double_field_5")
plt.xlim(start_time, end_time)
plt.title("Trend of double_field_5 over time")
plt.show()
# plt.savefig("result/line.png")
