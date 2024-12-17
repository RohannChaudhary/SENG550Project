#PROMPT 4
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, count, split, lower, trim, array_distinct, size, regexp_replace

# Initialize Spark session
spark = SparkSession.builder.appName("NetflixCollaborations").getOrCreate()

# Load the dataset
df = spark.read.csv("cleaned-data.csv", header=True, inferSchema=True)

# =============================
# Step 1: Clean and Convert Stringified Lists to Arrays
# =============================
# Ensure production_countries is treated as an array
df_cleaned = df.withColumn(
    "production_countries",
    array_distinct(
        split(
            regexp_replace(trim(col("production_countries")), "[\\[\\]\\']", ""), ","
        )
    )
)

# =============================
# Step 2: Filter Titles with Multiple Countries
# =============================
# Filter for titles with at least 2 production countries
df_multi_country = df_cleaned.filter(size(col("production_countries")) > 1)

# =============================
# Step 3: Generate Country Pairs for Each Title
# =============================
# Explode the list column into individual rows
df_country_pairs = df_multi_country.select(
    col("title"),
    explode(col("production_countries")).alias("country_1")
).join(
    df_multi_country.select(
        col("title"),
        explode(col("production_countries")).alias("country_2")
    ),
    on="title"
).filter(col("country_1") < col("country_2"))  # Avoid self-pairs and duplicate pairs

# =============================
# Step 4: Aggregate Collaborations
# =============================
# Count the number of titles for each country pair
country_collaborations = df_country_pairs.groupBy("country_1", "country_2") \
                                        .agg(count("title").alias("collaboration_count")) \
                                        .orderBy(col("collaboration_count").desc())

# =============================
# Step 5: Calculate Percentage of Multi-Country Titles
# =============================
# Total number of titles
total_titles = df_cleaned.count()

# Total number of multi-country titles
multi_country_titles = df_multi_country.count()

# Calculate percentage of multi-country titles
percentage = (multi_country_titles / total_titles) * 100
print(f"Percentage of titles produced by multiple countries: {percentage:.2f}%")

# =============================
# Step 6: Show Results
# =============================
# Show top collaborating countries
print("Top Collaborating Countries:")
country_collaborations.show(10, truncate=False)

# =============================
# Step 7: Fix Output Before Saving
# =============================
# Clean country pairs before saving to CSV
country_collaborations_cleaned = country_collaborations.withColumn("country_1", trim(lower(col("country_1")))) \
                                                      .withColumn("country_2", trim(lower(col("country_2"))))

# Save the cleaned results to a CSV file
country_collaborations_cleaned.write.csv("top_collab_countries.csv", header=True, mode="overwrite")
