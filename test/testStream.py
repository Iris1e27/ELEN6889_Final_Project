from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType, BooleanType
from pyspark.sql.functions import col, lit, sum, window, udf, when, avg
import time

# define the input and output paths of your bucket
input_path = "gs://6889nba/nba/"
output_path = "gs://6889nba/output/"

# create SparkSession
spark = SparkSession.builder.appName("myApp").getOrCreate()

# define the schema for the DataFrame
schema = StructType([
    StructField("team", StringType(), True),
    StructField("timestamp", TimestampType(), True),
    StructField("text", StringType(), True),
    StructField("location", StringType(), True),
    StructField("likes", IntegerType(), True),
    StructField("sentiment", IntegerType(), True)
])


# read in the CSV file as a DataFrame
df = (
    spark.read
    .format("csv")
    .option("header", "false")
    .schema(schema)
    .load(input_path)
)

# define a user-defined function to check if a string is in English
def is_english(text):
    if text is None:
        return False
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

# register the UDF
is_english_udf = udf(is_english, BooleanType())
# filter out non-English text
df_filtered = df.filter(is_english_udf(df["text"]))

df_filtered = df.filter(col("location").isNotNull() & col("likes").isNotNull() & col("sentiment").isNotNull())

# group the remaining tweets by location and a 1-hour window with a sliding duration of 30 minutes
likes_by_location_windowed = (
    df_filtered
    .groupBy(
        window(col("timestamp"), "1 hour", "30 minutes"),
        col("location")
    )
    .agg(
        sum("likes").alias("total_likes"),
        sum(when(col("sentiment") == 1, 1).otherwise(0)).alias("count_sentiment_1"),
        sum(when(col("sentiment") == 0, 1).otherwise(0)).alias("count_sentiment_0"),
        sum(when(col("sentiment") == -1, 1).otherwise(0)).alias("count_sentiment_-1"),
        avg(col("sentiment")).alias("average_sentiment")
    )
    .withColumn("window_start", col("window.start"))
    .withColumn("window_end", col("window.end"))
    .drop("window")
    .orderBy("window_start")
)

# write the aggregated data to a CSV file on your bucket
likes_by_location_windowed.write.mode("overwrite").csv(output_path)

