from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    explode, col, split, lower, trim, regexp_replace, count, sum, array_distinct
)

# Initialize Spark session
spark = SparkSession.builder.appName("GenreDistribution").getOrCreate()

# Load the dataset
df = spark.read.csv("cleaned-data.csv", header=True, inferSchema=True)

# =============================
# Step 1: Clean and Parse 'genres' and 'production_countries'
# =============================
# Clean the 'genres' column: remove brackets, quotes, and split into an array
df_cleaned = df.withColumn(
    "genres",
    array_distinct(
        split(
            regexp_replace(trim(lower(col("genres"))), "[\\[\\]\\']", ""), ","
        )
    )
).withColumn(
    "production_countries",
    array_distinct(
        split(
            regexp_replace(trim(lower(col("production_countries"))), "[\\[\\]\\']", ""), ","
        )
    )
)

# =============================
# Step 2: Explode 'genres' and 'production_countries'
# =============================
# Explode both 'genres' and 'production_countries' into individual rows
df_exploded = df_cleaned.withColumn(
    "genre", explode(col("genres"))
).withColumn(
    "country", explode(col("production_countries"))
)

# =============================
# Step 3: Aggregate Genre Counts Per Country
# =============================
# Group by 'country' and 'genre', and count the number of titles
genre_distribution = df_exploded.groupBy("country", "genre") \
                                .agg(count("*").alias("genre_count"))

# =============================
# Step 4: Calculate Total Titles Per Country
# =============================
# Calculate the total number of titles for each country
country_totals = genre_distribution.groupBy("country") \
                                   .agg(sum("genre_count").alias("total_count"))

# Join the total count back to the genre-level counts
genre_distribution = genre_distribution.join(
    country_totals, on="country", how="inner"
)

# =============================
# Step 5: Calculate Genre Proportions
# =============================
# Add a column for the proportion of each genre
genre_distribution = genre_distribution.withColumn(
    "genre_percentage", (col("genre_count") / col("total_count")) * 100
)

# =============================
# Step 6: Save Aggregated Dataset
# =============================
# Save the aggregated dataset to a CSV file
genre_distribution.select("country", "genre", "genre_count", "genre_percentage") \
                  .orderBy("country", "genre_percentage", ascending=[True, False]) \
                  .write.csv("genre_distribution_by_country.csv", header=True, mode="overwrite")


