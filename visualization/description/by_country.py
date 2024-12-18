import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# =============================
# Step 1: Load and Clean the Dataset
# =============================

# Load the dataset, skip malformed rows
df = pd.read_csv("cleaned-data.csv", engine="python", on_bad_lines="skip")

# Keep only rows where 'description' is a valid string and not empty
df_cleaned = df[df['description'].apply(lambda x: isinstance(x, str) and len(x.strip()) > 0)]

# Filter by specific countries
selected_countries = ['us', 'in', 'ca', 'jp', 'gb', 'fr']
country_wordclouds = {}

# Generate text for each country
for country in selected_countries:
    country_data = df_cleaned[df_cleaned['production_countries'].str.contains(country, na=False, case=False)]
    text = " ".join(country_data['description'].values)
    country_wordclouds[country] = text

# =============================
# Step 2: Generate and Save Word Clouds
# =============================

for country, text in country_wordclouds.items():
    # Create a WordCloud object
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color="black",
        colormap="viridis",
        max_words=200,
        contour_width=3,
        contour_color="steelblue"
    ).generate(text)

    # Save each word cloud as an individual image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"Word Cloud for {country.upper()}", fontsize=16, color="white", weight="bold")
    plt.tight_layout(pad=0)
    plt.savefig(f"wordcloud_{country}.png", dpi=300)
    plt.close()

print("Word clouds saved as individual images.")
