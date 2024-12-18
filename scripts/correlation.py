from pyspark.sql import SparkSession
import pandas as pd
from pyspark.sql.functions import col, corr
import matplotlib as plt 
import seaborn as sns

# Initialize Spark session
spark = SparkSession.builder.appName("IMDbVotesAndPopularity").getOrCreate()

# Load the dataset
file_path = "../cleaned_titles.csv/file.csv"  # Replace with your actual file path
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Filter rows with valid IMDb votes and TMDB popularity
filtered_df = df.filter(
    col("imdb_votes").isNotNull() & col("tmdb_popularity").isNotNull()
)

# Calculate correlation between IMDb votes and TMDB popularity
correlation = filtered_df.select(corr("imdb_votes", "tmdb_popularity").alias("correlation")).collect()[0][0]

print(f"Correlation between IMDb votes and TMDB popularity: {correlation}")

# Save the cleaned data for visualization
output_path = "cleaned_votes_popularity.csv"  # Replace with your desired output path
filtered_df.select("imdb_votes", "tmdb_popularity").write.csv(output_path, header=True, mode="overwrite")

print(f"Cleaned data saved to '{output_path}' for further visualization.")
