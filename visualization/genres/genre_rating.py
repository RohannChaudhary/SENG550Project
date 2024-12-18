import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv("datasets/genre_ratings.csv")  # Replace with your file path

# Remove rows with missing values in 'average_imdb_rating' or 'average_tmdb_rating'
df = df.dropna(subset=["average_imdb_rating", "average_tmdb_rating"])

# Sort genres by average IMDb ratings for better visualization
df = df.sort_values("average_imdb_rating")

# Define plot size and aesthetics
plt.figure(figsize=(12, 8))
plt.title("Comparison of IMDb and TMDb Ratings by Genre", fontsize=16, fontweight="bold")
plt.xlabel("Genres", fontsize=12)
plt.ylabel("Average Rating", fontsize=12)
plt.ylim(df["average_imdb_rating"].min() - 0.1, df["average_tmdb_rating"].max() + 0.1)  # Adjust limits to fit data

# Plot IMDb and TMDb ratings
plt.plot(df["genre"], df["average_imdb_rating"], marker="o", label="IMDb Rating", linewidth=2, color="#1f77b4")
plt.plot(df["genre"], df["average_tmdb_rating"], marker="o", label="TMDb Rating", linewidth=2, color="#ff7f0e")

# Add lines to connect points for each genre
for i, genre in enumerate(df["genre"]):
    plt.plot(
        [genre, genre],
        [df.iloc[i]["average_imdb_rating"], df.iloc[i]["average_tmdb_rating"]],
        color="gray",
        linestyle="--",
        alpha=0.7
    )

# Add data labels to the points
for i in range(len(df)):
    plt.text(
        df.iloc[i]["genre"],
        df.iloc[i]["average_imdb_rating"] - 0.02,
        f"{df.iloc[i]['average_imdb_rating']:.2f}",
        ha="center",
        fontsize=10,
        color="#1f77b4"
    )
    plt.text(
        df.iloc[i]["genre"],
        df.iloc[i]["average_tmdb_rating"] + 0.02,
        f"{df.iloc[i]['average_tmdb_rating']:.2f}",
        ha="center",
        fontsize=10,
        color="#ff7f0e"
    )

# Customize the legend
plt.legend(title="Ratings Source", loc="upper left", fontsize=10)

# Style gridlines
plt.grid(axis="y", color="gray", linestyle="--", alpha=0.7)
plt.gca().set_facecolor("#f5f5f5")

# Show the plot
plt.tight_layout()
plt.show()
