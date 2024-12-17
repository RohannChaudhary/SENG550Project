from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    explode, col, split, regexp_replace, trim, lower, array_distinct, size,
    least, greatest, count
)

# Initialize Spark session
spark = SparkSession.builder.appName("CountryPairCount").getOrCreate()

# Load the dataset
df = spark.read.csv("cleaned-data.csv", header=True, inferSchema=True)

# =============================
# Step 1: Clean and Convert Stringified Lists to Arrays
# =============================
# Clean and split stringified lists into proper arrays
df_cleaned = df.withColumn(
    "production_countries",
    array_distinct(
        split(
            regexp_replace(
                trim(lower(col("production_countries"))), "[\\[\\]\\' ]+", ""  # Remove unwanted characters
            ),
            ","
        )
    )
)

# =============================
# Step 2: Filter for Titles with Multiple Countries
# =============================
# Filter titles with at least 2 countries in production_countries
df_multi_country = df_cleaned.filter(size(col("production_countries")) > 1)

# =============================
# Step 3: Generate All Unique Country Pairs for Each Title
# =============================
# Explode the array to generate all combinations of country pairs
df_country_pairs = df_multi_country.select(
    col("title"),
    explode(col("production_countries")).alias("country_1")
).join(
    df_multi_country.select(
        col("title"),
        explode(col("production_countries")).alias("country_2")
    ),
    on="title"
)

# Sort country pairs alphabetically and filter out self-pairs
df_country_pairs = df_country_pairs.withColumn(
    "country_1", least(col("country_1"), col("country_2"))
).withColumn(
    "country_2", greatest(col("country_1"), col("country_2"))
).filter(col("country_1") != col("country_2"))  # Remove self-pairs like 'us, us'

# Remove duplicates within each title to avoid redundant pairs
df_country_pairs = df_country_pairs.dropDuplicates(["title", "country_1", "country_2"])

# =============================
# Step 4: Aggregate the Number of Titles for Each Country Pair
# =============================
# Group by country pairs and count the number of titles
country_pair_counts = df_country_pairs.groupBy("country_1", "country_2") \
                                      .agg(count("title").alias("shared_titles_count")) \
                                      .orderBy(col("shared_titles_count").desc())

# =============================
# Step 5: Show and Save Results
# =============================
# Show top country pairs with their shared titles count
print("Top Country Pairs and Their Shared Titles Count:")
country_pair_counts.show(10, truncate=False)

# Save the results to a CSV file
country_pair_counts.write.csv("top_collab_countries.csv", header=True, mode="overwrite")
