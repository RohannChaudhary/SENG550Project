import pandas as pd

# Load the dataset, skipping malformed rows
df = pd.read_csv("cleaned-data.csv", engine="python", on_bad_lines="skip")

# Step 1: Drop rows with null or empty 'description' or 'genres'
df_cleaned = df[
    df['description'].notnull() & 
    df['genres'].notnull() & 
    df['description'].str.strip().astype(bool) & 
    df['genres'].str.strip().astype(bool)
]

# Step 2: Convert 'imdb_score' to numeric, coercing errors
df_cleaned['imdb_score'] = pd.to_numeric(df_cleaned['imdb_score'], errors='coerce')

# Step 3: Replace null values in 'imdb_score' with the column's mean
average_imdb_score = df_cleaned['imdb_score'].mean(skipna=True)
df_cleaned['imdb_score'] = df_cleaned['imdb_score'].fillna(average_imdb_score)

# Check the results
print(f"Dataset size after cleaning: {len(df_cleaned)}")
print(f"Average IMDb score used for null values: {average_imdb_score:.2f}")

# Save the cleaned dataset
df_cleaned.to_csv("cleaned_for_rec.csv", index=False)
