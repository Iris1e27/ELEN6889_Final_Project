from google.cloud import bigquery

# 设置Google Cloud项目和BigQuery目标数据集和表
project_id = "big-data-6893-362802"
dataset_id = "NBAdataset"
table_id = "big-data-6893-362802.NBAdataset.nba"

# 创建BigQuery客户端
client = bigquery.Client(project=project_id)

# 定义BigQuery表的模式
schema = [
    bigquery.SchemaField("team", "STRING"),
    bigquery.SchemaField("timestamp", "TIMESTAMP"),
    bigquery.SchemaField("text", "STRING"),
    bigquery.SchemaField("location", "STRING"),
    bigquery.SchemaField("likes", "INTEGER"),
    bigquery.SchemaField("sentiment", "INTEGER")
]

# 定义数据导入配置
job_config = bigquery.LoadJobConfig(
    schema=schema,
    skip_leading_rows=1,
    source_format=bigquery.SourceFormat.CSV,
    field_delimiter=",",
    quote_character='"',
    allow_quoted_newlines=True,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
)

# 从CSV文件导入数据到BigQuery表
with open("E:\\ColumbiaUniversity\\ELEN6889\\Project\\dataset\\mergedAllWithHeader.csv", "rb") as source_file:
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)

job.result()  # 等待作业完成

print(f"Loaded {job.output_rows} rows into {project_id}.{dataset_id}.{table_id}")
