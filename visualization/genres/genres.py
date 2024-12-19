import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
df = pd.read_csv("../../datasets/all_genres_by_country.csv") 

# =============================
# Step 1: Clean the Dataset
# =============================

# Remove rows with empty country values
df = df[df['country'].notnull() & (df['country'] != "")]

# Group by country and genre, aggregate counts and percentages
df_grouped = df.groupby(['country', 'genre'], as_index=False).agg({
    'genre_count': 'sum',
    'genre_percentage': 'sum'
})

# =============================
# Step 2: Filter for Relevant Countries
# =============================

selected_countries = ['us', 'in', 'gb', 'jp', 'fr', 'ca']
df_filtered = df_grouped[df_grouped['country'].isin(selected_countries)]

# =============================
# Step 3: Remove Genres with Less Than 13%
# =============================

# Calculate total percentage for each genre across all countries
total_genre_percentage = df_filtered.groupby('genre')['genre_percentage'].sum()

# Keep only genres with total percentage >= 13%
valid_genres = total_genre_percentage[total_genre_percentage >= 13].index

# Filter the dataset to include only valid genres
df_filtered = df_filtered[df_filtered['genre'].isin(valid_genres)]

# Pivot the dataset for visualization
pivot_df = df_filtered.pivot(index='country', columns='genre', values='genre_percentage').fillna(0)

# Sort by total genre percentage across all genres (optional)
pivot_df["total"] = pivot_df.sum(axis=1)
pivot_df = pivot_df.sort_values(by="total", ascending=False).drop(columns=["total"])

# =============================
# Step 4: Define Extended Aesthetic Color Palette
# =============================

aesthetic_colors = [
   "#E63946",  # Vibrant Red
    "#F4A261",  # Burnt Orange
    "#2A9D8F",  # Teal
    "#264653",  # Deep Blue-Black
    "#E9C46A",  # Golden Yellow
    "#A8DADC",  # Light Teal
    "#1D3557",  # Navy Blue
    "#457B9D",  # Ocean Blue
    "#F77F00",  # Bright Orange
    "#6A0572",  # Purple
    "#D00000",  # Scarlet
    "#4361EE",  # Royal Blue
    "#480CA8",  # Deep Violet
    "#FF006E",  # Magenta
    "#06D6A0",  # Bright Green
    "#8338EC",  # Electric Purple
    "#F72585",  # Hot Pink
]

# Adjust the palette to match the number of genres
colors = aesthetic_colors[:len(pivot_df.columns)]

# =============================
# Step 5: Create the Stacked Bar Chart
# =============================

fig, ax = plt.subplots(figsize=(12, 8))

# Plot the stacked bar chart
pivot_df.plot(
    kind="bar",
    stacked=True,
    color=colors,
    ax=ax,
    edgecolor="none",
    width=0.8,
    alpha=0.9,
)

# Add labels and title
ax.set_title("Genre Distribution by Top Producing Countries on Netflix", fontsize=16, fontweight="bold", color="#E50914")
ax.set_ylabel("Percentage of Titles (%)", fontsize=12)
ax.set_xlabel("Country", fontsize=12)
ax.legend(
    title="Genres", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=10, title_fontsize=12
)
ax.set_xticks(np.arange(len(pivot_df.index)))
ax.set_xticklabels(pivot_df.index, rotation=45, ha="right")

# Customize grid and background
ax.grid(axis="y", color="#bcbcbc", linestyle="--", linewidth=0.5, alpha=0.7)
ax.set_axisbelow(True)
ax.set_facecolor("#F5F5F1")
fig.patch.set_facecolor("#F5F5F1")

# Show the plot
plt.tight_layout()
plt.show()
