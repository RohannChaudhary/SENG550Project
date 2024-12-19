import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("rec_system/cleaned_for_rec.csv")

# =============================
# Step 2: Prepare Features for the Recommendation System
# =============================

# Function to clean text data
def clean_text(x):
    if isinstance(x, str):
        return x.lower().replace(" ", "")
    return ""

# Clean and prepare text for 'description', 'genres', and 'production_countries'
df['description'] = df['description'].apply(clean_text)
df['genres'] = df['genres'].apply(clean_text)
df['production_countries'] = df['production_countries'].apply(clean_text)

# Convert IMDb score into categories
df['imdb_category'] = pd.cut(df['imdb_score'], bins=[0, 4, 6, 8, 10], 
                             labels=['low', 'average', 'good', 'excellent'], 
                             include_lowest=True)

# Create a soup column by concatenating all the cleaned features
df['soup'] = (
    df['description'] + " " +
    df['genres'] + " " +
    (df['production_countries'] + " ") * 3 +  # Repeat 'production_countries' 3 times
    df['imdb_category'].astype(str)
)


# Save the prepared dataset for future use
df.to_csv("prepared_dataset.csv", index=False)

print("Feature preparation complete! The 'soup' column has been created.")
