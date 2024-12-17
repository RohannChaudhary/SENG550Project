from pyspark.sql import SparkSession
from pyspark.sql.functions import split, explode, col, count, trim, row_number, regexp_replace
from pyspark.sql.window import Window

# Initialize Spark session
spark = SparkSession.builder.appName("TopGenresByCountry").getOrCreate()

# Load the dataset into a Spark DataFrame
file_path = 'cleaned_titles.csv/file.csv'
netflix_df = spark.read.csv(file_path, header=True, inferSchema=True)

# Clean 'production_countries' and 'genres' by removing [] and single quotes
cleaned_df = netflix_df.withColumn(
    "production_countries", regexp_replace(col("production_countries"), "[\\[\\]'']", "")
).withColumn(
    "genres", regexp_replace(col("genres"), "[\\[\\]'']", "")
)

# Explode production_countries into individual rows
countries_exploded = cleaned_df.withColumn("Country", explode(split(col("production_countries"), ",")))

# Trim whitespace in country names
countries_cleaned = countries_exploded.withColumn("Country", trim(col("Country")))

# Explode genres into individual rows
genres_exploded = countries_cleaned.withColumn("Genre", explode(split(col("genres"), ",")))

# Trim whitespace in genres
genres_cleaned = genres_exploded.withColumn("Genre", trim(col("Genre")))

# Group by Country and Genre, then count occurrences
genre_distribution = genres_cleaned.groupBy("Country", "Genre").agg(
    count("*").alias("TotalCount")
)

# Create a window to rank genres within each country
window_spec = Window.partitionBy("Country").orderBy(col("TotalCount").desc())

# Add a rank column to identify the top genres
ranked_genres = genre_distribution.withColumn("Rank", row_number().over(window_spec))

# Filter to get only the top genres for each country (e.g., top 3 genres)
top_genres_per_country = ranked_genres.filter(col("Rank") <= 3)

# Save the results to a CSV file
output_path = 'top_genres_by_country.csv'  # Replace with the desired output file path
top_genres_per_country.write.csv(output_path, header=True, mode="overwrite")

print(f"Top genres per country saved to {output_path}")