# Only considering the top 3 genres per country
from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct, col

# Initialize Spark session
spark = SparkSession.builder.appName("CommonGenresAcrossCountries").getOrCreate()

# Load the dataset
file_path = "../datasets/top_genres_by_country.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Group by Genre and count the number of unique countries
genre_country_count = df.groupBy("Genre").agg(
    countDistinct("Country").alias("CountryCount")
)

# Filter only genres that appear in more than 1 country
common_genres = genre_country_count.filter(col("CountryCount") > 1)

# Save the results to a CSV file
output_common = "common_genres.csv"
common_genres.write.csv(output_common, header=True, mode="overwrite")

print(f"Common genres saved to {output_common}")
