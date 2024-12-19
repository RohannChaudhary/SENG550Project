import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
file_path = "../../datasets/genre_ratings.csv" 
df = pd.read_csv(file_path)

# Sort genres by average IMDb rating
df = df.sort_values(by="average_imdb_rating", ascending=False)

# Calculate 'impact' values as deviation from mean IMDb rating
impact_values = df["average_imdb_rating"] - df["average_imdb_rating"].mean()

# Set up the Netflix theme
plt.style.use("dark_background")  
netflix_red = "#E50914"
netflix_gray = "#B81D24"

# Create the SHAP-like scatter plot
plt.figure(figsize=(12, 8))

plt.scatter(
    impact_values,                # X-axis: IMDb Rating Impact
    df["genre"],                  # Y-axis: Genres
    color=netflix_red,            
    s=100, edgecolor="white", alpha=0.8
)

# Add a vertical line at 0 for reference
plt.axvline(0, color=netflix_gray, linestyle="--", linewidth=1)

# Customize chart aesthetics
plt.title("IMDb Rating Impact on Genres", 
          fontsize=16, fontweight="bold", color="white")
plt.xlabel("IMDb Rating Impact (Deviation from Mean)", fontsize=12, color="white")
plt.ylabel("Genre", fontsize=12, color="white")

# Customize tick labels and grid
plt.xticks(color="white", fontsize=10)
plt.yticks(color="white", fontsize=10)
plt.grid(axis="x", color="#444444", linestyle="--", linewidth=0.5)
# Save the figure
plt.tight_layout()
plt.savefig("genre_imdb_plot.png", dpi=300, bbox_inches="tight")
plt.show()
