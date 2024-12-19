from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, count, sum as _sum, round, regexp_replace, trim

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("Country Contribution Analysis") \
    .getOrCreate()

# Load the dataset with robust options to handle malformed rows
data_path = "../cleaned_titles.csv/file.csv" 
df = spark.read.csv(
    data_path, 
    header=True, 
    inferSchema=True, 
    mode="DROPMALFORMED"  # Drop malformed rows
)

df_cleaned = df.select("production_countries").withColumn(
    "production_countries", 
    regexp_replace(col("production_countries"), r"[\'\[\]]", "")  # Remove square brackets and single quotes
)

# Filter out rows where 'production_countries' is empty (originally "[]")
df_filtered = df_cleaned.filter(trim(col("production_countries")) != "")

# Split and explode the 'production_countries' column to handle multiple countries
countries_df = df_filtered.select(
    explode(split(col("production_countries"), r",\s*")).alias("country")  
)

# Group by country and count titles
country_counts = countries_df.groupBy("country").agg(count("*").alias("title_count"))

# Filter out countries with names longer than 2 letters
valid_country_counts = country_counts.filter(col("country").rlike("^[a-zA-Z]{2}$"))

# Calculate total titles
total_titles = valid_country_counts.agg(_sum("title_count").alias("total_titles")).collect()[0]["total_titles"]

# Calculate percentage contribution for each country
country_percentage = valid_country_counts.withColumn(
    "percentage_share",
    round((col("title_count") / total_titles) * 100, 2)
)

# Top 10 countries with the largest share of content
top_10_countries = country_percentage.orderBy(col("percentage_share").desc()).limit(10)

# Write results to CSV files
output_path = "output_country"
country_percentage.write.csv(f"{output_path}/country_percentage.csv", header=True, mode="overwrite")
top_10_countries.write.csv(f"{output_path}/top_10_countries.csv", header=True, mode="overwrite")

print(f"Analysis complete. Results saved in the '{output_path}' directory.")
