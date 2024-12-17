from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count
from pyspark.sql.types import IntegerType

# Initialize Spark session
spark = SparkSession.builder.appName("AgeCertificationTrends").getOrCreate()

# Load the dataset
file_path = "cleaned_titles.csv/file.csv"  # Correct path to your dataset
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Filter for valid release_year (convertible to integer) and non-null age certification
valid_df = df.withColumn("release_year", col("release_year").cast(IntegerType())) \
             .filter(col("release_year").isNotNull() & col("age_certification").isNotNull())

# Group by release year, type (Movie or TV Show), and age certification, then count the titles
age_cert_trends = valid_df.groupBy("release_year", "type", "age_certification").agg(
    count("*").alias("TitleCount")
)

# Select relevant columns and order the results
age_cert_trends_selected = age_cert_trends.select(
    "release_year", "type", "age_certification", "TitleCount"
).orderBy("release_year", col("TitleCount").desc())

# Save the results to a CSV file
output_path = "age_certification_trends.csv"  # Replace with desired output path
age_cert_trends_selected.write.csv(output_path, header=True, mode="overwrite")

print(f"Age certification trends (Movies and Shows with valid years) saved to {output_path}")
