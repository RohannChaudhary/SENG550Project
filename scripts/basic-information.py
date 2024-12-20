from pyspark.sql import SparkSession
from pyspark.sql.functions import countDistinct, col, split, explode, trim, regexp_replace, count

# Initialize Spark session
spark = SparkSession.builder.appName("DatasetBasicInfo").getOrCreate()

# Loading the dataset
file_path = "../cleaned_titles.csv/file.csv" 
df = spark.read.csv(file_path, header=True, inferSchema=True)

cleaned_df = df.withColumn(
    "Country", explode(split(regexp_replace(col("production_countries"), "[\\[\\]'']", ""), ","))
).withColumn(
    "Genre", explode(split(regexp_replace(col("genres"), "[\\[\\]'']", ""), ","))
)

# Trim whitespace in 'Country' and 'Genre'
cleaned_df = cleaned_df.withColumn("Country", trim(col("Country"))).withColumn("Genre", trim(col("Genre")))

# Filter out NULL or empty values
cleaned_df = cleaned_df.filter((col("Country") != "") & (col("Country").isNotNull()) & (col("Country") != "romance"))
cleaned_df = cleaned_df.filter((col("Genre") != "") & (col("Genre").isNotNull()))

# Count total titles
total_titles_count = cleaned_df.count()

# Count the number of movies and shows
type_counts = cleaned_df.groupBy("type").agg(count("*").alias("TitleCount"))

# Calculate the percentage of each type
type_counts_with_percentage = type_counts.withColumn(
    "Percentage", (col("TitleCount") / total_titles_count) * 100
)

# Save type percentages to CSV
type_counts_with_percentage.write.csv("type_percentages.csv", header=True, mode="overwrite")

# Total number of unique genres
unique_genres_count = cleaned_df.select(countDistinct("Genre").alias("TotalUniqueGenres"))
unique_genres_count.write.csv("total_unique_genres.csv", header=True, mode="overwrite")

# Total number of unique countries
unique_countries_count = cleaned_df.select(countDistinct("Country").alias("TotalUniqueCountries"))
unique_countries_count.write.csv("total_unique_countries.csv", header=True, mode="overwrite")

# List of unique genres
unique_genres = cleaned_df.select("Genre").distinct()
unique_genres.write.csv("unique_genres.csv", header=True, mode="overwrite")

# List of unique countries
unique_countries = cleaned_df.select("Country").distinct()
unique_countries.write.csv("unique_countries.csv", header=True, mode="overwrite")

print("Basic dataset information has been saved successfully.")