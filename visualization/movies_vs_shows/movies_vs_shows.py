import pandas as pd
import matplotlib.pyplot as plt

file_path = "../../datasets/movies_show_percentage.csv"
df = pd.read_csv(file_path)

# Netflix colors
netflix_red = "#E50914"
netflix_dark = "#221F1F"
netflix_gray = "#B81D24"

# Bar Chart: Shows vs Movies
plt.figure(figsize=(8, 6))
bars = plt.bar(
    df["type"], 
    df["Percentage"], 
    color=[netflix_red, netflix_gray], 
    edgecolor="white"
)

# Add centered value labels inside the bars
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2, 
        height / 2,  # Centered vertically
        f"{height:.1f}%", 
        ha="center", 
        va="center", 
        color="white", 
        fontsize=12, 
        fontweight="bold"
    )

# Customize the chart
plt.title("Netflix Content Distribution: Shows vs Movies", fontsize=16, fontweight="bold", color="white")
plt.ylabel("Percentage", fontsize=12, color="white")
plt.xticks(color="white", fontsize=12)
plt.yticks(color="white", fontsize=10)
plt.gca().set_facecolor(netflix_dark)
plt.grid(axis="y", linestyle="--", alpha=0.3, color="gray")

# Save the bar chart
plt.tight_layout()
plt.savefig("netflix_shows_vs_movies.png", dpi=300, facecolor=netflix_dark)
plt.show()