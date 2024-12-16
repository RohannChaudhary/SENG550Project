from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum, when, trim, lower, count, row_number, size, udf
from pyspark.sql.window import Window
from pyspark.sql.types import ArrayType, StringType
from datetime import datetime
import ast

# =============================
# Step 1: Initialize Spark Session
# =============================
spark = SparkSession.builder.appName("NetflixAnalysis").getOrCreate()

# =============================
# Step 2: Load the Dataset
# =============================
df = spark.read.csv(
    "titles.csv",
    header=True,
    inferSchema=True,
    multiLine=True,         # Enables parsing of multi-line fields
    escape='"',             # Handles fields with embedded quotes
    quote='"',              # Specifies the quoting character
    sep=",",                # Use 'sep' instead of 'delimiter'
    mode="PERMISSIVE"       # Flags malformed rows without dropping them
)

# Initial row count
print(f"Initial row count: {df.count()}")

# =============================
# Step 3: Drop Rows with Null Critical Columns
# =============================
df_cleaned = df.filter((df["title"].isNotNull()) & (df["type"].isNotNull()))
df_cleaned = df_cleaned.filter(
    (df_cleaned["genres"].isNotNull()) & (df_cleaned["production_countries"].isNotNull())
)
print(f"Row count after dropping nulls: {df_cleaned.count()}")

# =============================
# Step 4: Ensure Consistent Casing and Whitespace
# =============================
df_cleaned = df_cleaned.withColumn("type", trim(lower(col("type")))) \
                       .withColumn("genres", trim(lower(col("genres")))) \
                       .withColumn("production_countries", trim(lower(col("production_countries"))))


# =============================
# Step 5: Check for Outliers
# =============================
# Describe numerical columns
df_cleaned.select("runtime").describe().show()
df_cleaned.select("imdb_score", "tmdb_score").describe().show()

# Identify specific outliers
current_year = datetime.now().year
df_cleaned.filter((col("runtime") < 1) | (col("runtime") > 300)).select("title", "runtime").show()
df_cleaned.filter((col("imdb_score") < 0) | (col("imdb_score") > 10)).select("title", "imdb_score").show()
df_cleaned.filter(col("release_year") > current_year).select("title", "release_year").show()

# =============================
# Step 6: Handle Runtime = 0
# =============================
df_cleaned = df_cleaned.withColumn(
    "runtime",
    when(col("runtime") == 0, None).otherwise(col("runtime"))
)
print(f"Number of titles with null runtime: {df_cleaned.filter(col('runtime').isNull()).count()}")

# =============================
# Step 7: Validate Categorical Columns
# =============================
# Ensure only 'movie' or 'show' in `type`
df_cleaned = df_cleaned.filter((col("type") == "movie") | (col("type") == "show"))
df_cleaned.select("type").distinct().show()

# Validate `age_certification`
valid_age_certifications = ["G", "PG", "PG-13", "R", "NC-17", "TV-Y", "TV-Y7", "TV-G", "TV-PG", "TV-14", "TV-MA"]
df_cleaned = df_cleaned.withColumn(
    "age_certification",
    when(col("age_certification").isin(valid_age_certifications), col("age_certification"))
    .otherwise(None)
)
df_cleaned.select("age_certification").distinct().show()

# =============================
# Step 8: Handle Duplicates
# =============================
# Use a window function to retain only the row with the highest runtime for duplicate titles
window_spec = Window.partitionBy("title").orderBy(col("runtime").desc())
df_cleaned = df_cleaned.withColumn("rank", row_number().over(window_spec))
df_cleaned = df_cleaned.filter(col("rank") == 1).drop("rank")


# Replace non-numerical values in `imdb_score`, `imdb_votes`, `tmdb_score`, and `tmdb_popularity` with null
numerical_columns = ["imdb_score", "imdb_votes", "tmdb_score", "tmdb_popularity"]

for column in numerical_columns:
    df_cleaned = df_cleaned.withColumn(
        column,
        when(col(column).rlike("^[0-9]+(\\.[0-9]+)?$"), col(column))  # Retain valid numerical values
        .otherwise(None)  # Replace non-numerical values with null
    )

# Verify no duplicates remain
duplicates = df_cleaned.groupBy("title").agg(count("title").alias("count")).filter(col("count") > 1)
print(f"Total duplicate titles after removal: {duplicates.count()}")

# =============================
# Step 9: Export Cleaned Data
# =============================
df_cleaned.write.csv("cleaned_titles.csv", header=True, mode="overwrite")
print(f"Cleaned data exported successfully.")
