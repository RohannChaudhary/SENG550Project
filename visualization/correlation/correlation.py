import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

file_path = "../../datasets/correlation.csv"
df = pd.read_csv(file_path)

correlation_matrix = df[["imdb_votes", "tmdb_popularity"]].corr()
plt.figure(figsize=(6, 5))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap")
plt.savefig("correlation_heatmap.png")  # Save the figure
plt.close()

print("Correlation heatmap saved as 'correlation_heatmap.png'.")

# Scatter plot with transparency
plt.figure(figsize=(12, 8))
sns.scatterplot(x="imdb_votes", y="tmdb_popularity", data=df, alpha=0.4)
plt.title("Relationship Between IMDb Votes and TMDB Popularity")
plt.xlabel("IMDb Votes")
plt.ylabel("TMDB Popularity")
plt.grid()
plt.savefig("scatter_transparency.png")  # Save the figure
plt.close()

print("Scatter plot saved as 'scatter_transparency.png'.")
