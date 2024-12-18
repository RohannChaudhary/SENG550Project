from pyspark.sql import SparkSession
from pyspark.sql.functions import split, regexp_replace, trim, col, explode, lower, avg, when, isnan

# Initialize Spark session
spark = SparkSession.builder.appName("GenreRatingsAggregation").getOrCreate()

# Load the dataset
df = spark.read.csv("cleaned-data.csv", header=True, inferSchema=True)

# =============================
# Step 1: Clean and Explode genres
# =============================
# Clean and split 'genres' into individual rows
df_cleaned = df.withColumn(
    "genres",
    explode(
        split(
            regexp_replace(trim(lower(col("genres"))), "[\\[\\]\\' ]", ""), ","
        )
    )
)

# Ensure genre names are valid (non-empty after cleaning)
df_valid_genres = df_cleaned.filter(col("genres").rlike("^[a-z]+$"))

# =============================
# Step 2: Filter Non-Null Ratings
# =============================
# Ensure IMDb and TMDb scores are valid (non-null and not NaN)
df_ratings = df_valid_genres.withColumn(
    "imdb_score", when((~isnan(col("imdb_score"))) & (col("imdb_score").isNotNull()), col("imdb_score"))
).withColumn(
    "tmdb_score", when((~isnan(col("tmdb_score"))) & (col("tmdb_score").isNotNull()), col("tmdb_score"))
)

# =============================
# Step 3: Aggregate Ratings by Genre
# =============================
# Calculate average IMDb, TMDb, and combined ratings per genre
genre_ratings = df_ratings.groupBy("genres").agg(
    avg(col("imdb_score")).alias("average_imdb_rating"),
    avg(col("tmdb_score")).alias("average_tmdb_rating")
).withColumn(
    "overall_average_rating",
    (col("average_imdb_rating") + col("average_tmdb_rating")) / 2
)

# Rename column for clarity
genre_ratings = genre_ratings.withColumnRenamed("genres", "genre")

# =============================
# Step 4: Show and Save Results
# =============================
# Show final aggregated ratings
genre_ratings.show(10, truncate=False)

# Save the results to a CSV file
genre_ratings.write.csv("genre_ratings_avg.csv", header=True, mode="overwrite")
