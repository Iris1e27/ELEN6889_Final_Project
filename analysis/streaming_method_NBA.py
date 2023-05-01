# for streaming method
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType, BooleanType
from pyspark.sql.functions import *

def is_english(text):
    if text is None:
        return False
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True
# Define a UDF for the is_english() function
is_english_udf = udf(lambda text: is_english(text), BooleanType())

myschema = StructType([
    StructField("team", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("text", StringType(), True),
    StructField("location", StringType(), True),
    StructField("likes", IntegerType(), True),
    StructField("sentiment", IntegerType(), True)
])

spark = SparkSession.builder \
    .appName("Tweet Analysis") \
    .getOrCreate()

# Read streaming data
streaming_data = (
    spark.readStream.csv("gs://dataproc-staging-us-central1-300388429198-ocbfs3ky/inputdata/*.csv",
                         header=False, schema=myschema)
)

# # Filter and add watermark
# filtered_data = (
#     streaming_data.filter("isnotnull(location) AND isnotnull(likes) AND isnotnull(sentiment)")
#     .filter(is_english_udf(col("text")))
#     .withWatermark("timestamp", "1 hour")
# )

# Filter out -1 values in the "likes" column and replace with 0 and null values in some columns
# Apply operator fusion: Merge filter operations into one
filtered_data = (
    streaming_data.filter(
        "isnotnull(location) AND isnotnull(likes) AND isnotnull(sentiment)")
    .withColumn("likes", when(col("likes") == -1, 0).otherwise(col("likes")))
    .filter(is_english_udf(col("text")))
    .withWatermark("timestamp", "1 hour")
)


# Aggregate data
aggregated_data = (
    filtered_data.groupBy(
        window("timestamp", "30 minutes", "30 minutes"),
        "location"
    )
    .agg(
        sum("likes").alias("total_likes"),
        sum(when(col("sentiment") == 1, 1).otherwise(0)).alias("count_sentiment_1"),
        sum(when(col("sentiment") == 0, 1).otherwise(0)).alias("count_sentiment_0"),
        sum(when(col("sentiment") == -1, 1).otherwise(0)).alias("count_sentiment_-1"),
        avg("sentiment").alias("average_sentiment")
    )
    .select(
        "location",
        "total_likes",
        "count_sentiment_1",
        "count_sentiment_0",
        "count_sentiment_-1",
        "average_sentiment",
        col("window").getField("start").alias("window_start"),
        col("window").getField("end").alias("window_end")
    )
)

# Write aggregated data to temporary folder
query = (
    aggregated_data.writeStream
    .outputMode("append")
    .format("parquet")
    .option("path", "gs://dataproc-staging-us-central1-300388429198-ocbfs3ky/outputdata/")
    .option("checkpointLocation", "gs://dataproc-staging-us-central1-300388429198-ocbfs3ky/checkpoint/")
    .start()
)


query.awaitTermination()

# Read the output from the temporary folder
output_data = spark.read.parquet("gs://dataproc-staging-us-central1-300388429198-ocbfs3ky/outputdata/")

# Sort the output data and write the final result
sorted_output = output_data.sort(asc("window_start"))

sorted_output.write.csv("gs://dataproc-staging-us-central1-300388429198-ocbfs3ky/outputdata/", mode="overwrite")