#PROMPT 5

from pyspark.sql import SparkSession
from pyspark.sql.functions import split, regexp_replace, trim, col, explode, lower, length, avg, when, isnan

# Initialize Spark session
spark = SparkSession.builder.appName("CountryRatingsAggregation").getOrCreate()

# Loading the dataset
df = spark.read.csv("cleaned-data.csv", header=True, inferSchema=True)

# =============================
# Step 1: Clean and Explode production_countries
# =============================
# Clean and split 'production_countries' into individual rows
df_cleaned = df.withColumn(
    "production_countries",
    explode(
        split(
            regexp_replace(trim(col("production_countries")), "[\\[\\]\\' ]", ""), ","
        )
    )
)

# Ensure country codes are lowercase and exactly two letters
df_valid_countries = df_cleaned.filter(
    (length(col("production_countries")) == 2) & (col("production_countries").rlike("^[a-z]{2}$"))
)

# =============================
# Step 2: Filter Non-Null Ratings
# =============================
# Ensure IMDb and TMDb scores are valid (non-null and not NaN)
df_ratings = df_valid_countries.withColumn(
    "imdb_score", when((~isnan(col("imdb_score"))) & (col("imdb_score").isNotNull()), col("imdb_score"))
).withColumn(
    "tmdb_score", when((~isnan(col("tmdb_score"))) & (col("tmdb_score").isNotNull()), col("tmdb_score"))
)

# =============================
# Step 3: Aggregate Ratings by Country
# =============================
# Calculate average IMDb, TMDb, and combined ratings per country
country_ratings = df_ratings.groupBy("production_countries").agg(
    avg(col("imdb_score")).alias("average_imdb_rating"),
    avg(col("tmdb_score")).alias("average_tmdb_rating")
).withColumn(
    "overall_average_rating",
    (col("average_imdb_rating") + col("average_tmdb_rating")) / 2
)

# Rename column for clarity
country_ratings = country_ratings.withColumnRenamed("production_countries", "country")

# =============================
# Step 4: Show and Save Results
# =============================
# Show final aggregated ratings
country_ratings.show(10, truncate=False)

# Save the results to a CSV file
country_ratings.write.csv("country_ratings_avg.csv", header=True, mode="overwrite")
