from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg

# Initialize Spark session
spark = SparkSession.builder.appName("RuntimeTrends").getOrCreate()

# Load the dataset
file_path = "cleaned_titles.csv/file.csv" 
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Filter for Movies only
movies_df = df.filter(col("type") == "movie")

# Calculate average runtime per release year
runtime_trends = movies_df.groupBy("release_year").agg(
    avg("runtime").alias("AverageRuntime")
).filter(col("release_year").isNotNull())

# Select only release_year and AverageRuntime
runtime_trends_selected = runtime_trends.select("release_year", "AverageRuntime")

# Save the runtime trends to a CSV file
output_path = "runtime_trends.csv"  # Replace with desired output path
runtime_trends_selected.orderBy("release_year").write.csv(output_path, header=True, mode="overwrite")

print(f"Average runtime trends saved to {output_path}")
