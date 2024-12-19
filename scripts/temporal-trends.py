from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col, count, trim, regexp_replace
from pyspark.sql.types import IntegerType

# Initialize Spark session
spark = SparkSession.builder.appName("CountryContributionTrends").getOrCreate()

# Load the dataset
file_path = "cleaned_titles.csv/file.csv"
netflix_df = spark.read.csv(file_path, header=True, inferSchema=True)

# Clean 'production_countries' column to remove [ ] and ' characters
cleaned_df = netflix_df.withColumn(
    "production_countries", regexp_replace(col("production_countries"), "[\\[\\]']", "")
)

# Ensure 'release_year' contains only valid numeric years
valid_years_df = cleaned_df.withColumn("release_year", col("release_year").cast(IntegerType())) \
                           .filter(col("release_year").isNotNull())

# Split 'production_countries' into individual countries and explode into rows
countries_exploded = valid_years_df.withColumn("Country", explode(split(col("production_countries"), ",")))

# Trim leading/trailing whitespace in country names
countries_cleaned = countries_exploded.withColumn("Country", trim(col("Country")))

# Group by release_year and Country, then count the number of titles
temporal_trends = countries_cleaned.groupBy("release_year", "Country").agg(
    count("*").alias("TotalTitles")
)

# Sort the results by release year and descending title count
temporal_trends_sorted = temporal_trends.orderBy(col("release_year").asc(), col("TotalTitles").desc())

# Save the results to a CSV file
output_path = "output_temporal_trends.csv"  # Replace with the desired output path
temporal_trends_sorted.write.csv(output_path, header=True, mode="overwrite")

print(f"Temporal trends saved to {output_path}")
