import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# =============================
# Step 1: Load and Clean the Dataset
# =============================

# Load the dataset, skip malformed rows
df = pd.read_csv("cleaned-data.csv", engine="python", on_bad_lines="skip")

# Keep only rows where 'description' and 'production_countries' are valid
df_cleaned = df[
    df['description'].apply(lambda x: isinstance(x, str) and len(x.strip()) > 0) &
    df['production_countries'].apply(lambda x: isinstance(x, str) and len(x.strip()) > 0)
]

# Parse the 'production_countries' column to ensure it's a list
df_cleaned['production_countries'] = df_cleaned['production_countries'].str.strip("[]").str.replace("'", "").str.split(", ")

# =============================
# Step 2: Generate Word Clouds for Selected Countries
# =============================

selected_countries = ['us', 'in', 'ca', 'jp', 'gb', 'fr']

# Dictionary to store word clouds for each country
wordclouds = {}

for country in selected_countries:
    # Filter rows for the current country
    country_data = df_cleaned[df_cleaned['production_countries'].apply(lambda x: country in x)]
    
    # Combine all descriptions for this country
    text = " ".join(country_data['description'].values)
    
    # Generate the word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="black",
        colormap="viridis",
        max_words=200,
        contour_width=3,
        contour_color="steelblue"
    ).generate(text)
    
    wordclouds[country] = wordcloud

# =============================
# Step 3: Visualize All Word Clouds
# =============================

fig, axes = plt.subplots(6, 1, figsize=(60, 40))
axes = axes.flatten()

for i, country in enumerate(selected_countries):
    ax = axes[i]
    ax.imshow(wordclouds[country], interpolation="bilinear")
    ax.axis("off")
    ax.set_title(f"Word Cloud for {country.upper()}", fontsize=14, weight="bold")

# Adjust layout for minimal spacing
plt.subplots_adjust(wspace=0.1, hspace=0.1)  # Reduced spacing between plots
plt.show()
